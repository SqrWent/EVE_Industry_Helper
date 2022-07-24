import os
from FileManaging import DFManaging
import RawDataFetching as RawDF


def source_dir() -> str:
    return "src"


__source_dir__ = source_dir()


class DataFile:
    """
    Description:
        A simple data managing class.
    """

    def __init__(self, exists_or_not: bool = False, **kwargs) -> None:
        self.exists = exists_or_not
        self.dir: str = DFManaging.default_value("dir", kwargs)
        self.mtime: float = DFManaging.default_value("mtime", kwargs)
        self.size: int = DFManaging.default_value("size", kwargs)

    def load(self, mode: str = "r") -> object:
        if self.exists & (self.dir is not None):
            file = open(self.dir, mode)
            return file
        else:
            # Raise error when the file does not exist.
            raise ValueError("File does not exists or empty directory!")


class EIH:
    """
    Description:
        This is the main class of the EIH project.
    """

    def __init__(self):

        # Check if id_sheet.json exists
        if os.path.exists(__source_dir__ + "/id_sheet.json"):
            directory = __source_dir__ + "/id_sheet.json"
            self.id_sheet = DataFile(True,
                                     dir=directory,
                                     mtime=os.path.getmtime(directory),
                                     size=os.path.getsize(directory))
        else:
            self.id_sheet = DataFile(False)

        # Check if object_info.yaml exists
        if os.path.exists(__source_dir__ + "/object_info.yaml"):
            directory = __source_dir__ + "/object_info.yaml"
            self.object_info = DataFile(True,
                                        dir=directory,
                                        mtime=os.path.getmtime(directory),
                                        size=os.path.getsize(directory))
        else:
            self.object_info = DataFile(False)

    @staticmethod
    def renew_objects() -> None:
        RawDF.fetch_id_sheets()
        RawDF.fetch_object_infos()
        print("Renew Object Information Finished!")
