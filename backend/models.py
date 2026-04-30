from sqlalchemy import String, Integer, Float, DateTime, JSON, ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime


def now_local():
    return datetime.now().astimezone()


class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    api_base_url: Mapped[str] = mapped_column(String(512), default="")
    api_usage_path: Mapped[str] = mapped_column(String(256), default="/v1/usage")
    api_balance_path: Mapped[str | None] = mapped_column(String(256), nullable=True)
    tp_base_url: Mapped[str] = mapped_column(String(512), default="")
    tp_usage_path: Mapped[str] = mapped_column(String(256), default="/v1/usage")
    currency_symbol: Mapped[str] = mapped_column(String(16), default="CNY")
    models: Mapped[list] = mapped_column(JSON, default=list)
    logo_path: Mapped[str | None] = mapped_column(String(512), nullable=True, default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_local)

    providers: Mapped[list["Provider"]] = relationship(back_populates="category")


class Provider(Base):
    __tablename__ = "providers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    api_key: Mapped[str] = mapped_column(String(512))  # Fernet encrypted
    base_url: Mapped[str] = mapped_column(String(512))
    usage_api_path: Mapped[str] = mapped_column(String(256), default="/v1/usage")
    models: Mapped[list] = mapped_column(JSON, default=list)
    usage_mapping: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    balance_mapping: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    balance_api_path: Mapped[str | None] = mapped_column(String(256), nullable=True)
    currency_symbol: Mapped[str] = mapped_column(String(16), default="CNY")
    last_balance: Mapped[float | None] = mapped_column(Float, nullable=True)
    interval_seconds: Mapped[int] = mapped_column(Integer, default=0)
    billing_mode: Mapped[str] = mapped_column(String(16), default="api")
    monthly_fee: Mapped[float | None] = mapped_column(Float, nullable=True)
    sub_start_date: Mapped[str | None] = mapped_column(String(16), nullable=True)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    deleted: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_local)

    category: Mapped["Category | None"] = relationship(back_populates="providers")
    usage_records: Mapped[list["UsageRecord"]] = relationship(back_populates="provider", cascade="all, delete-orphan")
    collection_logs: Mapped[list["CollectionLog"]] = relationship(back_populates="provider", cascade="all, delete-orphan")


class UsageRecord(Base):
    __tablename__ = "usage_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    provider_id: Mapped[int] = mapped_column(ForeignKey("providers.id"))
    model: Mapped[str] = mapped_column(String(128))
    tokens_used: Mapped[int] = mapped_column(Integer, default=0)
    cost: Mapped[float] = mapped_column(Float, default=0.0)
    balance: Mapped[float | None] = mapped_column(Float, nullable=True)
    recorded_at: Mapped[datetime] = mapped_column(DateTime, default=now_local)

    provider: Mapped["Provider"] = relationship(back_populates="usage_records")


class CollectionLog(Base):
    __tablename__ = "collection_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    provider_id: Mapped[int] = mapped_column(ForeignKey("providers.id"))
    status: Mapped[str] = mapped_column(String(50), default="ok")
    record_count: Mapped[int] = mapped_column(Integer, default=0)
    balance: Mapped[float | None] = mapped_column(Float, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_local)

    provider: Mapped["Provider"] = relationship(back_populates="collection_logs")
