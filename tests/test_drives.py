from raid.config import DRIVES
from raid.drive import Drive


def main():
    print("=== RAID DRIVE STATUS ===")

    for drive_id, path in DRIVES.items():
        drive = Drive(drive_id, path)

        print(
            f"Drive {drive_id}: "
            f"{drive.path} -> {drive.status()}"
        )


if __name__ == "__main__":
    main()