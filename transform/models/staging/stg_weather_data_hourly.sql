with source as (
    select * from {{ source('raw', 'raw_weather_data_hourly') }}
),

transformed as (
    select 
        timestamp,
        cast(relative_humidity_2m as double) as relative_humidity_2m,
        cast(wind_speed_10m as double) as wind_speed_10m,
        cast(is_day as int) as is_day,
        cast(sunshine_duration as double) as sunshine_duration,
        cast(temperature_2m as double) as temperature_2m,
        cast(cloud_cover as double) as cloud_cover,
        cast(rain as double) as rain,
        cast(weather_code as integer) as weather_code,
        loaded_at
    from source
    where timestamp is not null
)

select * from transformed

