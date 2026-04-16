# IR-010: Throughput collapse — uplink interference

## Fault type
throughput_collapse

## Symptoms
- UL_bitrate collapses while DL_bitrate remains relatively stable
- SNR degrades on uplink
- RSRQ worsens despite stable RSRP
- CQI may drop
- Affects UEs near cell edge more severely

## Root cause
Uplink interference from external source: nearby industrial equipment,
unlicensed transmitters on adjacent bands, or a rogue UE transmitting
at excessive power. The interference raises the uplink noise floor,
reducing effective SINR for all UEs on the cell.

## Typical duration
Persistent until interference source is removed or mitigated.

## Resolution
- Spectrum scan to identify interference source frequency
- Coordinate with regulator if unlicensed transmitter found
- Adjust UL power control parameters to compensate
- Enable uplink interference rejection combining (IRC) if supported

## Related KPIs
UL_bitrate, SNR, RSRQ, CQI