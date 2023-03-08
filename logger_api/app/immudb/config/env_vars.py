import os

IMMUDB_HOST: str = os.getenv(key='IMMUDB_HOST', default='localhost')
IMMUDB_PORT: int = int(os.getenv(key='IMMUDB_PORT', default='3322'))
IMMUDB_DB: str = os.getenv(key='IMMUDB_DB', default='logger')
IMMUDB_USER: str = os.getenv(key='IMMUDB_USER', default='immudb')
IMMUDB_PASSWORD: str = os.getenv(key='IMMUDB_PASSWORD', default='password')
