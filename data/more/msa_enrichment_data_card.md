# MSA Enrichment Data Card

## Purpose

The MSA enrichment pipeline appends CBSA/MSA-level context to sports game rows
so games can be grouped into comparable observational blocks before comparing
economic outcomes such as sales, transactions, real sales, or sector-level
activity.

The current implementation is a reproducible first pass. It uses the existing
official-backed Census/OMB county-to-CBSA crosswalk and exact U.S. sports venue
geography already present in the project. It creates stable schemas for a
broader federal-source enrichment layer, but several requested attributes remain
planned blanks until their source files are ingested.

This dataset supports observational comparisons and blocking. It does not by
itself establish causal effects of sports events on local economic outcomes.

## Unit Of Observation

| Output | Unit |
|---|---|
| `data/intermediate/county_cbsa_crosswalk.csv` | one county-CBSA row |
| `data/processed/msa_attribute_master.csv` | one CBSA/MSA |
| `data/processed/sports_games_msa_enriched.csv` | one sports game |
| `data/processed/msa_blocks.csv` | one CBSA/MSA with block assignment |

## Source Datasets And Vintages

| Source | Publisher | Vintage | Status |
|---|---|---|---|
| Census/OMB CBSA delineation file | U.S. Census Bureau / OMB | 2023-07 | ingested from curated local file |
| County population from GeoIDs | Opportunity Insights Economic Tracker geography file | 2019 | ingested from curated local file |
| Sports game-level MSA source | Project processed data | project-current | ingested |
| NCHS urban-rural classification | CDC NCHS | latest available | planned Phase 2 |
| RUCC, UIC, county typology | USDA ERS | latest available | planned Phase 2 |
| GDP by county/metro | BEA | latest available | planned Phase 2 |
| QCEW employment and wages | BLS | latest available | planned Phase 2 |
| SVI | CDC/ATSDR | latest available | planned Phase 2 |
| Climate normals | NOAA NCEI | 1991-2020 normals | planned Phase 2 |
| EPA ecoregions | EPA | latest available | planned Phase 2 |

Full source notes are recorded in
`metadata/msa_enrichment_sources.yaml`.

## Join Keys

| Join | Key |
|---|---|
| county to CBSA | `county_fips` |
| game to exact venue geography | `game_id` through `data/processed/simple_game_dataset.csv` |
| game to MSA attributes | `venue_cbsa_code` to `cbsa_code` |
| MSA attributes to blocks | `cbsa_code` |

CBSA is the canonical technical key. `msa` and `venue_cbsa_title` are user-facing
labels.

## Aggregation Methods

Current implemented aggregations:

- County population is summed to CBSA.
- CBSA state list is the distinct set of county states.
- CBSA type is the dominant official Census/OMB type in the crosswalk.
- Region is derived from the state list using Census-style broad regions.
- Population size bins are rank bins across CBSAs in the master table.
- Urban/rural labels are first-pass proxies derived from CBSA type and
  population size.

Planned aggregations:

- Population-weighted averages for SVI, NCHS, amenities, and other continuous
  county variables.
- Employment-weighted averages for QCEW labor-market variables.
- Dominant-category logic for RUCC, UIC, typology, ecoregions, and climate
  clusters.
- Shares for mixed MSAs, such as county typology shares or NCHS class shares.

## Blocking Variables

Current full block:

```text
msa_block_id = region + pop_size_bin + nchs_urban_rural_dominant + economic_profile + vulnerability_bin
```

Current compact block:

```text
msa_block_compact_id = pop_size_bin + nchs_urban_rural_dominant + service_economy_bin + svi_bin
```

In the first pass, `economic_profile`, `service_economy_bin`, and `svi_bin` are
unknown placeholders because BEA, QCEW, and SVI have not yet been ingested.

Sparse blocks are flagged when they contain fewer than 5 MSAs or fewer than 20
games.

## Output Schemas

### `msa_attribute_master.csv`

Required high-value fields include:

- `cbsa_code`
- `cbsa_title`
- `cbsa_type`
- `state_list`
- `region`
- `county_count`
- `population_latest`
- `population_2019`
- `population_growth_pct_2019_latest`
- `pop_size_bin`
- `pop_growth_bin`
- `nchs_urban_rural_dominant`
- `rucc_dominant`
- `uic_dominant`
- `dominant_county_typology`
- `gdp_total`
- `gdp_per_capita`
- `dominant_gdp_industry`
- `economic_diversity_hhi`
- `avg_weekly_wage`
- `local_service_economy_index`
- `natural_amenities_bin`
- `climate_cluster`
- `dominant_ecoregion_level_3`
- `svi_overall_population_weighted`
- `svi_overall_quintile`
- `source_vintage_summary`
- `attribute_completeness_score`

Current row count: 935 CBSAs.

### `sports_games_msa_enriched.csv`

Includes original game fields plus:

- `venue_county_fips`
- `venue_cbsa_code`
- `venue_cbsa_title`
- selected MSA attributes
- `msa_block_id`
- `msa_block_label`
- `msa_block_compact_id`
- `venue_geo_match_method`
- `venue_geo_match_confidence`
- `enrichment_warning`

Current row count: 38,838 games.

### `msa_blocks.csv`

Includes:

- `cbsa_code`
- `cbsa_title`
- `msa_block_id`
- `msa_block_compact_id`
- `block_population_count`
- `block_msa_count`
- `block_game_count`
- `is_sparse_block`
- `recommended_for_matching`

Current row count: 935 CBSAs.

## Missingness Summary

Current first-pass coverage:

| Check | Result |
|---|---|
| Sports rows | 38,838 |
| Sports rows with `venue_cbsa_code` | 35,492 |
| Sports rows without CBSA | 3,346 |
| MSA master rows | 935 |
| Sparse MSA block rows | 857 |
| Recommended-for-matching MSA block rows | 78 |

High-missingness planned fields include BEA GDP, QCEW wages/employment, USDA
rurality and typology, SVI, natural amenities, climate normals, and ecoregions.
These fields are present to stabilize the schema but should not yet be used for
blocking decisions until populated.

## Validation Checks

Validation is implemented in:

```bash
python scripts/msa_enrichment/06_validate_outputs.py
```

The validation report is:

```text
metadata/msa_enrichment_validation_report.csv
```

Implemented checks include:

- row counts for sports games, MSA master, and block table
- each game has CBSA or an enrichment warning
- each populated game CBSA joins to the MSA master
- county FIPS values are valid 5-character strings
- duplicate `game_id` detection
- feature missingness reporting
- sparse block reporting
- 25-game lineage sample for manual review

Current validation status: no failing checks.

## Known Limitations

- This is a first-pass MSA enrichment layer, not the full federal attribute
  warehouse described in the task.
- Population is currently 2019 county population summed to CBSA. It is used for
  size bins but not yet for growth estimates.
- NCHS urban/rural labels are currently proxies derived from CBSA type and
  population, not the official NCHS county classification.
- BEA, BLS QCEW, USDA ERS, NOAA, EPA, and CDC SVI attributes are planned fields
  and should not be treated as populated evidence.
- Non-U.S. and unmatched games retain blank CBSA attributes with an enrichment
  warning.
- Blocking groups can be sparse. Use `recommended_for_matching` before relying
  on a block for matching or controls.

## Recommended Use

Use this dataset to:

- group sports games by CBSA/MSA context
- compare event-heavy MSA-weeks within broad population and urbanization blocks
- audit venue-to-county-to-CBSA lineage
- identify where richer federal attributes should be prioritized
- build first-pass control pools for observational analysis

## Not Recommended Use

Do not use this dataset to:

- claim causal effects of sports events
- perform final matching on unpopulated planned fields
- compare all MSAs as interchangeable
- treat city-level venue strings as equivalent to county-based CBSA geography
- ignore sparse-block warnings

## Rebuild Instructions

Run from the repository root:

```bash
python scripts/msa_enrichment/01_download_msa_sources.py
python scripts/msa_enrichment/02_build_county_cbsa_crosswalk.py
python scripts/msa_enrichment/03_build_msa_attribute_tables.py
python scripts/msa_enrichment/04_enrich_sports_games_with_msa.py
python scripts/msa_enrichment/05_build_msa_blocks.py
python scripts/msa_enrichment/06_validate_outputs.py
```

Use `--force` with `01_download_msa_sources.py` to refresh copied raw source
snapshots from local curated inputs.
