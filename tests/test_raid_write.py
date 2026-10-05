from raid.config import DRIVES, MIRROR_PAIRS
from raid.stripe import get_target_pair
from raid.mirror import write_mirror


def write_stripe(stripe_index, data):
    pair_ids = get_target_pair(stripe_index, MIRROR_PAIRS)

    print(f"\nStripe {stripe_index} -> Mirror Pair {pair_ids}")

    pair = [
        (drive_id, DRIVES[drive_id])
        for drive_id in pair_ids
    ]

    filename = f"stripe_{stripe_index}.bin"

    successful, failed = write_mirror(
        pair,
        filename,
        data
    )

    print(f"Successful writes: {successful}")
    print(f"Failed writes: {failed}")


def main():
    print("=== RAID-10 STRIPING TEST ===")

    write_stripe(
        0,
        b"RAID10_STRIPE_0"
    )

    write_stripe(
        1,
        b"RAID10_STRIPE_1"
    )


if __name__ == "__main__":
    main()