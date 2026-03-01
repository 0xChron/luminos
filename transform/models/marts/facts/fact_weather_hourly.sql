with base as (
    select *
    from {{ ref('stg_weather_hourly') }}
),

weather_hourly as (
    select 
        cast(timestamp as date) as date,
        date_trunc('hour', timestamp) as hour_ts,
        relative_humidity_2m,
        wind_speed_10m,
        case when is_day = 1 then true else false end as is_day,
        sunshine_duration,
        temperature_2m,
        cloud_cover,
        rain,
        weather_code
    from base
) 

select * from weather_hourly
order by date, hour_ts