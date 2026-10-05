from raid.config import DRIVES
from raid.reader import read_from_drive


def main():
    print("=== RAID READ TEST ===")

    data = read_from_drive(
        DRIVES["D"],
        "stripe_0.bin"
    )

    print("Read from D:")
    print(data.decode())


if __name__ == "__main__":
    main()