# IR-008: Throughput collapse — scheduler fault

## Fault type
throughput_collapse

## Symptoms
- DL_bitrate drops to near zero on a single cell
- RSRP, RSRQ and SNR all remain normal
- UL_bitrate also affected
- Other cells in same area unaffected
- Fault clears spontaneously or after gNB restart

## Root cause
Software fault in the gNB downlink scheduler. The scheduler stops
allocating PRBs correctly despite good radio conditions. This is a
vendor-specific software bug seen in certain gNB software versions
under high load or after long uptime periods.

## Typical duration
15 minutes to several hours. Clears on gNB restart.

## Resolution
- Remote restart of gNB baseband unit
- Upgrade to patched gNB software version
- Monitor gNB uptime — schedule preventive restarts if bug is known
- Capture gNB logs before restart for vendor RCA

## Related KPIs
DL_bitrate, UL_bitrate, RSRP, CellID