"""Create prediction and detection tables

Revision ID: 11335acb0603
Revises:
Create Date: 2026-09-30 10:38:41.636633

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "11335acb0603"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "predictions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("request_id", sa.String(length=100), nullable=False),
        sa.Column("image_name", sa.String(length=255), nullable=False),
        sa.Column("model_version", sa.String(length=100), nullable=False),
        sa.Column("detection_count", sa.Integer(), nullable=False),
        sa.Column("inference_time_ms", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_index(
        "ix_predictions_id",
        "predictions",
        ["id"],
        unique=False,
    )

    op.create_index(
        "ix_predictions_request_id",
        "predictions",
        ["request_id"],
        unique=False,
    )

    op.create_table(
        "detections",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "prediction_id",
            sa.Integer(),
            sa.ForeignKey("predictions.id"),
            nullable=False,
        ),
        sa.Column("class_name", sa.String(length=100), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("x1", sa.Float(), nullable=False),
        sa.Column("y1", sa.Float(), nullable=False),
        sa.Column("x2", sa.Float(), nullable=False),
        sa.Column("y2", sa.Float(), nullable=False),
    )

    op.create_index(
        "ix_detections_id",
        "detections",
        ["id"],
        unique=False,
    )

    op.create_index(
        "ix_detections_prediction_id",
        "detections",
        ["prediction_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_detections_prediction_id",
        table_name="detections",
    )
    op.drop_index(
        "ix_detections_id",
        table_name="detections",
    )
    op.drop_table("detections")

    op.drop_index(
        "ix_predictions_request_id",
        table_name="predictions",
    )
    op.drop_index(
        "ix_predictions_id",
        table_name="predictions",
    )
    op.drop_table("predictions")