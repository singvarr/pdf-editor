import os
from pathlib import Path
import shutil


class FileBackupService:
    _BACKUP_FILE_NAME_SUFFIX = "_backup"

    def __init__(self, file_path: Path):
        self._file_path = file_path

    @staticmethod
    def remove_file(path: str):
        os.remove(path)

    @property
    def _backup_file_path(self):
        return self._file_path.with_stem(f"{self._file_path.stem}{self._BACKUP_FILE_NAME_SUFFIX}")

    def restore(self):
        os.replace(self._backup_file_path, self._file_path)

    def remove(self):
        FileBackupService.remove_file(self._backup_file_path)

    def create(self):
        shutil.copy(self._file_path, self._backup_file_path)
