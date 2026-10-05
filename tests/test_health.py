from raid.health import check_drive_health, get_raid_status


def main():
    print("=== RAID HEALTH TEST ===")

    drive_status = check_drive_health()

    for drive, status in drive_status.items():
        print(f"Drive {drive}: {status}")

    raid_status = get_raid_status(drive_status)

    print(f"\nRAID Status: {raid_status}")


if __name__ == "__main__":
    main()