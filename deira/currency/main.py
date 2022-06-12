import os

from datetime import date
from dagster import job, op

from database import currency_db
from dataset import currency_dataset

@op
def create_params():
    root_folder = './bcb_download'
    actual_year = date.today().year
    actual_date = date.today().strftime("%Y%m%d")
    actual_year_folder = f'{ root_folder}/{ actual_year }'
    local_file_path = f'{ actual_year_folder }/20220610.csv'

    params = {}
    for variable in ['root_folder','actual_year', 'actual_date', 'actual_year_folder', 'local_file_path']:
        params[variable] = eval(variable)

    return params

@op
def create_folders(params):
    os.makedirs( params['root_folder'] , exist_ok=True)
    os.makedirs( params['actual_year_folder'] , exist_ok=True)
    return True

@op
def download_data(params, folders):
    if folders:
        currency = currency_dataset()
        currency.download(params)
        return True

@op
def check_table(params):
    currency = currency_db()
    tableExists = currency.check_table()
    print(tableExists)
    return True

@op
def insert_data(context, params,downloaded_data):
    currency = currency_db()
    currency.insert_data(context,downloaded_data)
    return True

@job
def job():
    params = create_params()
    folders_created = create_folders(params)
    downloaded_data = download_data(params, folders_created)
    checked_table = check_table(params)
    inserted_data = insert_data(params, downloaded_data)