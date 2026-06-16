# Data Card - Economic Data

## Purpose

The economic data contains processed Womply activity measures and geography reference files from the Economic Tracker-derived pipeline. It is used to teach economic outcome construction, joins, baselines, and statistical testing.

## Key Files

| File | Rows | Columns | Description |
| --- | ---: | ---: | --- |
| `data/processed/economic/womply_city_weekly.csv` | 5,777 | 8 | City-level weekly Womply outcomes. |
| `data/processed/economic/womply_county_weekly.csv` | 81,968 | 9 | County-level weekly Womply outcomes. |
| `data/processed/economic/womply_state_weekly.csv` | 5,559 | 19 | State-level weekly Womply outcomes. |
| `data/processed/economic/womply_national_weekly.csv` | 109 | 23 | National weekly Womply outcomes. |
| `data/processed/us/economic/womply_county_weekly.csv` | 81,968 | 9 | U.S. county Womply outcomes used by county/CBSA joins. |
| `data/processed/economic/geoid_county.csv` | 3,142 | 12 | County geography lookup. |
| `data/processed/us/county_cbsa_crosswalk_us.csv` | 1,915 | 9 | County-to-CBSA crosswalk for market aggregation. |

## Important Columns

- `week_start_monday`: normalized analysis week.
- `countyfips`: county FIPS identifier.
- `cityid`: Economic Tracker city identifier.
- `merchants_all`: Womply merchant activity measure.
- `revenue_all`: Womply revenue activity measure.
- `statefips`: state FIPS identifier.
- `countyname`, `statename`, `stateabbrev`: geography labels.

## Teaching Uses

- define economic outcomes
- join event exposure to weekly county outcomes
- create rolling baselines
- discuss why relative measures need careful interpretation
- compare city, county, CBSA, state, and national aggregation levels

## Limitations

- Womply measures are relative activity indicators, not complete GDP or official tax receipts.
- Economic activity can change because of many factors unrelated to sports.
- The data covers a specific historical period and should not be generalized without checking coverage.
- Aggregation from county to CBSA can smooth or hide local effects.

## Responsible Interpretation

Use:

```text
Womply activity is higher/lower in this comparison.
```

Avoid:

```text
The local economy increased because of the event.
```
