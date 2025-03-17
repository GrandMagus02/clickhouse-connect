# clickhouse_connect/cc_sqlalchemy/sql/preparer.py
from sqlalchemy.sql.compiler import IdentifierPreparer


class ChIdentifierPreparer(IdentifierPreparer):
    # _double_percents = False  # Add this attribute
    pass
