from pathlib import Path
import shutil

from raid.checksum import verify_files


def rebuild_pair(source_drive, target_drive, stripe_indexes):
    rebuilt = []
    failed = []

    for stripe_index in stripe_indexes:
        filename = f"stripe_{stripe_index}.bin"

        source = Path(source_drive) / filename
        target = Path(target_drive) / filename

        try:
            if not source.exists():
                failed.append((filename, "Source missing"))
                continue

            shutil.copy2(source, target)

            if not target.exists():
                failed.append((filename, "Target not created"))
                continue

            match, _, _ = verify_files(source, target)

            if match:
                rebuilt.append(filename)
            else:
                failed.append(
                    (filename, "Checksum verification failed")
                )

        except Exception as error:
            failed.append((filename, str(error)))

    return rebuilt, failed