{{ config(materialized='table', unique_key='time_key') }}

with time_spine as (
    -- minutes since midnight: 0..1435 stepping by 5 minutes
    select gs as minutes_since_midnight
    from generate_series(0, 1435, 5) as t(gs)
),


time_dimension as (
    select
        -- surrogate key: HHMM (e.g., 0:00 -> 0, 13:05 -> 1305)
        (
          lpad(cast(floor(minutes_since_midnight / 60) as varchar), 2, '0') ||
          lpad(cast(minutes_since_midnight % 60 as varchar), 2, '0')
        )::integer as time_key,

        -- natural time parts
        floor(minutes_since_midnight / 60)::integer as hour,
        (minutes_since_midnight % 60)::integer as minute,
        0::integer as second,

        -- convenience
        (hour * 3600 + minute * 60 + second)::integer as seconds_since_midnight,
        lpad(cast(hour as varchar), 2, '0') || ':' || lpad(cast(minute as varchar), 2, '0') || ':00' as time_label,

        -- flags
        case when hour between 6 and 17 then true else false end as is_daylight,
        case when hour between 0 and 5 then true else false end as is_night,
        case when minute = 0 then true else false end as is_top_of_hour,

        current_timestamp as dbt_updated_at
    from time_spine
)

select * from time_dimension
order by time_key