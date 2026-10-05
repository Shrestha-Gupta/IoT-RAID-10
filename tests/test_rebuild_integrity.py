from raid.config import DRIVES
from raid.checksum import verify_files


def main():
    print("=== REBUILD INTEGRITY TEST ===")

    stripe_indexes = [0, 2, 4, 6, 8]

    all_passed = True

    for stripe_index in stripe_indexes:
        filename = f"stripe_{stripe_index}.bin"

        file_d = DRIVES["D"] / filename
        file_e = DRIVES["E"] / filename

        match, checksum_d, checksum_e = verify_files(
            file_d,
            file_e
        )

        print(f"\n{filename}")
        print(f"D SHA-256: {checksum_d}")
        print(f"E SHA-256: {checksum_e}")

        if match:
            print("Integrity: PASS")
        else:
            print("Integrity: FAIL")
            all_passed = False

    print("\n==============================")

    if all_passed:
        print("ALL REBUILT STRIPES VERIFIED")
    else:
        print("INTEGRITY CHECK FAILED")


if __name__ == "__main__":
    main()