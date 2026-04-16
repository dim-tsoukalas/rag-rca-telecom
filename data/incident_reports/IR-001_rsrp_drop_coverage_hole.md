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