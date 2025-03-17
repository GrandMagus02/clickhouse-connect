# clickhouse_connect/cc_sqlalchemy/dialect.py
from typing import Any, Type, Optional

from sqlalchemy import util, text
from sqlalchemy.engine.default import DefaultDialect
from sqlalchemy.engine.interfaces import DBAPIConnection, PoolProxiedConnection, DBAPICursor, \
    _DBAPISingleExecuteParams, ExecutionContext
from sqlalchemy.engine.url import URL
from sqlalchemy.pool import Pool, NullPool
from sqlalchemy.sql import compiler

from clickhouse_connect import dbapi
from clickhouse_connect.cc_sqlalchemy import ischema_names, dialect_name
from clickhouse_connect.cc_sqlalchemy.execution import ChExecutionContext
from clickhouse_connect.cc_sqlalchemy.inspector import ChInspector
from clickhouse_connect.cc_sqlalchemy.sql import full_table
from clickhouse_connect.cc_sqlalchemy.sql.compiler import ChCompiler
from clickhouse_connect.cc_sqlalchemy.sql.ddlcompiler import ChDDLCompiler
from clickhouse_connect.cc_sqlalchemy.sql.preparer import ChIdentifierPreparer
from clickhouse_connect.cc_sqlalchemy.sql.type import ChTypeCompiler
from clickhouse_connect.driver.binding import quote_identifier, format_str


class ClickHouseDialect(DefaultDialect):
    name = dialect_name
    driver = 'connect'

    default_schema_name = 'default'
    supports_native_decimal = True
    supports_native_boolean = True
    supports_statement_cache = False
    returns_unicode_strings = True
    postfetch_lastrowid = False
    description_encoding = None
    max_identifier_length = 127
    ischema_names = ischema_names
    is_async = False
    compiler_linting = compiler.NO_LINTING
    _supports_statement_cache = False
    positional = False
    paramstyle = 'named'
    label_length = None
    supports_server_side_cursors = False
    requires_name_normalize = False

    statement_compiler = ChCompiler
    ddl_compiler = ChDDLCompiler
    type_compiler_cls = ChTypeCompiler
    preparer = ChIdentifierPreparer
    identifier_preparer = ChIdentifierPreparer
    execution_ctx_cls = ChExecutionContext
    inspector = ChInspector

    # def __init__(self, dbapi_=None, **kwargs):
    #     super().__init__(dbapi_, **kwargs)
    #     self.dbapi = dbapi_ or dbapi

    @classmethod
    def dbapi(cls):
        return dbapi

    def create_connect_args(self, url: URL):
        opts = url.translate_connect_args()
        opts.update(url.query)
        return ([], opts)

    def get_dialect_pool_class(self, url: URL) -> Type[Pool]:
        return NullPool

    def initialize(self, connection):
        pass

    def _builtin_onconnect(self):
        def on_connect(dbapi_connection, _connection_record):
            pass

        return on_connect

    def connect(self, *cargs: Any, **cparams: Any) -> DBAPIConnection:
        return self.dbapi.connect(*cargs, **cparams)

    def do_rollback(self, dbapi_connection: PoolProxiedConnection) -> None:
        dbapi_connection.rollback()

    def do_begin(self, dbapi_connection: PoolProxiedConnection) -> None:
        pass

    @util.non_memoized_property
    def loaded_dbapi(self):
        if self.dbapi is None:
            raise ImportError("DBAPI module is not set up")
        return self.dbapi

    @staticmethod
    def get_schema_names(connection, **_):
        return [row.name for row in connection.execute('SHOW DATABASES')]

    @staticmethod
    def has_database(connection, db_name):
        return (connection.execute(text('SELECT name FROM system.databases ' +
                                   f'WHERE name = {format_str(db_name)}'))).rowcount > 0

    def get_table_names(self, connection, schema=None, **kw):
        cmd = 'SHOW TABLES'
        if schema:
            cmd += ' FROM ' + quote_identifier(schema)
        return [row.name for row in connection.execute(cmd)]

    def get_primary_keys(self, connection, table_name, schema=None, **kw):
        return []

    def get_pk_constraint(self, connection, table_name, schema=None, **kw):
        return []

    def get_foreign_keys(self, connection, table_name, schema=None, **kw):
        return []

    def get_temp_table_names(self, connection, schema=None, **kw):
        return []

    def get_view_names(self, connection, schema=None, **kw):
        return []

    def get_temp_view_names(self, connection, schema=None, **kw):
        return []

    def get_view_definition(self, connection, view_name, schema=None, **kw):
        pass

    def get_indexes(self, connection, table_name, schema=None, **kw):
        return []

    def get_unique_constraints(self, connection, table_name, schema=None, **kw):
        return []

    def get_check_constraints(self, connection, table_name, schema=None, **kw):
        return []

    def has_table(self, connection, table_name, schema=None, **_kw):
        result = connection.execute(text(f'EXISTS TABLE {full_table(table_name, schema)}'))
        row = result.fetchone()
        return row[0] == 1

    def has_sequence(self, connection, sequence_name, schema=None, **_kw):
        return False

    def do_begin_twophase(self, connection, xid):
        raise NotImplementedError

    def do_prepare_twophase(self, connection, xid):
        raise NotImplementedError

    def do_rollback_twophase(self, connection, xid, is_prepared=True, recover=False):
        raise NotImplementedError

    def do_commit_twophase(self, connection, xid, is_prepared=True, recover=False):
        raise NotImplementedError

    def do_recover_twophase(self, connection):
        raise NotImplementedError

    def set_isolation_level(self, dbapi_conn, level):
        pass

    def get_isolation_level(self, dbapi_conn):
        return None

    def do_execute(
            self,
            cursor: DBAPICursor,
            statement: str,
            parameters: Optional[_DBAPISingleExecuteParams],
            context: Optional[ExecutionContext] = None,
    ) -> None:
        """Provide an implementation of ``cursor.execute(statement,
        parameters)``."""
        cursor.execute(statement, parameters)
