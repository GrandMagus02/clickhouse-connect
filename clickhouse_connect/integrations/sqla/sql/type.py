from sqlalchemy.sql.compiler import StrSQLTypeCompiler


class ChTypeCompiler(StrSQLTypeCompiler):
    # def process(self, type_, **kw):
    #     try:
    #         _compiler_dispatch = type_._compiler_dispatch
    #     except AttributeError:
    #         return self._visit_unknown(type_, **kw)
    #     else:
    #         return _compiler_dispatch(self, **kw)
    #
    # def _visit_unknown(self, type_, **kw):
    #     if type_.__class__.__name__ == type_.__class__.__name__.upper():
    #         return type_.__class__.__name__
    #     else:
    #         return repr(type_)
    pass
