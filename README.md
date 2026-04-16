# Multi-Switch Flow Table Analyzer (SDN Project 8)

## 1. Problem Statement & Objective
The goal of this project is to implement an SDN-based solution using the POX controller and Mininet to retrieve and analyze flow entries from multiple switches. The system dynamically identifies whether rules are **ACTIVE** (routing traffic) or **UNUSED** based on real-time packet/byte counts.

## 2. Topology Design & Setup
This project utilizes a **3-Switch Linear Topology** ($s1 - s2 - s3$) with a remote controller. This multi-hop setup is essential for validating how flow rules are installed and monitored across different paths.

**Topology Verification:**
The `net` and `links` commands verify the physical mapping of hosts and switches.
![Topology Verification](screenshots/Screenshot%202026-04-16%20232133.png)

## 3. Setup & Execution
1. **Controller Initialization:**
   Launch POX with the `flow_analyzer` module.
   ![Controller Startup](screenshots/Screenshot%202026-04-16%20230607.png)

2. **Mininet Initialization:**
   Start the linear topology and connect to the remote controller.
   ![Mininet Startup](screenshots/Screenshot%202026-04-16%20230339.png)

## 4. Functional Correctness
Connectivity is verified using `pingall`, ensuring the controller's Learning Switch logic correctly handles `packet_in` events.
![Pingall Result](screenshots/Screenshot%202026-04-16%20230356.png)

## 5. Flow Analyzer Logic (The "Project 8" Core)
The analyzer polls the switches and displays the real-time state of the flow tables.

### Scenario A: Active Traffic Monitoring
When traffic is active, the analyzer identifies rules as **ACTIVE**, displaying priority and increasing packet/byte counts.
![Active Flow Table](screenshots/Screenshot%202026-04-16%20230730.png)

### Scenario B: Flow Expiration (Idle Timeout)
To demonstrate dynamic management, an `idle_timeout` of 30s was implemented. After traffic ceases, the rules are purged, returning the status to **EMPTY**.
![Empty Flow Table](screenshots/Screenshot%202026-04-16%20230705.png)

## 6. Performance Observation & Analysis
Network performance was measured using standard metrics:
* **Latency:** Average RTT measured via `ping` (~0.293 ms).
* **Throughput:** Stress tested via `iperf`, resulting in high byte-count capture in the analyzer.

![Ping Latency](screenshots/Screenshot%202026-04-16%20230428.png)
![High Throughput Monitoring](screenshots/Screenshot%202026-04-16%20230809.png)

## 7. Protocol Interaction (Wireshark)
Wireshark captures confirm the OpenFlow 1.0 protocol exchanges, including `OFPT_PACKET_IN` and `OFPT_STATS_REQUEST`.
![Wireshark Capture](screenshots/Screenshot%202026-04-16%20231055.png)

---
**Submitted By:** Jayanth Kumar P  
**SRN:** PES1UG24CS199  
**Degree:** Electronics and Instrumentation Engineering  
**University:** PES University
