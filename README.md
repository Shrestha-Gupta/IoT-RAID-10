\# IoT-Based Data Storage System using Software-Defined RAID 10



\## Project Overview



This project presents an IoT-based data storage and real-time monitoring system designed to provide reliable local data storage with redundancy, fault tolerance, and real-time visualization.



The system collects environmental data using sensors connected to a NodeMCU ESP8266. The sensor data is transmitted over Wi-Fi to a Flask-based server running on a Windows 11 laptop.



The server implements a Python-based software-defined RAID 10 prototype providing data striping, mirroring, drive failure detection, degraded operation, read failover, rebuild/resynchronization, SHA-256 integrity verification, and drive health monitoring.



Sensor data is also stored in InfluxDB and visualized using Grafana.



\---



\## System Architecture



DHT11

HC-SR04

Soil Moisture Sensor

&#x20;       |

&#x20;       v

NodeMCU ESP8266

&#x20;       |

&#x20;       | Wi-Fi / HTTP POST

&#x20;       v

Flask Server

&#x20;       |

&#x20;       +----------------------+

&#x20;       |                      |

&#x20;       v                      v

Software-Defined RAID 10     InfluxDB

&#x20;       |                      |

&#x20;       |                      v

&#x20;       |                   Grafana

&#x20;       |

&#x20;       +-- Mirror Pair 1: D <-> E

&#x20;       |

&#x20;       +-- Mirror Pair 2: F <-> G



\---



\## Hardware Used



1\. NodeMCU ESP8266

2\. DHT11 Temperature and Humidity Sensor

3\. HC-SR04 Ultrasonic Sensor

4\. Soil Moisture Sensor

5\. Four USB storage drives

6\. Windows 11 laptop



\### Current Sensor Status



DHT11:

Working and tested successfully.



HC-SR04:

Working and tested successfully.



Soil Moisture Sensor:

Hardware available. Integration is pending.



Water Level Sensor:

Removed from the current implementation.



\---



\## Software Used



1\. Python

2\. Flask

3\. InfluxDB

4\. Grafana

5\. Arduino IDE

6\. ESP8266 Arduino Libraries

7\. Git

8\. GitHub



\---



\## RAID 10 Configuration



The prototype uses four separate USB storage drives.



The drives are configured into two mirror pairs:



D <----> E



F <----> G



Stripe allocation alternates between these mirror pairs:



Stripe 0 -> D/E

Stripe 1 -> F/G

Stripe 2 -> D/E

Stripe 3 -> F/G



This implementation demonstrates the core RAID 10 concepts of:



1\. Striping

2\. Mirroring

3\. Redundancy

4\. Fault tolerance



\---



\## RAID Features Implemented



\### 1. Data Mirroring



The same data is written to both drives belonging to a mirror pair.



\### 2. Data Striping



Logical stripe allocation alternates between the two mirror pairs.



\### 3. Drive Failure Detection



The system checks the availability of the configured drives.



Drive states include:



ONLINE



OFFLINE



\### 4. Degraded Mode



If one drive in a mirror pair becomes unavailable, the surviving drive continues serving the data.



\### 5. Read Failover



When both drives of a mirror pair are available, the system can select the faster available drive.



If the selected drive fails, the other mirror member can be used.



\### 6. Rebuild and Resynchronization



When a failed drive becomes available again, missing data can be rebuilt from its surviving mirror member.



\### 7. SHA-256 Integrity Verification



SHA-256 checksums are used to verify that rebuilt data matches the source data.



\### 8. Drive Health Monitoring



The system continuously checks the state of the configured storage drives and determines the overall RAID state.



Possible RAID states include:



HEALTHY



DEGRADED



REBUILDING



FAILED



\---



\## IoT Data Flow



The current data flow is:



Sensor

&#x20;   |

&#x20;   v

NodeMCU ESP8266

&#x20;   |

&#x20;   | Wi-Fi

&#x20;   v

HTTP POST

&#x20;   |

&#x20;   v

Flask Server

&#x20;   |

&#x20;   +------------------> InfluxDB

&#x20;   |                       |

&#x20;   |                       v

&#x20;   |                    Grafana

&#x20;   |

&#x20;   v

Software-Defined RAID 10



The NodeMCU currently sends sensor readings approximately every 5 seconds.



\---



\## Flask Server



The Flask server acts as the central processing layer.



It receives sensor data from the NodeMCU through an HTTP POST request.



Main API endpoints:



POST /api/data



Used to receive sensor readings.



GET /api/status



Used to check the current RAID and drive status.



The server processes the received sensor data and performs two storage operations:



1\. Stores sensor measurements in InfluxDB.

2\. Stores the corresponding data through the software-defined RAID 10 layer.



\---



\## InfluxDB



InfluxDB is used as the time-series database for sensor measurements.



The following sensor fields are stored:



1\. Temperature

2\. Humidity

3\. Distance



The current InfluxDB configuration uses:



Organization:

IoT-Storage



Bucket:

sensor-data



InfluxDB is responsible for maintaining the time-series sensor measurements used by Grafana.



\---



\## Grafana



Grafana is used for real-time visualization of the sensor data stored in InfluxDB.



The current dashboard is named:



IoT Storage Monitoring



The dashboard contains three main visualizations:



1\. Temperature

2\. Humidity

3\. Distance



The dashboard successfully displays live sensor data.



\---



\## Live Hardware Test



A successful live hardware test produced the following values:



Temperature: 27.20 °C



Humidity: 77.60 %



Distance: 36.31 cm



HTTP Response Code: 200



InfluxDB Status: success



RAID Status: HEALTHY



Mirror Pair: F/G



The sensor data was successfully received by the Flask server, stored in InfluxDB, and visualized through Grafana.



\---



\## RAID Failure Test



A physical drive was temporarily disconnected while the system was running.



\### Initial State



D -> ONLINE

E -> ONLINE

F -> ONLINE

G -> ONLINE



RAID Status -> HEALTHY



\### Failure Condition



Drive D was disconnected.



New state:



D -> OFFLINE

E -> ONLINE

F -> ONLINE

G -> ONLINE



RAID Status -> DEGRADED



The system continued receiving sensor data while drive D was unavailable.



The surviving mirror member E continued handling the data.



This demonstrated degraded-mode operation and mirror-based fault tolerance.



\---



\## RAID Recovery Test



After reconnecting drive D, the rebuild process was executed.



The rebuild process:



1\. Detected the previously failed drive.

2\. Identified the surviving mirror member.

3\. Copied the required stripe data from the surviving drive.

4\. Rebuilt the missing data.

5\. Verified the rebuilt files.

6\. Performed SHA-256 integrity verification.

7\. Restored the RAID state to HEALTHY.



The automatic rebuild test completed successfully.



The rebuild integrity verification test also completed successfully.



\---



\## Automated Tests



The project contains multiple automated tests for the RAID subsystem.



The implemented tests include:



test\_drives.py

test\_metadata.py

test\_raid\_write.py

test\_raid\_read.py

test\_failover.py

test\_health.py

test\_rebuild.py

test\_checksum.py

test\_writer.py

test\_degraded\_write.py

test\_degraded\_multiple.py

test\_multi\_rebuild.py

test\_rebuild\_integrity.py

test\_auto\_rebuild.py

test\_latency.py

test\_optimized\_read.py



These tests cover:



1\. Drive detection

2\. Metadata management

3\. RAID writing

4\. RAID reading

5\. Failover

6\. Drive health monitoring

7\. Degraded operation

8\. Rebuild

9\. Multiple-stripe rebuild

10\. SHA-256 integrity verification

11\. Automatic rebuild

12\. Drive latency measurement

13\. Optimized read selection



\---



\## Project Structure



IoT-RAID-10/

|

|-- app.py

|-- influx.py

|-- requirements.txt

|-- .gitignore

|

|-- raid/

|   |-- \_\_init\_\_.py

|   |-- config.py

|   |-- drive.py

|   |-- metadata.py

|   |-- stripe.py

|   |-- mirror.py

|   |-- writer.py

|   |-- reader.py

|   |-- checksum.py

|   |-- health.py

|   |-- rebuild.py

|   |-- rebuild\_manager.py

|   |-- status.py

|

|-- tests/

|   |-- test\_drives.py

|   |-- test\_metadata.py

|   |-- test\_raid\_write.py

|   |-- test\_raid\_read.py

|   |-- test\_failover.py

|   |-- test\_health.py

|   |-- test\_rebuild.py

|   |-- test\_checksum.py

|   |-- test\_writer.py

|   |-- test\_degraded\_write.py

|   |-- test\_degraded\_multiple.py

|   |-- test\_multi\_rebuild.py

|   |-- test\_rebuild\_integrity.py

|   |-- test\_auto\_rebuild.py

|   |-- test\_latency.py

|   |-- test\_optimized\_read.py

|

|-- espcode/



\---



\## Prototype Implementation



The original proposed architecture of the project uses a Raspberry Pi with software RAID 10.



Due to hardware availability and cost constraints, the current working prototype is implemented on a Windows 11 laptop using Python.



Therefore, the current implementation is described as:



Python-Based Software-Defined RAID 10 Prototype



The prototype implements the core RAID 10 concepts at the application level rather than using Linux kernel-level RAID tools such as mdadm.



The implementation focuses on:



1\. Striping

2\. Mirroring

3\. Fault detection

4\. Degraded operation

5\. Read failover

6\. Rebuild and recovery

7\. Data integrity verification

8\. Drive health monitoring



\---



\## Storage Configuration



The current prototype uses four separate USB storage drives.



The logical mirror configuration is:



D <----> E



F <----> G



The physical drives have different storage capacities.



Therefore, the current implementation is primarily intended for functional and research validation rather than maximum storage utilization.



\---



\## Important Architecture Difference



Reference architecture:



ESP32

&#x20;   |

&#x20;   v

Raspberry Pi

&#x20;   |

&#x20;   v

Linux mdadm RAID 10

&#x20;   |

&#x20;   v

InfluxDB

&#x20;   |

&#x20;   v

Grafana



Current prototype:



NodeMCU ESP8266

&#x20;   |

&#x20;   v

Windows 11 Laptop

&#x20;   |

&#x20;   v

Python Software-Defined RAID 10

&#x20;   |

&#x20;   v

InfluxDB

&#x20;   |

&#x20;   v

Grafana



The current implementation does not claim to be Linux kernel-level mdadm RAID.



It is an application-level software-defined RAID 10 prototype developed to demonstrate the core concepts and behavior of RAID 10 in a low-cost environment.



\---



\## Current Limitations



1\. The current RAID implementation is application-level rather than block-device/kernel-level RAID.

2\. The prototype uses USB storage drives.

3\. The storage drives have different capacities.

4\. Soil moisture sensor integration is pending.

5\. The current implementation is intended for research and proof-of-concept validation.

6\. The prototype does not replace Linux mdadm-based RAID.

7\. The current implementation is designed for functional validation of RAID 10 concepts rather than production-grade storage deployment.



\---



\## Security and Configuration



Sensitive configuration values such as the InfluxDB authentication token are stored in a local .env file.



The .env file is excluded from Git tracking using .gitignore.



Therefore, private credentials are not included in the GitHub repository.



\---



\## Installation



Clone the repository:



git clone https://github.com/Shrestha-Gupta/IoT-RAID-10.git



Move into the project directory:



cd IoT-RAID-10



Install the required Python packages:



pip install -r requirements.txt



Configure the local InfluxDB connection using the .env file.



\---



\## Running the Project



Start the Flask server:



python app.py



The Flask server runs on:



http://localhost:5000



The main sensor-data endpoint is:



POST /api/data



The system status endpoint is:



GET /api/status



The NodeMCU sends sensor readings to the Flask server over Wi-Fi.



\---



\## Monitoring



The complete monitoring pipeline is:



NodeMCU

&#x20;   |

&#x20;   v

Flask Server

&#x20;   |

&#x20;   v

InfluxDB

&#x20;   |

&#x20;   v

Grafana



Grafana provides real-time visualization of:



1\. Temperature

2\. Humidity

3\. Distance



The RAID subsystem independently manages redundant local storage.



\---



\## GitHub Repository



The project source code, RAID implementation, automated tests, requirements file, and documentation are maintained in the GitHub repository.



Repository:



https://github.com/Shrestha-Gupta/IoT-RAID-10



Sensitive files such as .env are excluded from the repository.



The local InfluxDB installation is also not included in the repository because the InfluxDB executable exceeds GitHub's standard individual file size limit.



\---



\## Future Scope



The project can be extended in the following areas:



1\. Raspberry Pi deployment

2\. Linux mdadm-based RAID 10

3\. Larger dedicated storage drives

4\. Cloud backup

5\. Mobile monitoring application

6\. Additional IoT sensors

7\. Improved authentication and security

8\. Automatic periodic drive health monitoring

9\. Remote alerts and notifications

10\. Storage capacity monitoring

11\. Advanced storage analytics

12\. AI/ML-based anomaly detection

13\. Industrial deployment



\---



\## Conclusion



The prototype successfully demonstrates an IoT-based data storage and real-time monitoring system using a Python-based software-defined RAID 10 approach.



The implemented system successfully demonstrates:



1\. IoT sensor data acquisition

2\. NodeMCU ESP8266-based data transmission

3\. Wi-Fi communication

4\. Flask server processing

5\. RAID 10 striping and mirroring

6\. Drive failure detection

7\. Degraded operation

8\. Read failover

9\. Automatic rebuild

10\. SHA-256 integrity verification

11\. InfluxDB time-series storage

12\. Grafana real-time visualization



The successful drive failure, degraded-mode, rebuild, and integrity verification tests demonstrate the feasibility of combining IoT monitoring with redundant local storage in a low-cost prototype environment.

