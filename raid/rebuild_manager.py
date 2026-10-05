from raid.config import DRIVES
from raid.status import RAIDStatus
from raid.rebuild import rebuild_pair


def rebuild_drive(source_id, target_id, stripe_indexes):
    print(f"RAID Status: {RAIDStatus.REBUILDING}")

    source = DRIVES[source_id]
    target = DRIVES[target_id]

    rebuilt, failed = rebuild_pair(
        source,
        target,
        stripe_indexes
    )

    if failed:
        print(f"RAID Status: {RAIDStatus.FAILED}")
        return False

    print(f"Rebuilt stripes: {len(rebuilt)}")
    print(f"RAID Status: {RAIDStatus.HEALTHY}")

    return True