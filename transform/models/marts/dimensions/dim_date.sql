{{ config(materialized='table', unique_key='date_key') }}

WITH date_spine AS (
    {{ dbt_utils.date_spine(
        datepart="day",
        start_date="cast('" ~ var('start_date') ~ "' as date)",
        end_date="cast('" ~ var('end_date') ~ "' as date)"
    ) }}
),

date_dimension AS (
    SELECT
        -- surrogate key
        strftime(date_day, '%Y%m%d')::INTEGER AS date_key,
        
        -- natural key
        date_day AS date,
        
        -- year attributes
        EXTRACT(YEAR FROM date_day) AS year,
        EXTRACT(QUARTER FROM date_day) AS quarter,
        CONCAT('Q', EXTRACT(QUARTER FROM date_day), ' ', EXTRACT(YEAR FROM date_day)) AS quarter_name,
        
        -- month attributes
        EXTRACT(MONTH FROM date_day) AS month_number,
        TRIM(strftime(date_day, '%B')) AS month_name,
        strftime(date_day, '%Y-%m') AS year_month,
        
        -- week attributes
        EXTRACT(WEEK FROM date_day) AS week_of_year,
        
        -- day attributes
        EXTRACT(DAY FROM date_day) AS day_of_month,
        EXTRACT(DOW FROM date_day) AS day_of_week_number,
        TRIM(strftime(date_day, '%A')) AS day_name,
        EXTRACT(DOY FROM date_day) AS day_of_year,
        
        -- philippines seasons (wet: june-nov, dry: dec-may)
        CASE 
            WHEN EXTRACT(MONTH FROM date_day) BETWEEN 6 AND 11 
            THEN 'Wet'
            ELSE 'Dry'
        END AS season,
        
        -- weekend 
        CASE WHEN EXTRACT(DOW FROM date_day) IN (0, 6) THEN TRUE ELSE FALSE END AS is_weekend
        
    FROM date_spine
)

SELECT * FROM date_dimension