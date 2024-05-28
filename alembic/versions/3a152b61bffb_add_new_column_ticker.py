"""Add new column ticker

Revision ID: 3a152b61bffb
Revises: 70d0aacbc475
Create Date: 2024-05-17 22:16:42.587954

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector


# revision identifiers, used by Alembic.
revision: str = '3a152b61bffb'
down_revision: Union[str, None] = '70d0aacbc475'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)

    # article_contents 테이블에 ticker 컬럼이 있는지 확인
    columns = [column['name'] for column in inspector.get_columns('article_contents')]
    if 'ticker' not in columns:
        op.add_column('article_contents', sa.Column('ticker', sa.String(), nullable=False, server_default=''))

    # articles 테이블에 ticker 컬럼이 있는지 확인
    columns = [column['name'] for column in inspector.get_columns('articles')]
    if 'ticker' not in columns:
        op.add_column('articles', sa.Column('ticker', sa.String(), nullable=False, server_default=''))

def downgrade() -> None:
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)

    # article_contents 테이블에 ticker 컬럼이 있는지 확인
    columns = [column['name'] for column in inspector.get_columns('article_contents')]
    if 'ticker' in columns:
        op.drop_column('article_contents', 'ticker')

    # articles 테이블에 ticker 컬럼이 있는지 확인
    columns = [column['name'] for column in inspector.get_columns('articles')]
    if 'ticker' in columns:
        op.drop_column('articles', 'ticker')
