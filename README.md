# IoT-Based Data Storage System using Software-Defined RAID 10

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Flask-Backend-black?style=for-the-badge&logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/NodeMCU-ESP8266-red?style=for-the-badge&logo=arduino" alt="NodeMCU">
  <img src="https://img.shields.io/badge/InfluxDB-Time--Series%20DB-22ADF6?style=for-the-badge&logo=influxdb" alt="InfluxDB">
  <img src="https://img.shields.io/badge/Grafana-Monitoring-orange?style=for-the-badge&logo=grafana" alt="Grafana">
  <img src="https://img.shields.io/badge/RAID-10-success?style=for-the-badge" alt="RAID 10">
  <img src="https://img.shields.io/badge/OS-Windows%2011-0078D4?style=for-the-badge&logo=windows" alt="Windows 11">
</p>

<p align="center">
  <b>Reliable IoT Data Storage • Fault Tolerance • Real-Time Monitoring</b>
</p>

---

## 📌 Project Overview

This project presents an **IoT-based data storage and real-time monitoring system** designed to provide reliable local data storage, redundancy, fault tolerance, data integrity, and real-time visualization.

Environmental data is collected using sensors connected to a **NodeMCU ESP8266**. The NodeMCU transmits sensor readings over Wi-Fi using HTTP POST requests to a **Flask server running on Windows 11**.

The Flask server contains a **Python-based software-defined RAID 10 prototype** that implements core RAID 10 concepts including:

- Data striping
- Data mirroring
- Drive failure detection
- Degraded operation
- Read failover
- Drive rebuild and resynchronization
- SHA-256 integrity verification
- Drive health monitoring
- Read optimization

Sensor measurements are simultaneously stored in **InfluxDB** and visualized through a **Grafana dashboard**.

---

## 🏗️ System Architecture

```text
                         ┌──────────────────────┐
                         │      DHT11 Sensor     │
                         │ Temperature / Humidity│
                         └──────────┬───────────┘
                                    │
                         ┌──────────▼───────────┐
                         │    HC-SR04 Sensor    │
                         │      Distance        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  NodeMCU ESP8266     │
                         │                      │
                         │ Sensor Acquisition   │
                         │ Wi-Fi Communication  │
                         └──────────┬───────────┘
                                    │
                              HTTP POST / JSON
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Flask Server      │
                         │      Windows 11      │
                         └──────────┬───────────┘
                                    │
                    ┌───────────────┴────────────────┐
                    │                                │
                    ▼                                ▼
        ┌──────────────────────┐          ┌──────────────────────┐
        │ Software-Defined     │          │      InfluxDB        │
        │       RAID 10        │          │  Time-Series Storage │
        └──────────┬───────────┘          └──────────┬───────────┘
                   │                                 │
          ┌────────┴────────┐                        │
          │                 │                        │
          ▼                 ▼                        │
      ┌───────┐         ┌───────┐                    │
      │ D ↔ E │         │ F ↔ G │                    │
      │Mirror │         │Mirror │                    │
      │ Pair 1│         │ Pair 2│                    │
      └───────┘         └───────┘                    │
                                                    │
                                                    ▼
                                          ┌──────────────────────┐
                                          │       Grafana        │
                                          │  Real-Time Dashboard │
                                          └──────────────────────┘
```

---

## 🔄 Data Flow

```text
Sensors
   │
   ▼
NodeMCU ESP8266
   │
   │ Wi-Fi
   ▼
HTTP POST Request
   │
   ▼
Flask Server
   │
   ├──────────────► Python Software-Defined RAID 10
   │                         │
   │                         ├── Striping
   │                         ├── Mirroring
   │                         ├── Failure Detection
   │                         ├── Degraded Mode
   │                         ├── Failover
   │                         ├── Rebuild
   │                         └── Integrity Verification
   │
   └──────────────► InfluxDB
                            │
                            ▼
                          Grafana
```

---

# 🔧 Hardware Used

| Component | Purpose |
|---|---|
| **NodeMCU ESP8266** | IoT controller and Wi-Fi communication |
| **DHT11** | Temperature and humidity measurement |
| **HC-SR04** | Distance measurement |
| **Soil Moisture Sensor** | Planned sensor integration |
| **4 USB Storage Drives** | RAID 10 prototype storage |
| **Windows 11 Laptop** | Server and RAID prototype host |

---

# 💻 Software & Technologies

| Technology | Role |
|---|---|
| **Python** | RAID engine and backend logic |
| **Flask** | REST API server |
| **Arduino IDE** | NodeMCU programming |
| **InfluxDB** | Time-series sensor storage |
| **Grafana** | Real-time visualization |
| **HTTP / JSON** | NodeMCU-server communication |
| **Windows 11** | Prototype host operating system |
| **SHA-256** | Data integrity verification |

---

# 💾 RAID 10 Configuration

The prototype uses four physical storage drives organized into two mirror pairs.

```text
                 SOFTWARE-DEFINED RAID 10

                       RAID 10
                          │
             ┌────────────┴────────────┐
             │                         │
             ▼                         ▼
       Mirror Pair 1             Mirror Pair 2
          D ↔ E                     F ↔ G
             │                         │
             └────────────┬────────────┘
                          │
                       Striping
```

### Stripe Distribution

```text
Stripe 0  →  D + E
Stripe 1  →  F + G
Stripe 2  →  D + E
Stripe 3  →  F + G
Stripe 4  →  D + E
Stripe 5  →  F + G
```

Each stripe is mirrored across both members of its respective mirror pair.

---

# ⚙️ RAID Features

## 1. Data Striping

Logical data is distributed between the two mirror pairs.

```text
Stripe 0 → D/E
Stripe 1 → F/G
Stripe 2 → D/E
Stripe 3 → F/G
```

This provides the striping behavior associated with RAID 0.

---

## 2. Data Mirroring

Each stripe is written to both drives in its mirror pair.

```text
        D
        │
        │ Mirror
        ▼
        E
```

Similarly:

```text
        F
        │
        │ Mirror
        ▼
        G
```

This provides redundancy similar to RAID 1.

---

## 3. Drive Failure Detection

The system monitors the configured storage drives.

Possible drive states:

```text
ONLINE
OFFLINE
```

Possible RAID states:

```text
HEALTHY
DEGRADED
REBUILDING
FAILED
```

---

## 4. Degraded Mode

If one drive in a mirror pair becomes unavailable, the surviving drive continues serving the data.

Example:

```text
D → OFFLINE
E → ONLINE

F → ONLINE
G → ONLINE

RAID → DEGRADED
```

The system can continue receiving and storing sensor data.

---

## 5. Read Failover

When both mirror members are available, the system measures their read latency and can select the faster drive.

Example test:

```text
D latency = 0.3042 ms
E latency = 0.0586 ms

Selected drive = E
```

If the selected drive becomes unavailable, the other mirror member can be used.

---

## 6. Rebuild & Resynchronization

When a failed drive becomes available again, missing data can be rebuilt from its surviving mirror member.

```text
Before Failure

D  <──────────>  E


D becomes unavailable

D  OFFLINE
E  ONLINE


After D is restored

E  ────────────► D
      Rebuild
```

The system copies the missing data and verifies the rebuilt files.

---

## 7. SHA-256 Integrity Verification

SHA-256 checksums are used to verify rebuilt data.

```text
Source File
     │
     ▼
SHA-256 Checksum
     │
     ▼
Target File
     │
     ▼
SHA-256 Checksum
     │
     ▼
Compare
     │
 ┌───┴────┐
 │        │
Match   Mismatch
 │        │
 ▼        ▼
Valid   Failed
```

A rebuild is considered successful only when the source and target checksums match.

---

## 8. Drive Health Monitoring

The system continuously checks drive availability and determines the overall RAID state.

Example:

```text
D : ONLINE
E : ONLINE
F : ONLINE
G : ONLINE

RAID : HEALTHY
```

After a drive failure:

```text
D : OFFLINE
E : ONLINE
F : ONLINE
G : ONLINE

RAID : DEGRADED
```

---

# 📡 IoT Communication

The NodeMCU sends sensor readings to the Flask server in JSON format.

Example:

```json
{
  "temperature": 27.20,
  "humidity": 77.60,
  "distance": 36.31
}
```

The request is sent using:

```text
HTTP POST
```

API endpoint:

```text
POST /api/data
```

---

# 🖥️ Flask Backend

The Flask server acts as the central backend of the system.

### Main Responsibilities

- Receive sensor data
- Validate incoming JSON
- Store sensor data in InfluxDB
- Store sensor records through the RAID engine
- Monitor drive health
- Determine RAID status
- Return system status

### API Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Server information |
| `/api/data` | POST | Receive sensor data |
| `/api/status` | GET | Get RAID and drive status |

---

# 📊 InfluxDB

InfluxDB is used as the time-series database.

The following values are stored:

- Temperature
- Humidity
- Distance

Measurement:

```text
sensor_data
```

Example fields:

```text
temperature
humidity
distance
```

InfluxDB acts as the data source for Grafana.

---

# 📈 Grafana Dashboard

The project includes a Grafana dashboard named:

```text
IoT Storage Monitoring
```

The dashboard provides real-time visualization of:

### 🌡️ Temperature

Unit:

```text
°C
```

### 💧 Humidity

Unit:

```text
%
```

### 📏 Distance

Unit:

```text
cm
```

```text
              IoT Storage Monitoring

     ┌────────────────────────────────────┐
     │          Temperature               │
     │             27.20 °C               │
     │             ─────────               │
     └────────────────────────────────────┘

     ┌────────────────────────────────────┐
     │             Humidity               │
     │              77.60 %               │
     │             ─────────               │
     └────────────────────────────────────┘

     ┌────────────────────────────────────┐
     │             Distance               │
     │             36.31 cm               │
     │             ─────────               │
     └────────────────────────────────────┘
```

---

# 🧪 Live System Test

The complete physical system was tested using the NodeMCU and connected sensors.

### Example Live Reading

| Parameter | Value |
|---|---:|
| Temperature | **27.20 °C** |
| Humidity | **77.60 %** |
| Distance | **36.31 cm** |
| HTTP Response | **200** |
| InfluxDB | **Success** |
| RAID Status | **HEALTHY** |
| Mirror Pair | **F + G** |
| Successful Drives | **F, G** |
| Transmission Interval | **5 seconds** |

### NodeMCU Output

```text
Temperature: 27.20 °C
Humidity: 77.60 %
Distance: 36.31 cm

Sending JSON:
{"temperature":27.20,"humidity":77.60,"distance":36.31}

HTTP Response Code: 200
Server Response: success
```

---

# 🚨 RAID Failure Test

A physical drive failure test was performed by temporarily disconnecting the **D drive**.

### Before Failure

```text
D : ONLINE
E : ONLINE
F : ONLINE
G : ONLINE

RAID : HEALTHY
```

### After Disconnecting D

```text
D : OFFLINE
E : ONLINE
F : ONLINE
G : ONLINE

RAID : DEGRADED
```

Despite the drive failure:

- NodeMCU continued transmitting data
- Flask server remained operational
- HTTP requests continued returning `200`
- The surviving mirror drive E remained available
- Other RAID operations continued

This successfully demonstrated **fault-tolerant degraded operation**.

---

# 🔄 Recovery & Rebuild Test

After reconnecting the failed D drive, the rebuild process was executed.

```text
Drive Failure
      │
      ▼
DEGRADED State
      │
      ▼
Drive Reconnected
      │
      ▼
REBUILDING
      │
      ▼
Data Resynchronization
      │
      ▼
SHA-256 Verification
      │
      ▼
REBUILD COMPLETED
      │
      ▼
HEALTHY
```

### Result

```text
Automatic rebuild completed successfully.
Rebuild integrity verification passed successfully.
```

Therefore, the complete recovery cycle was successfully demonstrated:

```text
FAILURE
   ↓
DEGRADED
   ↓
RECOVERY
   ↓
REBUILD
   ↓
INTEGRITY VERIFICATION
   ↓
HEALTHY
```

---

# 🧪 Automated Testing

The project includes dedicated test modules for different RAID operations.

```text
tests/
│
├── test_drives.py
├── test_metadata.py
├── test_raid_write.py
├── test_raid_read.py
├── test_failover.py
├── test_health.py
├── test_rebuild.py
├── test_checksum.py
├── test_writer.py
├── test_degraded_write.py
├── test_degraded_multiple.py
├── test_multi_rebuild.py
├── test_rebuild_integrity.py
├── test_auto_rebuild.py
├── test_latency.py
└── test_optimized_read.py
```

### Tested Capabilities

| Feature | Tested |
|---|:---:|
| Drive Detection | ✅ |
| RAID Metadata | ✅ |
| Striping | ✅ |
| Mirroring | ✅ |
| RAID Read | ✅ |
| Read Failover | ✅ |
| Drive Health | ✅ |
| Degraded Mode | ✅ |
| Degraded Writes | ✅ |
| Rebuild | ✅ |
| Automatic Rebuild | ✅ |
| SHA-256 Verification | ✅ |
| Read Optimization | ✅ |

---

# 📁 Project Structure

```text
IoT_RAID/
│
├── app.py
├── influx.py
├── requirements.txt
├── .env
├── .gitignore
│
├── raid/
│   ├── __init__.py
│   ├── config.py
│   ├── metadata.py
│   ├── drive.py
│   ├── stripe.py
│   ├── mirror.py
│   ├── writer.py
│   ├── reader.py
│   ├── checksum.py
│   ├── health.py
│   ├── rebuild.py
│   ├── rebuild_manager.py
│   └── status.py
│
├── tests/
│   ├── test_drives.py
│   ├── test_metadata.py
│   ├── test_raid_write.py
│   ├── test_raid_read.py
│   ├── test_failover.py
│   ├── test_health.py
│   ├── test_rebuild.py
│   ├── test_checksum.py
│   ├── test_writer.py
│   ├── test_degraded_write.py
│   ├── test_degraded_multiple.py
│   ├── test_multi_rebuild.py
│   ├── test_rebuild_integrity.py
│   ├── test_auto_rebuild.py
│   ├── test_latency.py
│   └── test_optimized_read.py
│
└── espcode/
    └── NodeMCU ESP8266 code
```

---

# 📝 Implementation Note

The original/reference architecture of the project was designed around:

```text
ESP32
   ↓
Raspberry Pi
   ↓
Linux mdadm RAID 10
   ↓
InfluxDB
   ↓
Grafana
```

The current working prototype uses:

```text
NodeMCU ESP8266
   ↓
Windows 11 Laptop
   ↓
Python Software-Defined RAID 10
   ↓
InfluxDB
   ↓
Grafana
```

The change was made because a Raspberry Pi/Linux environment was not available within the project's hardware and budget constraints.

The current implementation is therefore an **application-level/software-defined RAID 10 prototype**, not a kernel-level `mdadm` RAID implementation.

The prototype reproduces the important RAID 10 behaviors required for demonstrating:

- Striping
- Mirroring
- Redundancy
- Fault detection
- Degraded operation
- Read failover
- Rebuild
- Resynchronization
- Data integrity verification

---

# 💽 Storage Configuration

The four physical drives currently used are approximately:

| Drive | Capacity | Filesystem |
|---|---:|---|
| D | 312.6 GB | FAT32 |
| E | 780.0 GB | NTFS |
| F | 307.5 GB | NTFS |
| G | 157.3 GB | FAT32 |

### RAID Pairing

```text
Mirror Pair 1
D ↔ E

Mirror Pair 2
F ↔ G
```

Because the drives have unequal capacities, the smallest usable member limits the effective capacity of each mirror pair.

The current implementation is primarily intended to demonstrate **RAID functionality, redundancy, failure handling, recovery, and integrity verification**, rather than maximum storage utilization.

---

# 🔐 Security

Sensitive configuration values are stored in `.env`.

Example:

```text
INFLUX_URL=http://localhost:8086
INFLUX_TOKEN=<your-token>
INFLUX_ORG=IoT-Storage
INFLUX_BUCKET=sensor-data
```

The `.env` file is excluded from Git using `.gitignore`.

> Never commit API tokens, passwords, or other secrets to the repository.

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/Shrestha-Gupta/IoT-RAID-10.git
cd IoT-RAID-10
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Main dependencies:

```text
Flask
influxdb-client
python-dotenv
```

## 3. Configure InfluxDB

Start InfluxDB locally.

Default address:

```text
http://localhost:8086
```

Create:

```text
Organization: IoT-Storage
Bucket: sensor-data
```

Configure the required credentials in `.env`.

---

# ▶️ Running the System

## Start InfluxDB

Start the local InfluxDB server and verify:

```text
http://localhost:8086
```

## Start Flask

From the project directory:

```bash
python app.py
```

The server listens on:

```text
http://0.0.0.0:5000
```

## Start NodeMCU

Upload the ESP8266 program using Arduino IDE.

Configure the Wi-Fi and server address:

```cpp
const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";
const char* serverURL = "http://YOUR_LAPTOP_IP:5000/api/data";
```

Open the Serial Monitor and verify sensor readings.

## Open Grafana

```text
http://localhost:3000
```

Open the:

```text
IoT Storage Monitoring
```

dashboard.

---

# 🧰 Useful Test Commands

Run tests from the project directory.

### RAID Write

```bash
python tests/test_raid_write.py
```

### RAID Health

```bash
python tests/test_health.py
```

### Failover

```bash
python tests/test_failover.py
```

### Automatic Rebuild

```bash
python tests/test_auto_rebuild.py
```

### Rebuild Integrity

```bash
python tests/test_rebuild_integrity.py
```

### Optimized Read

```bash
python tests/test_optimized_read.py
```

---

# ✅ Current System Status

| Component | Status |
|---|:---:|
| NodeMCU ESP8266 | ✅ Working |
| DHT11 | ✅ Working |
| HC-SR04 | ✅ Working |
| Flask Server | ✅ Working |
| Python RAID 10 | ✅ Working |
| RAID Striping | ✅ Tested |
| RAID Mirroring | ✅ Tested |
| Failure Detection | ✅ Tested |
| Degraded Mode | ✅ Tested |
| Read Failover | ✅ Tested |
| Automatic Rebuild | ✅ Tested |
| SHA-256 Verification | ✅ Tested |
| InfluxDB | ✅ Working |
| Grafana | ✅ Working |
| Real-Time Dashboard | ✅ Working |

---

# ⚠️ Current Limitations

### 1. Application-Level RAID

The current RAID implementation operates at the application/file level.

It is not a kernel-level block-device RAID implementation such as Linux `mdadm`.

### 2. Windows-Based Prototype

The current implementation runs on Windows 11 instead of the Raspberry Pi/Linux reference architecture.

### 3. USB Storage

The prototype depends on physically connected USB storage devices.

### 4. Unequal Drive Capacities

The four drives have different capacities, reducing the effective usable RAID capacity.

### 5. Laptop Dependency

The current prototype requires the Windows laptop to remain powered and connected.

### 6. Network Dependency

NodeMCU requires network connectivity to communicate with the Flask server.

### 7. Prototype Scalability

Further optimization is required before using the system as a large-scale production storage platform.

---

# 🔮 Future Scope

## Hardware & Storage

- Raspberry Pi deployment
- Linux-based implementation
- `mdadm` RAID 10 integration
- Equal-capacity storage drives
- Higher-capacity storage
- Dedicated NAS-style hardware

## Monitoring

- Dedicated RAID monitoring dashboard
- Storage usage monitoring
- Rebuild progress monitoring
- Drive health visualization
- Performance monitoring
- Automatic alerts

## Security

- User authentication
- Role-based access
- Encryption
- Secure communication
- Access logging

## IoT Expansion

- Soil moisture
- Water level
- Air quality
- Light intensity
- Pressure
- Additional environmental sensors

## Intelligence

- Sensor anomaly detection
- Predictive maintenance
- Drive failure prediction
- AI/ML-based analysis

## Connectivity

- Cloud synchronization
- Mobile application
- Remote monitoring
- Notification services

---

# 📚 Research Contribution

The project combines multiple technologies into a unified IoT storage architecture:

```text
┌───────────────────────────────┐
│       IoT Data Collection     │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│     NodeMCU ESP8266           │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│       Flask Backend           │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│  Software-Defined RAID 10     │
│                               │
│ Striping + Mirroring          │
│ Failover + Rebuild            │
│ Integrity + Health Monitoring │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│          InfluxDB             │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│           Grafana             │
│      Real-Time Monitoring     │
└───────────────────────────────┘
```

---

# 🏁 Conclusion

The developed prototype demonstrates an IoT-based data storage system combining:

- NodeMCU ESP8266
- Environmental sensors
- Flask backend
- Python software-defined RAID 10
- InfluxDB
- Grafana
- SHA-256 integrity verification

The system successfully demonstrates:

```text
Sensor Data Collection
        ↓
Wi-Fi Transmission
        ↓
Flask Processing
        ↓
RAID 10 Storage
        ↓
InfluxDB
        ↓
Grafana Visualization
```

The RAID implementation successfully demonstrates:

```text
Striping
   ↓
Mirroring
   ↓
Failure Detection
   ↓
Degraded Operation
   ↓
Read Failover
   ↓
Drive Recovery
   ↓
Automatic Rebuild
   ↓
SHA-256 Verification
   ↓
Healthy RAID
```

The physical drive failure test demonstrated that sensor data processing continues even when one RAID drive becomes unavailable.

After reconnecting the failed drive, the rebuild process successfully restored the missing data and passed integrity verification.

The project therefore provides a functional proof-of-concept for **reliable, redundant, fault-tolerant local IoT data storage with real-time monitoring**.

---

# 🔗 Repository

**GitHub:**  
https://github.com/Shrestha-Gupta/IoT-RAID-10

---

<p align="center">
  <b>IoT Data • Reliable Storage • RAID 10 • Real-Time Monitoring</b>
</p>
