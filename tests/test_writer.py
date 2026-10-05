from raid.writer import write_data


def main():
    print("=== RAID-10 WRITER TEST ===")

    test_data = [
        b"DATA_CHUNK_0",
        b"DATA_CHUNK_1",
        b"DATA_CHUNK_2",
        b"DATA_CHUNK_3"
    ]

    for index, data in enumerate(test_data):

        result = write_data(
            data,
            index
        )

        print(
            f"Stripe {result['stripe']} "
            f"-> {result['pair']} "
            f"Success: {result['successful']} "
            f"Failed: {result['failed']}"
        )


if __name__ == "__main__":
    main()