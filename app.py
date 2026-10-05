from flask import Flask, request, jsonify
from datetime import datetime

from raid.writer import write_data
from raid.health import check_drive_health, get_raid_status
from influx import write_sensor_data

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "system": "IoT-Based RAID 10 Storage System",
        "status": "running"
    })


@app.route("/api/data", methods=["POST"])
def receive_data():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "status": "error",
                "message": "No JSON data received"
            }), 400

        temperature = data.get("temperature")
        humidity = data.get("humidity")
        distance = data.get("distance")

        if temperature is None or humidity is None or distance is None:
            return jsonify({
                "status": "error",
                "message": "Missing sensor data"
            }), 400

        timestamp = datetime.now().isoformat()

        sensor_record = {
            "timestamp": timestamp,
            "temperature": float(temperature),
            "humidity": float(humidity),
            "distance": float(distance)
        }

        # -----------------------------
        # 1. Write to InfluxDB
        # -----------------------------
        influx_status = "success"
        influx_error = None

        try:
            write_sensor_data(sensor_record)
        except Exception as error:
            influx_status = "failed"
            influx_error = str(error)

        # -----------------------------
        # 2. Write to RAID-10
        # -----------------------------
        raid_data = str(sensor_record).encode("utf-8")

        stripe_index = int(datetime.now().timestamp() * 1000)

        raid_result = write_data(
            raid_data,
            stripe_index
        )

        # -----------------------------
        # 3. Check RAID health
        # -----------------------------
        drive_status = check_drive_health()
        raid_status = get_raid_status(drive_status)

        # -----------------------------
        # Response
        # -----------------------------
        return jsonify({
            "status": "success",
            "timestamp": timestamp,

            "sensor_data": sensor_record,

            "storage": {
                "influxdb": {
                    "status": influx_status,
                    "error": influx_error
                },

                "raid": {
                    "stripe": stripe_index,
                    "pair": raid_result["pair"],
                    "successful": raid_result["successful"],
                    "failed": raid_result["failed"],
                    "status": raid_status
                }
            },

            "drives": drive_status
        }), 200

    except Exception as error:

        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500


@app.route("/api/status", methods=["GET"])
def system_status():

    drive_status = check_drive_health()
    raid_status = get_raid_status(drive_status)

    return jsonify({
        "system": "IoT-Based RAID 10 Storage System",
        "raid_status": raid_status,
        "drives": drive_status
    })


if __name__ == "__main__":

    print("======================================")
    print(" IoT RAID 10 Storage Server")
    print("======================================")
    print("Server: http://0.0.0.0:5000")
    print("")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )