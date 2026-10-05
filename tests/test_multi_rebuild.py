from raid.config import DRIVES
from raid.rebuild import rebuild_pair


def main():
    print("=== MULTI-STRIPE REBUILD TEST ===")

    stripe_indexes = [0, 2, 4, 6, 8]

    rebuilt, failed = rebuild_pair(
        DRIVES["E"],
        DRIVES["D"],
        stripe_indexes
    )

    print("\nRebuilt:")
    for filename in rebuilt:
        print(f"  {filename}")

    print("\nFailed:")
    for filename, reason in failed:
        print(f"  {filename} -> {reason}")

    print(f"\nTotal rebuilt: {len(rebuilt)}")


if __name__ == "__main__":
    main()