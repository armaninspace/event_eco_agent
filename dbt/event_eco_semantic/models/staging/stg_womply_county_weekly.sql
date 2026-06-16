select
    cast(countyfips as varchar) as county_fips,
    cast(week_start_monday as date) as week_start_monday,
    cast(merchants_all as double) as merchants_all,
    cast(revenue_all as double) as revenue_all,
    cast(year as integer) as year,
    cast(month as integer) as month,
    cast(day_endofweek as integer) as day_endofweek
from read_csv_auto('../../data/processed/us/economic/womply_county_weekly.csv', header=true)
