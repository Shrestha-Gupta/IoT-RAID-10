def write_mirror(pair, filename, data):
    successful = []
    failed = []

    for drive_id, drive_path in pair:
        try:
            file_path = drive_path / filename

            with open(file_path, "wb") as file:
                file.write(data)

            successful.append(drive_id)

        except Exception as error:
            failed.append((drive_id, str(error)))

    return successful, failed