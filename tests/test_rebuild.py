from raid.config import DRIVES
from raid.rebuild import rebuild_file


def main():
    print("=== RAID REBUILD TEST ===")

    source = DRIVES["E"] / "stripe_0.bin"
    target = DRIVES["D"] / "stripe_0.bin"

    print(f"Source : {source}")
    print(f"Target : {target}")

    success = rebuild_file(source, target)

    if success:
        print("Rebuild successful.")
    else:
        print("Rebuild failed.")


if __name__ == "__main__":
    main()