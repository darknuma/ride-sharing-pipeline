from sqlalchemy.dialects.postgresql.base import PGDialect
from sqlalchemy.engine.default import DefaultDialect
from sqlalchemy.sql import compiler
from sqlalchemy import types
import urllib.parse

class PinotDialect(DefaultDialect):
    """SQLAlchemy dialect for Apache Pinot"""
    
    name = 'pinot'
    driver = 'http'
    
    # Map Python types to SQLAlchemy types
    ischema_names = {
        'STRING': types.String,
        'INT': types.Integer,
        'LONG': types.BigInteger,
        'FLOAT': types.Float,
        'DOUBLE': types.Float,
        'BOOLEAN': types.Boolean,
        'TIMESTAMP': types.DateTime,
        'JSON': types.JSON
    }
    
    @classmethod
    def dbapi(cls):
        """Pinot doesn't have a native Python driver, so we'll use requests"""
        import requests
        return requests
    
    def create_connect_args(self, url):
        """Convert SQLAlchemy connection URL to Pinot query parameters"""
        # Parse the connection URL
        controller_url = url.query.get('controller', '')
        query_options = {k: v for k, v in url.query.items() if k != 'controller'}
        
        connect_args = {
            'broker_url': f"{url.host}:{url.port}/query",
            'controller_url': controller_url,
            'query_params': query_options
        }
        
        return ([], connect_args)
    
    def get_pool_class(self, url):
        """Use SQLAlchemy's QueuePool for connection pooling"""
        from sqlalchemy.pool import QueuePool
        return QueuePool
    
    def _get_default_schema_name(self, connection):
        """Return default schema name"""
        return 'default'

# Optional: Custom SQL compiler if needed
class PinotCompiler(compiler.SQLCompiler):
    def visit_select(self, select, **kw):
        """Customize SELECT statement compilation if required"""
        return super().visit_select(select, **kw)

# Registration decorator for SQLAlchemy entry points
def register_dialect():
    from sqlalchemy.dialects import registry
    registry.register("pinot.http", "pinot_dialect", "PinotDialect")

# Example usage function
def example_connection():
    from sqlalchemy import create_engine
    
    # Connection string format
    connection_string = (
        "pinot+http://localhost:8099/query"
        "?controller=http://localhost:9000"
    )
    
    engine = create_engine(connection_string)
    return engine

