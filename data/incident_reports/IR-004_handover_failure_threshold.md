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