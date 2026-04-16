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