{% macro date_key(ts_expr) -%}
    cast(strftime(cast({{ ts_expr }} as timestamp), '%Y%m%d') as integer)
{%- endmacro %}

{% macro time_key(ts_expr) -%}
    cast(
        (extract(hour from cast({{ ts_expr }} as timestamp)) * 100)
        +
        (floor(extract(minute from cast({{ ts_expr }} as timestamp)) / 5) * 5)
    as integer)
{%- endmacro %}