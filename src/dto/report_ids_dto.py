from typing import List
from pydantic import BaseModel, constr


class ReportIdsDTO(BaseModel):
    ids: List[constr(min_length=1)]

