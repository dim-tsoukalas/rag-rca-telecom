# src/generate_incident_reports.py
import os

OUT_DIR = "data/incident_reports"
os.makedirs(OUT_DIR, exist_ok=True)

reports = {

"IR-001_rsrp_drop_coverage_hole.md": """
# IR-001: RSRP drop — coverage hole

## Fault type
rsrp_drop

## Symptoms
- RSRP falls below -110 dBm sustained for more than 30 seconds
- RSRQ degrades below -16 dB simultaneously
- SNR drops below 2 dB
- DL bitrate collapses to near zero (under 50 kbps)
- UE remains camped on cell but throughput is unusable

## Root cause
Coverage hole caused by insufficient overlap between adjacent cells.
The UE moves into a geographic area where no cell provides adequate
signal strength. This is common in driving scenarios near cell edge.

## Typical duration
30–120 seconds depending on UE mobility speed.

## Resolution
- RF optimization: antenna tilt adjustment on adjacent cells
- Add small cell or repeater to fill coverage gap
- Adjust handover thresholds to trigger earlier cell reselection
- Check for physical obstructions (new buildings, terrain changes)

## Related KPIs
RSRP, RSRQ, SNR, DL_bitrate
""",

"IR-002_rsrp_drop_pilot_pollution.md": """
# IR-002: RSRP drop — pilot pollution

## Fault type
rsrp_drop

## Symptoms
- RSRP is moderate (-90 to -100 dBm) but RSRQ is very poor (below -15 dB)
- SNR is low despite adequate RSRP
- Frequent CellID changes as UE cannot lock onto dominant cell
- DL bitrate unstable, oscillating between high and near-zero

## Root cause
Pilot pollution: multiple cells with similar signal strength compete
for the UE. No single dominant server exists. The UE receives
interference from several cells rather than clean signal from one.
Common after new site additions without proper PCI/antenna planning.

## Typical duration
Persistent until RF reoptimization is performed.

## Resolution
- Antenna downtilt on over-shooting cells
- Power reduction on interfering cells
- PCI replan to reduce confusion between neighboring cells
- Add neighbor cell relations in SON (Self-Organizing Network)

## Related KPIs
RSRP, RSRQ, SNR, CellID, CQI
""",

"IR-003_rsrp_drop_hardware_fault.md": """
# IR-003: RSRP drop — hardware fault at gNB

## Fault type
rsrp_drop

## Symptoms
- Sudden RSRP drop to below -115 dBm with no prior degradation
- Affects all UEs on same CellID simultaneously
- RSRQ and SNR also collapse
- DL and UL bitrate both drop to zero
- NRxRSRP also shows extreme degradation

## Root cause
Hardware failure at the gNB: typically a faulty radio unit (RU),
broken antenna connector, or AISG cable fault. Unlike coverage holes,
this fault is sudden and affects all users on the cell simultaneously.

## Typical duration
Until field engineer replaces or resets faulty hardware unit.

## Resolution
- Remote reset of radio unit via O&M interface
- Field inspection of antenna connector and feeder cable
- Replace faulty RU if reset does not restore performance
- Check alarm log for hardware-related alarms (VSWR, TX power)

## Related KPIs
RSRP, NRxRSRP, RSRQ, DL_bitrate, UL_bitrate
""",

"IR-004_handover_failure_threshold.md": """
# IR-004: Handover failure — misconfigured A3 threshold

## Fault type
handover_failure

## Symptoms
- CellID changes rapidly (flapping) between two cells
- DL_bitrate drops to zero during transition window (10–30 seconds)
- RSRP of serving cell is marginal (-105 to -112 dBm) when failure occurs
- UE reconnects to same or different cell after failure
- PINGAVG spikes dramatically during failure window

## Root cause
A3 event offset threshold misconfigured: handover is triggered too
late (UE already at cell edge) or too early (target cell not yet
strong enough). The UE initiates handover but loses connection before
the target cell confirms RRC reconfiguration complete.

## Typical duration
10–45 seconds per failure event. May recur if threshold not corrected.

## Resolution
- Adjust A3 offset parameter in RRC configuration
- Reduce time-to-trigger (TTT) value for faster handover initiation
- Verify target cell RACH configuration is reachable from source
- Enable MLB (Mobility Load Balancing) in SON

## Related KPIs
CellID, RSRP, DL_bitrate, UL_bitrate
""",

"IR-005_handover_failure_x2_interface.md": """
# IR-005: Handover failure — X2 interface failure

## Fault type
handover_failure

## Symptoms
- DL_bitrate and UL_bitrate both drop to zero for 15–60 seconds
- CellID changes but traffic does not recover on target cell
- UE falls back to source cell or triggers RRC re-establishment
- Pattern repeats consistently between same cell pair

## Root cause
X2 interface failure between source and target gNB. The handover
preparation message cannot be delivered, causing the procedure to
time out. May be caused by transport network issues, IP misconfiguration,
or gNB software fault.

## Typical duration
Persistent between affected cell pair until X2 is restored.

## Resolution
- Check X2 link status in O&M system
- Verify IP routing between gNB nodes
- Restart X2 interface on affected gNBs
- Fall back to S1-based handover as temporary measure
- Escalate to transport team if IP path is broken

## Related KPIs
CellID, DL_bitrate, UL_bitrate, PINGAVG, PINGLOSS
""",

"IR-006_handover_failure_rach.md": """
# IR-006: Handover failure — RACH failure on target cell

## Fault type
handover_failure

## Symptoms
- Handover is initiated (CellID changes in log)
- DL_bitrate collapses to zero immediately after CellID change
- UE cannot complete random access on target cell
- RRC re-establishment observed — UE reconnects to source cell
- RSRP of target cell appears adequate in logs

## Root cause
Random Access Channel (RACH) failure on target cell. The target cell
is reachable in terms of signal but the RACH preamble is not received
correctly. Causes include RACH congestion, misconfigured preamble
sequences, or timing advance issues in high-speed driving scenarios.

## Typical duration
5–20 seconds per event. Recurs at same geographic location.

## Resolution
- Increase RACH preamble power ramping step
- Add dedicated RACH resources for handover UEs
- Check target cell load — RACH congestion under high traffic
- Verify timing advance parameters for high-speed scenarios

## Related KPIs
CellID, DL_bitrate, RSRP, Speed
""",

"IR-007_throughput_collapse_congestion.md": """
# IR-007: Throughput collapse — cell congestion

## Fault type
throughput_collapse

## Symptoms
- DL_bitrate collapses below 30 kbps despite RSRP being normal (-70 to -85 dBm)
- UL_bitrate also drops significantly
- SNR and RSRQ remain acceptable
- CQI may be high (good channel) but throughput is still low
- Affects multiple UEs on same CellID simultaneously

## Root cause
Cell congestion: too many active UEs competing for limited PRB
(Physical Resource Block) resources. The scheduler cannot allocate
sufficient resources to each UE. Common during peak hours or
at dense urban locations (stadiums, transport hubs).

## Typical duration
Minutes to hours depending on traffic pattern.

## Resolution
- Enable carrier aggregation if additional spectrum available
- Offload traffic to adjacent cells via MLB
- Add small cell to absorb hotspot traffic
- Check if a single UE is consuming excessive PRBs (greedy UE)
- Schedule capacity upgrade if sustained over multiple days

## Related KPIs
DL_bitrate, UL_bitrate, CQI, RSRP, CellID
""",

"IR-008_throughput_collapse_scheduler.md": """
# IR-008: Throughput collapse — scheduler fault

## Fault type
throughput_collapse

## Symptoms
- DL_bitrate drops to near zero on a single cell
- RSRP, RSRQ and SNR all remain normal
- UL_bitrate also affected
- Other cells in same area unaffected
- Fault clears spontaneously or after gNB restart

## Root cause
Software fault in the gNB downlink scheduler. The scheduler stops
allocating PRBs correctly despite good radio conditions. This is a
vendor-specific software bug seen in certain gNB software versions
under high load or after long uptime periods.

## Typical duration
15 minutes to several hours. Clears on gNB restart.

## Resolution
- Remote restart of gNB baseband unit
- Upgrade to patched gNB software version
- Monitor gNB uptime — schedule preventive restarts if bug is known
- Capture gNB logs before restart for vendor RCA

## Related KPIs
DL_bitrate, UL_bitrate, RSRP, CellID
""",

"IR-009_throughput_collapse_backhaul.md": """
# IR-009: Throughput collapse — backhaul congestion

## Fault type
throughput_collapse

## Symptoms
- DL_bitrate collapses across multiple cells in same area
- RSRP and radio KPIs remain healthy
- PINGAVG and PINGMAX increase significantly (latency spike)
- PINGLOSS may increase
- UL_bitrate also affected

## Root cause
Backhaul link congestion between gNB and core network. The radio
interface is healthy but the IP transport carrying user traffic
is saturated. Common with microwave backhaul links or shared
fiber links serving multiple gNBs.

## Typical duration
Minutes to hours depending on traffic load.

## Resolution
- Check backhaul link utilization on transport team dashboard
- Enable QoS prioritization for RAN traffic on backhaul
- Add capacity to congested backhaul link
- Reroute traffic via alternate backhaul path if available

## Related KPIs
DL_bitrate, UL_bitrate, PINGAVG, PINGMAX, PINGLOSS
""",

"IR-010_throughput_collapse_interference.md": """
# IR-010: Throughput collapse — uplink interference

## Fault type
throughput_collapse

## Symptoms
- UL_bitrate collapses while DL_bitrate remains relatively stable
- SNR degrades on uplink
- RSRQ worsens despite stable RSRP
- CQI may drop
- Affects UEs near cell edge more severely

## Root cause
Uplink interference from external source: nearby industrial equipment,
unlicensed transmitters on adjacent bands, or a rogue UE transmitting
at excessive power. The interference raises the uplink noise floor,
reducing effective SINR for all UEs on the cell.

## Typical duration
Persistent until interference source is removed or mitigated.

## Resolution
- Spectrum scan to identify interference source frequency
- Coordinate with regulator if unlicensed transmitter found
- Adjust UL power control parameters to compensate
- Enable uplink interference rejection combining (IRC) if supported

## Related KPIs
UL_bitrate, SNR, RSRQ, CQI
""",

"IR-011_combined_rsrp_handover.md": """
# IR-011: Combined RSRP degradation leading to handover failure

## Fault type
rsrp_drop, handover_failure

## Symptoms
- Initial RSRP drop below -108 dBm as UE moves toward cell edge
- Handover attempt triggered but fails (DL_bitrate = 0 for 20+ seconds)
- CellID flap observed mid-failure
- UE eventually recovers on new cell with improved RSRP
- Total service interruption: 30–90 seconds

## Root cause
Coverage gap between two cells forces a late handover. By the time
the A3 event fires, the UE is already at very poor RSRP. The handover
fails due to insufficient signal on both source and target cells
during the transition window.

## Typical duration
30–90 seconds total service interruption.

## Resolution
- Reduce A3 TTT to trigger handover earlier while RSRP is still viable
- Improve coverage overlap between the two cells
- Add an intermediate small cell if geographic gap is too large

## Related KPIs
RSRP, CellID, DL_bitrate, UL_bitrate
""",

"IR-012_driving_coverage_pattern.md": """
# IR-012: Recurring coverage degradation in driving scenario

## Fault type
rsrp_drop

## Symptoms
- RSRP drops are correlated with specific geographic coordinates
- Degradation repeats consistently at same location across multiple drive sessions
- Speed is typically above 40 km/h during events
- NRxRSRP confirms degradation (not a measurement artifact)

## Root cause
Permanent coverage gap at a specific road segment. Terrain, buildings,
or highway geometry creates a consistent blind spot. The high UE speed
(40–60 km/h) means the gap is traversed quickly but causes repeated
handover stress.

## Typical duration
5–20 seconds per pass through the affected road segment.

## Resolution
- Site survey at affected GPS coordinates
- Deploy lamp-post small cell or roadside RRH
- Adjust antenna azimuth on nearest macro cell toward road segment

## Related KPIs
RSRP, NRxRSRP, Latitude, Longitude, Speed
""",

"IR-013_static_scenario_congestion.md": """
# IR-013: Throughput collapse in static UE scenario

## Fault type
throughput_collapse

## Symptoms
- UE is stationary (Speed = 0), RSRP is strong (-70 to -80 dBm)
- DL_bitrate repeatedly collapses to near zero in bursts
- Pattern is periodic, suggesting a scheduling or interference cycle
- CQI is high but throughput does not match

## Root cause
In static scenarios, the UE is often indoors or near a window.
Throughput collapse with good RSRP and high CQI indicates a
scheduling problem or competing traffic from other UEs on same cell.
May also indicate TDD uplink/downlink configuration mismatch.

## Typical duration
Intermittent bursts of 10–30 seconds.

## Resolution
- Check TDD configuration on serving cell
- Monitor PRB utilization per cell for congestion patterns
- Verify UE category and CA configuration
- Check for interference from co-located WiFi on same frequency band

## Related KPIs
DL_bitrate, RSRP, CQI, Speed, CellID
""",

"IR-014_nrxrsrp_degradation.md": """
# IR-014: NRxRSRP degradation without RSRP change

## Fault type
rsrp_drop

## Symptoms
- NRxRSRP drops significantly (below -110 dBm)
- Primary RSRP remains at normal levels (-80 to -95 dBm)
- RSRQ worsens while RSRP stays stable
- DL_bitrate may degrade moderately

## Root cause
Degradation specific to the neighbor cell reference signal (NRxRSRP).
The primary serving cell is healthy but the strongest neighbor cell
is experiencing issues. This can indicate a fault on a neighboring
gNB that the UE would normally hand over to. If uncorrected, future
handovers into that neighbor will fail.

## Typical duration
Persistent until neighbor cell issue is resolved.

## Resolution
- Investigate alarms on the neighbor cell identified in CELLHEX/NODEHEX
- Check neighbor cell hardware and software status
- Temporarily remove the degraded cell from neighbor relations
- Restore neighbor relation after fault clearance

## Related KPIs
NRxRSRP, NRxRSRQ, RSRQ, CELLHEX, NODEHEX
""",

"IR-015_multi_kpi_degradation.md": """
# IR-015: Multi-KPI simultaneous degradation

## Fault type
rsrp_drop, throughput_collapse

## Symptoms
- RSRP, RSRQ, SNR, DL_bitrate and UL_bitrate all degrade simultaneously
- Degradation is sudden rather than gradual
- Affects a single CellID
- CQI also drops
- No handover occurs despite poor conditions

## Root cause
Catastrophic cell degradation, typically caused by a hardware fault
at the gNB combined with a failed handover. The UE remains camped on
a severely degraded cell because the handover mechanism is also
impaired. This is the most severe fault type and results in complete
service loss for the UE.

## Typical duration
Until UE performs RRC re-establishment or UE moves out of cell range.

## Resolution
- Immediate escalation to NOC (Network Operations Center)
- Remote gNB reset as first step
- Field engineer dispatch if remote reset fails
- Check all hardware alarms: RU, BBU, transport, power
- Force UE reattachment via paging if reset restores cell

## Related KPIs
RSRP, RSRQ, SNR, CQI, DL_bitrate, UL_bitrate, CellID
""",

}

for filename, content in reports.items():
    fpath = os.path.join(OUT_DIR, filename)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"Written: {filename}")

print(f"\nAll {len(reports)} incident reports saved to {OUT_DIR}/")