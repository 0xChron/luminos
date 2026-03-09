with solar_base as (
    select *
    from {{ ref('fact_solar_hourly') }}
), 

weather_base as (
    select *
    from {{ ref('fact_weather_hourly') }}
),

dim_weather_codes as (
    select *
    from {{ ref('dim_weather_codes') }}
),

solar_weather_hourly as (
    select 
        s.date,
        s.hour_ts,
        s.generation_kwh,
        s.consumption_kwh,
        s.grid_feed_in_kwh,
        s.grid_purchase_kwh,
        s.charge_kwh,
        s.discharge_kwh,
        s.battery_soc_eoh,
        w.relative_humidity_2m,
        w.wind_speed_10m,
        w.is_day,
        w.sunshine_duration,
        w.temperature_2m,
        w.cloud_cover,
        w.rain,
        wc.description as weather_description
    from solar_base s
    join weather_base w
        on s.date = w.date
        and s.hour_ts = w.hour_ts
    join dim_weather_codes wc
        on w.weather_code = wc.weather_code
)

select *
from solar_weather_hourly
order by date, hour_ts
