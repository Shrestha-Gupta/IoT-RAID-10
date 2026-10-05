from raid.config import DRIVES
from raid.reader import read_from_mirror


def main():
    print("=== RAID MIRROR FAILOVER TEST ===")

    pair = [
        ("D", DRIVES["D"]),
        ("E", DRIVES["E"])
    ]

    result = read_from_mirror(
        pair,
        "stripe_0.bin"
    )

    print(f"Data read from: {result['drive']}")
    print(f"Data: {result['data'].decode()}")
    print(f"Failed drives: {result['failed_drives']}")


if __name__ == "__main__":
    main()