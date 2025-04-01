# clickhouse_connect/integrations.sqla/execution.py
from sqlalchemy.engine.default import DefaultExecutionContext


class ChExecutionContext(DefaultExecutionContext):
    pass
