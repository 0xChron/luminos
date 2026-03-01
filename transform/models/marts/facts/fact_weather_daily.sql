with base as (
    select *
    from {{ ref('stg_weather_data_daily') }}
),

weather_daily as (
    select 
        cast(timestamp as date) as date,
        shortwave_radiation_sum,
        sunshine_duration,
        daylight_duration,
        cloud_cover_mean,
        temperature_2m_mean,
        relative_humidity_2m_mean,
        rain_sum,
        wind_speed_10m_mean,
        weather_code
    from base
)

select * from weather_daily
order by date