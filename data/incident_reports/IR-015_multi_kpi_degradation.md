# IR-015: Multi-KPI simultaneous degradation

## Fault type
rsrp_drop, throughput_collapse

## Symptoms
- RSRP, RSRQ, SNR, DL_bitrate and UL_bitrate all degrade simultaneously
- Degradation is sudden rather than gradual
- Affects a single CellID
- CQI also drops
- No handover occurs despite poor conditions

## Root cause
Catastrophic cell degradation, typically caused by a hardware fault
at the gNB combined with a failed handover. The UE remains camped on
a severely degraded cell because the handover mechanism is also
impaired. This is the most severe fault type and results in complete
service loss for the UE.

## Typical duration
Until UE performs RRC re-establishment or UE moves out of cell range.

## Resolution
- Immediate escalation to NOC (Network Operations Center)
- Remote gNB reset as first step
- Field engineer dispatch if remote reset fails
- Check all hardware alarms: RU, BBU, transport, power
- Force UE reattachment via paging if reset restores cell

## Related KPIs
RSRP, RSRQ, SNR, CQI, DL_bitrate, UL_bitrate, CellID