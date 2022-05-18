"""Fix views

Revision ID: 95ba0cae72ef
Revises: beceec3e74dd
Create Date: 2020-12-20 23:14:19.670213

"""
import sqlalchemy as sa
from alembic_utils.pg_view import PGView

from alembic import op

# revision identifiers, used by Alembic.
revision = "95ba0cae72ef"
down_revision = "beceec3e74dd"
branch_labels = None
depends_on = None


statement_view = PGView(
    schema="public",
    signature="v_statement",
    definition="""
 SELECT transaction.id,
    transaction.account_id,
    transaction.broker_id,
    transaction.isin,
    transaction.qty,
    transaction.creditdebit,
    transaction.type,
    transaction.transaction_date,
    transaction.dealprice,
    transaction.payment_ref,
    transaction.closing_balance,
    transaction.payment_type,
    transaction.opening_balance,
    transaction.stock,
    broker.name AS broker,
        CASE
            WHEN transaction.creditdebit = 'DELI'::bpchar THEN transaction.qty
            ELSE 0::bigint
        END AS debit,
        CASE
            WHEN transaction.creditdebit = 'RECE'::bpchar THEN transaction.qty
            ELSE 0::bigint
        END AS credit
   FROM transaction
     LEFT JOIN broker ON broker.id = transaction.broker_id::text
  ORDER BY transaction.id;
    """,
)


holdings_view = PGView(
    schema="public",
    signature="v_holdings",
    definition="""
 WITH cte AS (
         SELECT row_number() OVER (PARTITION BY v_statement.broker_id, v_statement.account_id, v_statement.isin, v_statement.stock ORDER BY v_statement.id DESC) AS rn,
            v_statement.account_id,
            v_statement.broker_id,
            v_statement.isin,
            v_statement.stock,
            v_statement.closing_balance,
            v_statement.transaction_date
           FROM v_statement
        )
 SELECT cte.account_id,
    cte.broker_id,
    cte.isin,
    cte.stock,
    cte.closing_balance,
    cte.transaction_date
   FROM cte
  WHERE cte.rn = 1
  ORDER BY cte.account_id, cte.isin, cte.stock, cte.broker_id;
    """,
)


def upgrade():
    op.create_entity(statement_view)
    op.create_entity(holdings_view)
    pass


def downgrade():
    op.drop_entity(holdings_view)
    op.drop_entity(statement_view)
    pass
