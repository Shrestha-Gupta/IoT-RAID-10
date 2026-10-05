from raid.writer import write_data


def main():
    print("=== DEGRADED WRITE TEST ===")

    result = write_data(
        b"DATA_WRITTEN_DURING_DEGRADED_MODE",
        0
    )

    print(f"Mirror Pair : {result['pair']}")
    print(f"Successful  : {result['successful']}")
    print(f"Failed      : {result['failed']}")
    print(f"RAID Status : {result['status']}")


if __name__ == "__main__":
    main()