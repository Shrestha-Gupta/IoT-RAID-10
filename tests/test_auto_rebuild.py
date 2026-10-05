from raid.rebuild_manager import rebuild_drive


def main():
    print("=== AUTOMATIC REBUILD TEST ===")

    stripe_indexes = [0, 2, 4, 6, 8]

    success = rebuild_drive(
        "E",
        "D",
        stripe_indexes
    )

    if success:
        print("\nREBUILD COMPLETED SUCCESSFULLY")
    else:
        print("\nREBUILD FAILED")


if __name__ == "__main__":
    main()