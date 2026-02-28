with dim_weather_codes as (
    select 
        cast(weather_code as integer) as weather_code,
        trim(description) as description
    from {{ ref('wmo_weather_codes') }}
)

select * from dim_weather_codes
