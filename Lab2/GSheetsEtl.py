from SpatialEtl import SpatialEtl


class GSheetsEtl(SpatialEtl):
    config_dict = None
    def __init__(self, config_dict):
            super().__init__(self.config_dict)

    def process(self):
        super().extract()
        # transform()
        # load()