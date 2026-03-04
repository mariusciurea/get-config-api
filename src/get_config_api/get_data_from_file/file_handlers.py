import json
# import os
#
# from fastapi.params import Depends
from pathlib import Path

from src.get_config_api.get_data_from_file.base import FileHandler


class JSONFileHandler(FileHandler):

    def read_file(self, file_path: Path) -> list[dict]:
        """Return json data from file_path"""

        with open(file_path, mode="r", encoding="utf-8") as json_file:
            data = json.load(json_file)

        return data


class CSVFileHandler(FileHandler):
    def read_file(self, file_path: Path) -> dict:
        pass


class ExcelFileHandler(FileHandler):
    def read_file(self, file_path: Path) -> dict:
        pass


class DOCXFileHandler(FileHandler):
    def read_file(self, file_path: Path) -> list[dict]:
        pass



# class FileData:
#     def __init__(self):
#         self.json_data = JSONFileHandler()
#         self.csv_data = CSVFileHandler()
#         self.excel_data = ExcelFileHandler()
#
#     def read_data(self, file_path: str):
#         if os.path.splitext(file_path)[1] == ".json":
#             return self.json_data.read_file(file_path)
#         elif os.path.splitext(file_path)[1] == ".csv":
#             return self.csv_data.read_file(file_path)
#         elif os.path.splitext(file_path)[1] == ".xlsx":
#             return self.excel_data.read_file(file_path)
#         return


# class FileData:
#     def __init__(self, file_type: FileHandler):
#         self.file_type = file_type
#
#     def read_data(self, file_path: str):
#         self.file_type.read_file(file_path)


if __name__ == '__main__':
    from src.get_config_api.settings import get_settings

    settings_obj = get_settings()

    json_handler = JSONFileHandler()
    data = json_handler.read_file(settings_obj.DATA_DIR / "network_elements_data.json")
    print(type(data))

