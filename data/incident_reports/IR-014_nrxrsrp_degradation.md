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