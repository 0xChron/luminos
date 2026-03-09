with solar_base as (
    select *
    from {{ ref('fact_solar_daily') }}
), 

weather_base as (
    select *
    from {{ ref('fact_weather_daily') }}
),

dim_date as (
    select *
    from {{ ref('dim_date') }}
),

solar_weather_monthly as (
    select 
        d.year_month,
        sum(s.generation_kwh) as generation_kwh,
        sum(s.consumption_kwh) as consumption_kwh,
        sum(s.grid_feed_in_kwh) as grid_feed_in_kwh,
        sum(s.grid_purchase_kwh) as grid_purchase_kwh,
        sum(s.charge_kwh) as charge_kwh,
        sum(s.discharge_kwh) as discharge_kwh,
        sum(w.shortwave_radiation_sum) as shortwave_radiation_sum,
        sum(w.sunshine_duration) as sunshine_duration,
        sum(w.daylight_duration) as daylight_duration,
        avg(w.cloud_cover_mean) as cloud_cover_mean,
        avg(w.temperature_2m_mean) as temperature_2m_mean,
        avg(w.relative_humidity_2m_mean) as relative_humidity_2m_mean,
        sum(w.rain_sum) as rain_sum,
        avg(w.wind_speed_10m_mean) as wind_speed_10m_mean
    from solar_base s
    join dim_date d
        on s.date = d.date
    join weather_base w
        on s.date = w.date
    group by d.year_month
)

select *
from solar_weather_monthly
order by year_month