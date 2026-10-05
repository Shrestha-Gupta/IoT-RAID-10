from raid.writer import write_data


def main():
    print("=== MULTIPLE DEGRADED WRITES ===")

    for stripe_index in range(4, 10):
        data = f"DEGRADED_DATA_{stripe_index}".encode()

        result = write_data(
            data,
            stripe_index
        )

        print(
            f"Stripe {stripe_index} | "
            f"Pair {result['pair']} | "
            f"Success {result['successful']} | "
            f"Failed {result['failed']} | "
            f"Status {result['status']}"
        )


if __name__ == "__main__":
    main()