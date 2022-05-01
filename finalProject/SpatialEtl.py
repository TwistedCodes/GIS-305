"""
Defines what will be put through the process of extract, transform
and load as well as telling it where to get the information from
"""
class SpatialEtl:

    def __init__(self, config_dict):
        self.config_dict = config_dict

    def extract(self):
        print(f"Extracting data from {self.config_dict.get('remote_url')} to {self.config_dict.get('project_dir')}")

    def transform(self):
        print(f"Transforming")

    def load(self):
        print(f"Loading data into...")
