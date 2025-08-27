from psycopg.sql import Composed, SQL, Identifier, Placeholder


def create_column_assignments(columns: list[str], join_by: SQL, *, placeholder_postfix: str = '') -> Composed:
    if is_query_empty(join_by):
        raise ValueError('join_by must not be empty')
    statement = SQL('{col_name} = {value}')
    items = [statement.format(col_name=Identifier(col_name),
                              value=Placeholder(col_name + placeholder_postfix)) for col_name in columns]
    return join_by.join(items)


def is_query_empty(query: Composed | SQL) -> bool:
    return query.as_string() == ''


def concat_sql_queries(*queries: Composed) -> Composed:
    return Composed(queries)


if __name__ == '__main__':
    print(create_column_assignments([], SQL(' ')).as_string())
