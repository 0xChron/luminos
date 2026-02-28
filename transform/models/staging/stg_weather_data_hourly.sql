with source as (
    select * from {{ source('raw', 'raw_weather_data_hourly') }}
),

transformed as (
    select 
        timestamp,
        {{ date_key('timestamp') }} as date_key,
        {{ time_key('timestamp') }} as time_key,

        cast(temperature_2m as double) as temperature_2m,
        cast(cloud_cover as double) as cloud_cover,
        cast(precipitation as double) as precipitation,
        cast(wind_speed_10m as double) as wind_speed_10m,
        cast(relative_humidity_2m as double) as relative_humidity_2m,
        cast(weather_code as integer) as weather_code,
        loaded_at
    from source
    where timestamp is not null
)

select * from transformed

