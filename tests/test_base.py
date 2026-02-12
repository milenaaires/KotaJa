from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer

from src.db.base import Base


def test_base_is_declarative_base_subclass():
    assert issubclass(Base, DeclarativeBase)


def test_base_has_metadata():
    # Base deve ter o objeto MetaData
    assert hasattr(Base, "metadata")
    assert Base.metadata is not None


def test_can_declare_model_using_base():
    class Dummy(Base):
        __tablename__ = "dummy_test_table"

        id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Confirma que a tabela foi registrada no metadata
    assert "dummy_test_table" in Base.metadata.tables
