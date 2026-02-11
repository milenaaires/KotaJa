from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional

@dataclass(frozen=True)
class QuoteFilters:
    month_ref: date
    region_id: str
    brand_id: Optional[str] = None
    model_id: Optional[str] = None
    vehicle_variant_id: Optional[str] = None

@dataclass(frozen=True)
class QuoteResult:
    found: bool
    avg_price: Optional[Decimal]
    sample_size: Optional[int]
    message: str
