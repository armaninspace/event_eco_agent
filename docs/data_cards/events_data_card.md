# Data Card - Sports Event Data

## Purpose

The sports event data describes professional sports games and derived event exposure by geography-week. It is used to teach event normalization, geographic enrichment, exposure features, and downstream statistical testing.

## Key Files

| File | Rows | Columns | Description |
| --- | ---: | ---: | --- |
| `data/processed/sports_games_clean.csv` | 38,838 | 33 | Normalized multi-league game file from the original city-level pipeline. |
| `data/processed/sports_games_enriched.csv` | 38,838 | 38 | City-enriched sports games with geography mapping fields. |
| `data/processed/event_city_weekly_exposure.csv` | 13,080 | 11 | City-week sports exposure rollup. |
| `data/processed/us/sports_games_us.csv` | 35,492 | 47 | U.S.-only sports games with venue geography fields. |
| `data/processed/us/event_county_weekly_exposure.csv` | 27,884 | 17 | County-week event exposure by league and all-league rollups. |
| `data/processed/us/event_cbsa_weekly_exposure.csv` | 25,470 | 14 | CBSA-week event exposure by league and all-league rollups. |
| `data/processed/us/venue_geography_us.csv` | 310 | 21 | Curated U.S. venue geography reference. |

## Important Columns

- `game_id`: stable game identifier.
- `league`: sports league, such as MLB, NBA, NFL, or NHL.
- `game_date`: event date.
- `venue_name`: event venue name when available.
- `exact_venue_county_fips`: county FIPS code for U.S. venue geography.
- `exact_venue_cbsa_code`: CBSA code for broader market geography.
- `game_count`: number of games in a geography-week rollup.
- `playoff_game_count`: number of playoff games in a geography-week.
- `championship_game_count`: number of championship games in a geography-week.
- `neutral_site_game_count`: number of neutral-site games in a geography-week.
- `high_confidence_venue_game_count`: event count with high-confidence venue mapping.

## Teaching Uses

- build treatment variables such as `has_event` and `event_intensity`
- compare event weeks with non-event weeks
- explain geography joins from venue to county and CBSA
- discuss exposure measurement error and venue-confidence caveats

## Limitations

- Venue-based exposure may miss economic spillovers outside the host geography.
- Some events are mapped through curated or fallback geography logic.
- A sports event is an observational exposure, not a randomized treatment.
- Event timing may overlap with other local shocks, holidays, or tourism patterns.

## Responsible Interpretation

Use:

```text
Sports event exposure is associated with local activity in this dataset.
```

Avoid:

```text
Sports events caused local economic changes.
```
