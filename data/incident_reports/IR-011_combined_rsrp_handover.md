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