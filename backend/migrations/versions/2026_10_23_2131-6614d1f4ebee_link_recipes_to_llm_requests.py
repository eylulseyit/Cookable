"""link recipes to llm requests

Revision ID: 6614d1f4ebee
Revises: afc2e767b03b
Create Date: 2026-10-23 21:31:52.768360

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6614d1f4ebee'
down_revision: Union[str, Sequence[str], None] = 'afc2e767b03b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('recipes', sa.Column('description', sa.Text(), nullable=True))
    op.add_column('recipes', sa.Column('llm_request_id', sa.BigInteger(), nullable=True))
    op.create_index(op.f('ix_recipes_llm_request_id'), 'recipes', ['llm_request_id'], unique=False)
    op.create_foreign_key(op.f('fk_recipes_llm_request_id_llm_requests'), 'recipes', 'llm_requests', ['llm_request_id'], ['id'], ondelete='SET NULL')

    # Keep existing data: move each request -> recipe link to the recipe side, and
    # rename single-recipe requests so ingredient popularity still counts them
    op.execute(
        "UPDATE recipes SET llm_request_id = llm_requests.id "
        "FROM llm_requests WHERE llm_requests.recipe_id = recipes.id"
    )
    op.execute("UPDATE llm_requests SET operation = 'recipe_suggestions' WHERE operation = 'recipe'")

    op.drop_constraint(op.f('fk_llm_requests_recipe_id_recipes'), 'llm_requests', type_='foreignkey')
    op.drop_column('llm_requests', 'recipe_id')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('llm_requests', sa.Column('recipe_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key(op.f('fk_llm_requests_recipe_id_recipes'), 'llm_requests', 'recipes', ['recipe_id'], ['id'], ondelete='SET NULL')
    # A request may now own several recipes; the old column can only point back to one of them
    op.execute(
        "UPDATE llm_requests SET recipe_id = "
        "(SELECT min(id) FROM recipes WHERE recipes.llm_request_id = llm_requests.id)"
    )
    op.execute("UPDATE llm_requests SET operation = 'recipe' WHERE operation = 'recipe_suggestions'")

    op.drop_constraint(op.f('fk_recipes_llm_request_id_llm_requests'), 'recipes', type_='foreignkey')
    op.drop_index(op.f('ix_recipes_llm_request_id'), table_name='recipes')
    op.drop_column('recipes', 'llm_request_id')
    op.drop_column('recipes', 'description')
