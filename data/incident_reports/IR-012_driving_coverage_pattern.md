# IR-012: Recurring coverage degradation in driving scenario

## Fault type
rsrp_drop

## Symptoms
- RSRP drops are correlated with specific geographic coordinates
- Degradation repeats consistently at same location across multiple drive sessions
- Speed is typically above 40 km/h during events
- NRxRSRP confirms degradation (not a measurement artifact)

## Root cause
Permanent coverage gap at a specific road segment. Terrain, buildings,
or highway geometry creates a consistent blind spot. The high UE speed
(40–60 km/h) means the gap is traversed quickly but causes repeated
handover stress.

## Typical duration
5–20 seconds per pass through the affected road segment.

## Resolution
- Site survey at affected GPS coordinates
- Deploy lamp-post small cell or roadside RRH
- Adjust antenna azimuth on nearest macro cell toward road segment

## Related KPIs
RSRP, NRxRSRP, Latitude, Longitude, Speed