from datetime import date, datetime
from typing import Any, Dict


class NeedsAssessment:
    BOOLEAN_FIELDS = (
        "air_filter", "oil_filter", "air_oil_separator", "pre_coalescing",
        "post_coalescing", "belts", "hoses",
    )

    @classmethod
    def serialize(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        result = dict(data)
        for field in cls.BOOLEAN_FIELDS:
            if result.get(field) is not None:
                result[field] = bool(result[field])
        for field in ("created_at", "updated_at"):
            if isinstance(result.get(field), (datetime, date)):
                result[field] = result[field].isoformat()
        return result
