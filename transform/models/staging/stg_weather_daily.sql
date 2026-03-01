with source as (
    select * from {{ source('raw', 'raw_weather_daily') }}
),

transformed as (
    select 
        timestamp,
        cast(shortwave_radiation_sum as double) as shortwave_radiation_sum,
        cast(sunshine_duration as double) as sunshine_duration,
        cast(daylight_duration as double) as daylight_duration,
        cast(cloud_cover_mean as double) as cloud_cover_mean,
        cast(temperature_2m_mean as double) as temperature_2m_mean,
        cast(relative_humidity_2m_mean as double) as relative_humidity_2m_mean,
        cast(rain_sum as double) as rain_sum,
        cast(wind_speed_10m_mean as double) as wind_speed_10m_mean,
        cast(weather_code as int) as weather_code,
        loaded_at
    from source
    where timestamp is not null
)

select * from transformed

