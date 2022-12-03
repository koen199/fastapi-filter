from pydantic import BaseModel
from typing import List, Union, TYPE_CHECKING
from fastapi_filter.filters import FILTERS

if TYPE_CHECKING:
    from fastapi_filter.filters.filters import Filter

__FILTER_MAP = {f.OP: f for f in FILTERS}

def _get_filter_class(operator:str)->Filter:
    try:
        __FILTER_MAP[operator]
    except IndexError:
        raise ValueError('No filter with operator {} exists'.format(operator))

class FilterSchema(BaseModel):
    field:str 
    op:str
    value:Union[str,float,int]

def deserialize_filters(filters_data:List[FilterSchema])->List[Filter]:
    filters = []
    for f in filters_data:
        Class = _get_filter_class(f.op)
        filters.append(Class(f))
    return filters