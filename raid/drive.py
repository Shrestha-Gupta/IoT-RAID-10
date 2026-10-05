from pathlib import Path


class Drive:
    def __init__(self, drive_id, path):
        self.drive_id = drive_id
        self.path = Path(path)

    def exists(self):
        return self.path.exists()

    def is_directory(self):
        return self.path.is_dir()

    def is_available(self):
        return self.exists() and self.is_directory()

    def status(self):
        if self.is_available():
            return "ONLINE"
        return "OFFLINE"

    def __repr__(self):
        return f"Drive({self.drive_id}, {self.path}, {self.status()})"