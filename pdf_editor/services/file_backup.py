import os
from pathlib import Path
import shutil


class FileBackupService:
    _BACKUP_FILE_NAME_SUFFIX = "_backup"

    def __init__(self, file_path: Path):
        self._file_path = file_path

    @property
    def _backup_file_path(self):
        return self._file_path.with_stem(f"{self._file_path.stem}{self._BACKUP_FILE_NAME_SUFFIX}")

    def restore(self):
        os.replace(self._backup_file_path, self._file_path)

    def remove(self):
        os.remove(self._backup_file_path)

    def create(self):
        shutil.copy(self._file_path, self._backup_file_path)
