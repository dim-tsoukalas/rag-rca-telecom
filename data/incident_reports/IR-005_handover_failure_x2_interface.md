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