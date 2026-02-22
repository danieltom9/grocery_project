with src as (

    select *
    from {{ source('raw', 'products_2') }}

),

deduped as (

    select *
    from (
        select
            *,
            row_number() over (
                partition by product_id
                order by product_name
            ) as rn
        from src
    )
    where rn = 1

)

select
    product_id,
    product_name,
    search_term,
    price
from deduped
