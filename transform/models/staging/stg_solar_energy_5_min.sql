with source as (
    select * from {{ source('raw', 'raw_solar_energy_5_min') }}
),

transformed as (
    select 
        to_timestamp(timestamp) as timestamp,
        {{ date_key('to_timestamp(timestamp)') }} as date_key,
        {{ time_key('to_timestamp(timestamp)') }} as time_key,

        cast(generation as double) as generation,
        cast(consumption as double) as consumption,
        cast(grid_feed_in as double) as grid_feed_in,
        cast(grid_purchase as double) as grid_purchase,
        cast(charge_power as double) as charge_power,
        cast(discharge_power as double) as discharge_power,
        cast(battery_soc as double) as battery_soc,
        loaded_at
    from source
    where timestamp is not null
)

select * from transformed

