from raid.config import DRIVES
from raid.health import select_best_drive


def main():
    pair = [
        ("D", DRIVES["D"]),
        ("E", DRIVES["E"])
    ]

    best_drive, latency = select_best_drive(pair)

    print("=== READ OPTIMIZATION TEST ===")

    for drive, value in latency.items():
        print(f"Drive {drive}: {value:.3f} ms")

    print(f"\nSelected drive: {best_drive}")


if __name__ == "__main__":
    main()