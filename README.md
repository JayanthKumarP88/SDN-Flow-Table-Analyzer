# Multi-Switch Flow Table Analyzer (SDN Project 8)

## 1. Problem Statement & Objective
The objective of this project is to develop an SDN-based Flow Table Analyzer using the POX controller and Mininet. The system is designed to:
* Dynamically retrieve flow entries from multiple switches in a linear topology.
* Distinguish between **ACTIVE** and **UNUSED** rules based on real-time packet counts.
* Monitor performance metrics including Latency and Throughput.

## 2. Topology Design
We utilize a **3-Switch Linear Topology** ($s1 - s2 - s3$) with a remote controller. This setup allows us to monitor how flows are handled across multiple hops.

**Proof of Topology:**
[PLACEHOLDER: image_cae02b.png - Net and Links output]

## 3. Setup & Execution
1.  **Start the Controller:** `python3 pox.py flow_analyzer`
2.  **Start Mininet:** `sudo mn --topo linear,3 --mac --controller=remote`
3.  **Run Traffic:** `pingall` or `iperf h1 h3`

## 4. Functional Correctness & Forwarding
The controller implements a Learning Switch logic. Successful connectivity is verified via a `pingall` test with 0% packet loss.

**Connectivity Result:**
[PLACEHOLDER: image_ca6b14.png - Pingall Result]

## 5. Flow Analyzer Logic (The "Project 8" Core)
The analyzer polls the switches and prints the status of the flow tables. 

### Scenario A: Active Traffic (Learning & Forwarding)
When traffic passes through, the analyzer captures the flow entries, showing high priority rules and increasing byte counts.
[PLACEHOLDER: image_cac1a3.png - Active Flow Table]

### Scenario B: Flow Expiration (Idle Timeout)
To demonstrate dynamic flow management, we implemented an `idle_timeout` of 30 seconds. After traffic stops, the rules are removed from the switch.
[PLACEHOLDER: image_cac4f0.png - Empty Flow Table]

## 6. Performance Analysis
The project evaluates the network based on two key metrics:
* **Latency:** Average RTT measured via `ping`.
* **Throughput:** Bandwidth capacity measured via `iperf`.

**Performance Data:**
[PLACEHOLDER: image_ca6b8c.png - Ping and iperf Results]

## 7. Controller-Switch Interaction (Wireshark)
Verification of OpenFlow protocol messages, specifically `OFPT_STATS_REQUEST` and `OFPT_PACKET_IN`.
[PLACEHOLDER: image_cac92b.png - Wireshark Capture]

---
**Author:** Jayanth Kumar P  
**Course:** Electronics and Instrumentation Engineering  
**University:** PES University
