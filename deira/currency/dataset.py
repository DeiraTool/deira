from dagster import Failure

import requests

class currency_dataset:
    def __init__(self):
        self.base_url = "https://www4.bcb.gov.br/Download/fechamento/"
        self.data =  '20220610'

    def define_data_range(self, data):
        return True

    def download(self, params):
        url = f"https://www4.bcb.gov.br/Download/fechamento/{self.data}.csv"
        csv = requests.get(url, stream=True).content

        with open(params['local_file_path'], 'wb') as file_path:
            file_path.write(csv)
            return True