from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.prediction import Prediction


class Detection(Base):
    __tablename__ = "detections"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    prediction_id: Mapped[int] = mapped_column(
        ForeignKey("predictions.id"),
        index=True,
    )

    class_name: Mapped[str] = mapped_column(
        String(100)
    )

    confidence: Mapped[float] = mapped_column(
        Float
    )

    x1: Mapped[float] = mapped_column(
        Float
    )

    y1: Mapped[float] = mapped_column(
        Float
    )

    x2: Mapped[float] = mapped_column(
        Float
    )

    y2: Mapped[float] = mapped_column(
        Float
    )

    prediction: Mapped["Prediction"] = relationship(
        "Prediction",
        back_populates="detections",
    )