from sqlalchemy import Update
from sqlalchemy.sql import compiler


class ChCompiler(compiler.SQLCompiler):
    def visit_update(self, update_stmt: Update, **_):
        table = self.process(update_stmt.table, asfrom=True)
        text = f'ALTER TABLE {table} UPDATE '
        text += ', '.join(
            f'{self.process(c[0], include_table=False)} = {self.process(c[1])}' for c in update_stmt._values.items()
        )
        if update_stmt.whereclause is not None:
            text += f' WHERE {self.process(update_stmt.whereclause, include_table=False)}'
        return text
