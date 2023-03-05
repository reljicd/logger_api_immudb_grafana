import os

POSTGRES_HOST: str = os.getenv(key='POSTGRES_HOST', default='localhost')
POSTGRES_PORT: int = int(os.getenv(key='POSTGRES_PORT', default='5432'))
POSTGRES_DB: str = os.getenv(key='POSTGRES_DB', default='logger_api')
POSTGRES_USER: str = os.getenv(key='POSTGRES_USER', default='logger_api')
POSTGRES_PASSWORD: str = os.getenv(key='POSTGRES_PASSWORD', default='password')
