with base as (
    select *
    from {{ ref('stg_solar_energy_5_min') }}
), 

solar_energy_hourly as (
    select
        date_key,
        date_trunc('hour', timestamp) as hour_ts,
        sum(generation) * (5.0 / (60.0 * 1000)) as generation_kwh,
        sum(consumption) * (5.0 / (60.0 * 1000)) as consumption_kwh,
        sum(grid_feed_in) * (5.0 / (60.0 * 1000)) * (-1) as grid_feed_in_kwh,
        sum(grid_purchase) * (5.0 / (60.0 * 1000)) as grid_purchase_kwh,
        sum(charge_power) * (5.0 / (60.0 * 1000)) * (-1) as charge_kwh,
        sum(discharge_power) * (5.0 / (60.0 * 1000)) as discharge_kwh,
        arg_max(battery_soc, timestamp) as battery_soc_eoh
    from base
    group by date_key, hour_ts
)

select * from solar_energy_hourly
order by date_key, hour_ts