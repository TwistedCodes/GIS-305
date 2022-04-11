
class SpatialEtl:

    def __init__(self, config_dict):
        self.config_dict = config_dict

    def extract(self):
        print(f"Extracting data from {self.config_dict('remote_url')}" f"to {self.config_dict.get('project_dir')}")

    def transform(self):
        print(f"Transforming")

    def load(self):
        print(f"Loading data into...")
