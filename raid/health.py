from raid.config import DRIVES
from raid.status import RAIDStatus


def check_drive_health():
    status = {}

    for drive_id, path in DRIVES.items():
        if path.exists() and path.is_dir():
            status[drive_id] = "ONLINE"
        else:
            status[drive_id] = "OFFLINE"

    return status


def get_raid_status(drive_status):
    online_count = sum(
        1
        for status in drive_status.values()
        if status == "ONLINE"
    )

    if online_count == 4:
        return RAIDStatus.HEALTHY

    if online_count == 3:
        return RAIDStatus.DEGRADED

    if online_count == 2:
        # One surviving drive in each mirror pair
        if (
            drive_status["D"] == "ONLINE"
            and drive_status["E"] == "OFFLINE"
            and drive_status["F"] == "ONLINE"
            and drive_status["G"] == "OFFLINE"
        ):
            return RAIDStatus.DEGRADED

        if (
            drive_status["D"] == "OFFLINE"
            and drive_status["E"] == "ONLINE"
            and drive_status["F"] == "OFFLINE"
            and drive_status["G"] == "ONLINE"
        ):
            return RAIDStatus.DEGRADED

        return RAIDStatus.FAILED


import time


def measure_drive_latency(drive_path):
    test_file = drive_path / "stripe_0.bin"

    if not test_file.exists():
        return None

    start = time.perf_counter()

    try:
        with open(test_file, "rb") as file:
            file.read()
    except OSError:
        return None

    end = time.perf_counter()

    return (end - start) * 1000


def select_best_drive(pair):
    results = {}

    for drive_id, drive_path in pair:
        latency = measure_drive_latency(drive_path)

        if latency is not None:
            results[drive_id] = latency

    if not results:
        return None, {}

    best_drive = min(
        results,
        key=results.get
    )

    return best_drive, results
    return RAIDStatus.FAILED