from raid.metadata import create_metadata


metadata = create_metadata()

print("=== RAID METADATA ===")
print(f"RAID Level : {metadata['raid_level']}")
print(f"Chunk Size : {metadata['chunk_size']} bytes")
print(f"Mirror Pairs: {metadata['mirror_pairs']}")
print(f"RAID Status: {metadata['raid_status']}")

print("\nDrive Status:")
for drive, status in metadata["drive_status"].items():
    print(f"{drive}: {status}")
