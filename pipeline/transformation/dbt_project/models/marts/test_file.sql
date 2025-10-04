SELECT *
from {{ source('raw', 'products') }}
