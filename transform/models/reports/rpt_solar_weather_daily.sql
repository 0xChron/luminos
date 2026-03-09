with solar_base as (
    select *
    from {{ ref('fact_solar_daily') }}
), 

weather_base as (
    select *
    from {{ ref('fact_weather_daily') }}
),

dim_weather_codes as (
    select *
    from {{ ref('dim_weather_codes') }}
),

solar_weather_daily as (
    select 
        s.date,
        s.generation_kwh,
        s.consumption_kwh,
        s.grid_feed_in_kwh,
        s.grid_purchase_kwh,
        s.charge_kwh,
        s.discharge_kwh,
        w.shortwave_radiation_sum,
        w.sunshine_duration,
        w.daylight_duration,
        w.cloud_cover_mean,
        w.temperature_2m_mean,
        w.relative_humidity_2m_mean,
        w.rain_sum,
        w.wind_speed_10m_mean,
        wc.description as weather_description
    from solar_base s
    join weather_base w
        on s.date = w.date
    join dim_weather_codes wc
        on w.weather_code = wc.weather_code
)

select *
from solar_weather_daily
order by date
