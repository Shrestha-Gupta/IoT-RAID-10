from raid.config import DRIVES, MIRROR_PAIRS
from raid.stripe import get_target_pair
from raid.mirror import write_mirror


def write_data(data, stripe_index):
    pair_ids = get_target_pair(
        stripe_index,
        MIRROR_PAIRS
    )

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

    if len(successful) == 2:
        status = "HEALTHY"

    elif len(successful) == 1:
        status = "DEGRADED"

    else:
        status = "FAILED"

    return {
        "stripe": stripe_index,
        "pair": pair_ids,
        "successful": successful,
        "failed": failed,
        "status": status
    }