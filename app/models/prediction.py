from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    request_id: Mapped[str] = mapped_column(
        String(100),
        index=True,
    )

    image_name: Mapped[str] = mapped_column(
        String(255),
    )

    model_version: Mapped[str] = mapped_column(
        String(100),
    )

    detection_count: Mapped[int] = mapped_column(
        Integer,
    )

    inference_time_ms: Mapped[float] = mapped_column(
        Float,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )