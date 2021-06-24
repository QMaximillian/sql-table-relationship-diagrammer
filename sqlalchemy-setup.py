from sqlalchemy import create_engine, text

querymap = {
    "psql": {
        "get_tables":
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema='public'
            AND table_type='BASE TABLE'
            """,
        "get_columns": lambda table: (
            f"""
            SELECT *
            FROM INFORMATION_SCHEMA.columns
            WHERE table_name = '{table}'
            """
        ),
        "get_table_constraints": lambda table: (
            f"""
                SELECT *
                FROM INFORMATION_SCHEMA.table_contraints
                WHERE table_name = '{table}'
            """
        )
    }
}
engine = create_engine(
    'postgresql+psycopg2://quinnlashinsky:quinnlashinsky@localhost/quizletdev')

with engine.connect() as connection:
    result = connection.execute(text(querymap["psql"]["get_tables"]))
    for row in result:

        if row[0] != 'knex_migrations' and row[0] != 'knex_migrations_lock':
            result = connection.execute(
                text(querymap["psql"]["get_columns"](row[0])))
            print(result)
