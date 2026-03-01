with base as (
    select *
    from {{ ref('stg_solar_energy_5_min') }}
), 

-- kwh formula: (power in watts) * (grain: 5 minute) * (1 hour / 60 mins) * (1 kW / 1000 W) = kWh
solar_energy_daily as (
    select
        cast(timestamp as date) as date,
        sum(generation) * (5.0 / (60.0 * 1000) ) as generation_kwh,
        sum(consumption) * (5.0 / (60.0 * 1000) ) as consumption_kwh,
        sum(grid_feed_in) * (5.0 / (60.0 * 1000) ) * (-1) as grid_feed_in_kwh,
        sum(grid_purchase) * (5.0 / (60.0 * 1000) ) as grid_purchase_kwh,
        sum(charge_power) * (5.0 / (60.0 * 1000) ) * (-1) as charge_kwh,
        sum(discharge_power) * (5.0 / (60.0 * 1000) ) as discharge_kwh
    from base
    group by date
)

select * from solar_energy_daily
order by date
