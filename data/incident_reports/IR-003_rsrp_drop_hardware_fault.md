# IR-003: RSRP drop — hardware fault at gNB

## Fault type
rsrp_drop

## Symptoms
- Sudden RSRP drop to below -115 dBm with no prior degradation
- Affects all UEs on same CellID simultaneously
- RSRQ and SNR also collapse
- DL and UL bitrate both drop to zero
- NRxRSRP also shows extreme degradation

## Root cause
Hardware failure at the gNB: typically a faulty radio unit (RU),
broken antenna connector, or AISG cable fault. Unlike coverage holes,
this fault is sudden and affects all users on the cell simultaneously.

## Typical duration
Until field engineer replaces or resets faulty hardware unit.

## Resolution
- Remote reset of radio unit via O&M interface
- Field inspection of antenna connector and feeder cable
- Replace faulty RU if reset does not restore performance
- Check alarm log for hardware-related alarms (VSWR, TX power)

## Related KPIs
RSRP, NRxRSRP, RSRQ, DL_bitrate, UL_bitrate