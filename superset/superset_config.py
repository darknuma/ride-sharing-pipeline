import os

MAPBOX_API_KEY = os.getenv('MAPBOX_API_KEY', '')

# Pinot connection configuration
PREFERRED_DATABASES = ['pinot']

# Add Pinot to the databases
DATABASES = {
    'pinot': {
        'allow_csv_upload': False,
        'allow_ctas': False,
        'allow_cvas': False,
        'allow_dml': False,
        'allow_multi_schema_metadata_fetch': False,
        'allow_run_async': False,
        'allows_subquery': True,
        'disable_data_preview': False,
        'expose_in_sqllab': True,
        'force_ctas_schema': None,
        'parameters': {
            'broker_host': 'pinot-broker',
            'broker_port': 8099,
            'controller_host': 'pinot-controller',
            'controller_port': 9000,
        }
    }
}

# Cache configuration
CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_KEY_PREFIX': 'superset_',
}

# Additional security settings
SECRET_KEY = os.getenv('SUPERSET_SECRET_KEY', 'your_secure_key_here')