select
    cast(county_fips as varchar) as county_fips,
    county_name,
    state,
    cast(cbsa_code as varchar) as cbsa_code,
    cbsa_name,
    cast(week_start_monday as date) as week_start_monday,
    league,
    cast(game_count as double) as game_count,
    cast(completed_game_count as double) as completed_game_count,
    cast(future_or_uncompleted_game_count as double) as future_or_uncompleted_game_count,
    cast(playoff_game_count as double) as playoff_game_count,
    cast(championship_game_count as double) as championship_game_count,
    cast(neutral_site_game_count as double) as neutral_site_game_count,
    cast(total_attendance as double) as total_attendance,
    cast(unique_venue_count as double) as unique_venue_count,
    cast(high_confidence_venue_game_count as double) as high_confidence_venue_game_count,
    cast(low_confidence_venue_game_count as double) as low_confidence_venue_game_count
from read_csv_auto('../../data/processed/us/event_county_weekly_exposure.csv', header=true)
