import hashlib
from pathlib import Path


def calculate_checksum(file_path):
    file_path = Path(file_path)

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def verify_files(file1, file2):
    checksum1 = calculate_checksum(file1)
    checksum2 = calculate_checksum(file2)

    return checksum1 == checksum2, checksum1, checksum2