with source as (
    select * from {{ source('raw', 'raw_weather_data_daily') }}
),

transformed as (
    select 
        timestamp,
        {{ date_key('timestamp') }} as date_key,
        {{ time_key('timestamp') }} as time_key,

        cast(shortwave_radiation_sum as double) as shortwave_radiation_sum,
        cast(sunshine_duration as double) as sunshine_duration,
        cast(daylight_duration as double) as daylight_duration,
        cast(uv_index_clear_sky_max as double) as uv_index_clear_sky_max,
        cast(temperature_2m_max as double) as temperature_2m_max,
        cast(temperature_2m_min as double) as temperature_2m_min,
        loaded_at
    from source
    where timestamp is not null
)

select * from transformed

