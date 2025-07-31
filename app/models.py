"""ORM-модели Category и Product со связями и каскадным удалением."""

from sqlalchemy import (
    Boolean,
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Category(Base):
    """Категория товара: связь один-ко-многим с Product."""

    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    products = relationship(
        'Product',
        back_populates='category',
        cascade='all, delete-orphan',
        passive_deletes=True,
    )


class Product(Base):
    """Модель товара: хранит информацию и FK на Category."""

    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    price = Column(Float, nullable=False)
    image_url = Column(String, nullable=True)
    on_main = Column(Boolean, default=False, nullable=False)
    category_id = Column(
        Integer,
        ForeignKey('categories.id', ondelete='CASCADE'),
        nullable=False,
    )
    category = relationship(
        'Category',
        back_populates='products',
    )
