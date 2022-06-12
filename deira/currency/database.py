from io import StringIO
from dagster import Failure

import pandas as pd
import psycopg2
import os

host = os.environ['POSTGRES_HOST']
dbname = os.environ['POSTGRES_DBNAME']
user = os.environ['POSTGRES_USER']
password = os.environ['POSTGRES_PASSWORD']

class currency_db:
    def __init__(self):
        #Define our connection string
        self.conn_string = f"host='{host}' dbname='{dbname}' user='{user}' password='{password}'"

        # get a connection, if a connect cannot be made an exception will be raised here
        self.conn = psycopg2.connect(self.conn_string)

    def check_table(self):
        sql = f"""SELECT 1 FROM public.currency"""
        print(sql)

    def create_table(self):

        sql = f"""
            CREATE TABLE public.currency (
                "data" date NOT NULL,
                cod_moeda varchar(10) NOT NULL,
                tipo_moeda varchar(1) NOT NULL,
                moeda varchar(3) NOT NULL,
                taxa_compra float8 NOT NULL,
                taxa_venda float8 NOT NULL,
                paridade_compra float8 NOT NULL,
                paridade_venda float8 NOT NULL,
                deleted bool NULL DEFAULT false,
                CONSTRAINT currency_pk PRIMARY KEY (data, moeda)
            );
            CREATE INDEX currency_data_idx ON public.currency USING btree (data, moeda);
        """
        print(sql)

    def insert_data(self, context, downloaded_data):
        if downloaded_data:
            df = pd.read_csv('./bcb_download/2022/20220610.csv',
                sep=';', 
                encoding='ISO-8859-1',
                header=None,
                decimal=',',
                thousands='.',
                dtype = { 1 : 'string' }
            )

            # add deleted column
            df["deleted"] = 0

            # Saving dataframe to stringio to perform bulk_data_load
            buffer = StringIO()
            df.to_csv(buffer, header=False, index=False)
            buffer.seek(0)

            # conn.cursor will return a cursor object, you can use this cursor to perform queries
            cursor = self.conn.cursor()
            
            try:
                cursor.copy_from(buffer, 'currency', sep=',')
                self.conn.commit()
                cursor.close()
                self.conn.close()
                context.log.info('Data loaded successfully')
                return True

            except (Exception, psycopg2.DatabaseError) as error:
                self.conn.rollback()
                cursor.close()
                self.conn.close()
                raise Failure(
                    description="Some database error occurred",
                    metadata={
                        "error": str(error)
                    }
                )
                return False
            