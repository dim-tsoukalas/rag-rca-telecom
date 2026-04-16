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