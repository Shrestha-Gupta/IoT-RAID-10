from raid.config import DRIVES
from raid.checksum import verify_files


def main():
    file_d = DRIVES["D"] / "stripe_0.bin"
    file_e = DRIVES["E"] / "stripe_0.bin"

    match, checksum_d, checksum_e = verify_files(
        file_d,
        file_e
    )

    print("=== RAID INTEGRITY TEST ===")
    print(f"D SHA-256: {checksum_d}")
    print(f"E SHA-256: {checksum_e}")

    if match:
        print("INTEGRITY: PASS")
    else:
        print("INTEGRITY: FAIL")


if __name__ == "__main__":
    main()