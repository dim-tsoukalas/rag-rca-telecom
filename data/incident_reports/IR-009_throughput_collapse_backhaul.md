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