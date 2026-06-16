with exposure as (
    select *
    from {{ ref('stg_event_county_weekly_exposure') }}
    where league = 'ALL'
),

economic as (
    select *
    from {{ ref('stg_womply_county_weekly') }}
)

select
    exposure.county_fips,
    exposure.county_name,
    exposure.state,
    exposure.cbsa_code,
    exposure.cbsa_name,
    exposure.week_start_monday,
    economic.revenue_all,
    economic.merchants_all,
    exposure.game_count,
    exposure.playoff_game_count,
    exposure.championship_game_count,
    exposure.neutral_site_game_count,
    exposure.total_attendance,
    exposure.high_confidence_venue_game_count,
    exposure.low_confidence_venue_game_count,
    exposure.game_count > 0 as has_event,
    exposure.playoff_game_count > 0 as playoff_event
from exposure
left join economic
    on exposure.county_fips = economic.county_fips
    and exposure.week_start_monday = economic.week_start_monday
