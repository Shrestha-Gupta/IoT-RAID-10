from pathlib import Path

# =========================
# RAID-10 Configuration
# =========================

RAID_LEVEL = 10

# Four physical USB drives
DRIVES = {
    "D": Path(r"D:\IoTRAID_TEST"),
    "E": Path(r"E:\IoTRAID_TEST"),
    "F": Path(r"F:\IoTRAID_TEST"),
    "G": Path(r"G:\IoTRAID_TEST"),
}

# RAID-10 mirror pairs
MIRROR_PAIRS = [
    ("D", "E"),
    ("F", "G"),
]

# Smallest drive is approximately 157 GB.
# We will determine the exact usable capacity later.
CHUNK_SIZE = 1024 * 1024  # 1 MB

# Metadata location
METADATA_FILE = Path("raid_metadata.json")