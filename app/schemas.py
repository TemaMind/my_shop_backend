"""Pydantic-схемы для валидации параметров запроса на /info."""

from typing import Optional

from pydantic import BaseModel, Field


class InfoParams(BaseModel):
    """
    Параметры запроса на /info.

    - category: фильтрация по имени категории
    - min_price: минимальная цена (>= 0)
    - max_price: максимальная цена (>= 0)
    """

    category: Optional[str] = Field(
        None,
        description="Filter by category name"
    )
    min_price: Optional[float] = Field(
        None,
        ge=0,
        description="Minimum price"
    )
    max_price: Optional[float] = Field(
        None,
        ge=0,
        description="Maximum price"
    )
