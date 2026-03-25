from pydantic import BaseModel

class ReportSyncDTO(BaseModel):
    page: int
    limit: int