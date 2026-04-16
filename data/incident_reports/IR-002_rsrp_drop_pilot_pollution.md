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