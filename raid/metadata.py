import json
from pathlib import Path

from raid.config import RAID_LEVEL, DRIVES, MIRROR_PAIRS, CHUNK_SIZE, METADATA_FILE


def create_metadata():
    metadata = {
        "raid_level": RAID_LEVEL,
        "chunk_size": CHUNK_SIZE,
        "drives": {
            drive_id: str(path)
            for drive_id, path in DRIVES.items()
        },
        "mirror_pairs": MIRROR_PAIRS,
        "drive_status": {
            drive_id: "ONLINE"
            for drive_id in DRIVES
        },
        "raid_status": "HEALTHY"
    }

    with open(METADATA_FILE, "w") as file:
        json.dump(metadata, file, indent=4)

    return metadata


def load_metadata():
    if not Path(METADATA_FILE).exists():
        return None

    with open(METADATA_FILE, "r") as file:
        return json.load(file)