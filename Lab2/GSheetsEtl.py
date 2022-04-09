from SpatialEtl import SpatialETL

class GSheetsEtl(SpatialETL):
    config_dict = None
    def __init__(self, config_dict):
            super().__init__(self.config_dict)

    def process(self):
        super().extract()
        super().transform()
        super().load()