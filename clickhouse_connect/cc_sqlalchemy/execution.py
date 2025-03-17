# clickhouse_connect/cc_sqlalchemy/execution.py
from sqlalchemy.engine.default import DefaultExecutionContext


class ChExecutionContext(DefaultExecutionContext):
    pass
