from GSheetsEtl import GSheetsEtl
"""
Allows GSheets ETL to run and where it will get its information from
"""

if __name__ == "__main__":
    etl_instance = GSheetsEtl("https://foo_bar.com", "C:/Users", "GSheets", "C:/Users/my.gdb")

    etl_instance.process()