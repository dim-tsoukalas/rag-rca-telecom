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