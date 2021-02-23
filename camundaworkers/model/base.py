from os import environ
from sqlalchemy import create_engine


def create_sql_engine():
    pg_user = environ.get('POSTGRES_USER')
    pg_psw = environ.get('POSTGRES_PASSWORD')

    print(f"create_sql_engine - USER: {pg_user}, PASSWORD: {pg_psw}")
    return create_engine(f'postgresql://{pg_user}:{pg_psw}@acmesky_db:5432/acmesky')
