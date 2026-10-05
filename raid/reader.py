from pathlib import Path
from raid.health import select_best_drive


def read_from_drive(drive_path, filename):
    file_path = Path(drive_path) / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    with open(file_path, "rb") as file:
        return file.read()


def read_from_mirror(pair, filename):
    best_drive, latency = select_best_drive(pair)

    if best_drive is None:
        raise IOError("All mirror drives are unavailable.")

    drive_paths = dict(pair)

    try:
        data = read_from_drive(
            drive_paths[best_drive],
            filename
        )

        return {
            "drive": best_drive,
            "data": data,
            "latency": latency,
            "failed_drives": []
        }

    except (FileNotFoundError, OSError) as error:
        failed_drives = [(best_drive, str(error))]

        for drive_id, drive_path in pair:
            if drive_id == best_drive:
                continue

            try:
                data = read_from_drive(
                    drive_path,
                    filename
                )

                return {
                    "drive": drive_id,
                    "data": data,
                    "latency": latency,
                    "failed_drives": failed_drives
                }

            except (FileNotFoundError, OSError) as fallback_error:
                failed_drives.append(
                    (drive_id, str(fallback_error))
                )

        raise IOError(
            "All mirror drives are unavailable."
        )