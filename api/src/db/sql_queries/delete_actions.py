from psycopg.sql import SQL, Identifier, Composed

from src.db.sql_queries.conditions import add_and_conditions
from src.db.sql_queries.utils import is_query_empty, get_returning_values


def delete_row(conditions: list[str], table_name: str, *, returning: list[str] | None = None) -> Composed:
    and_conditions = add_and_conditions(conditions)
    return_vals = get_returning_values(returning)

    if is_query_empty(and_conditions):
        raise ValueError('conditions in "delete_row" fn must not be empty')
    return SQL('delete from {table_name} {conditions} returning {return_vals}').format(
        table_name=Identifier(table_name),
        conditions=and_conditions,
        return_vals=return_vals
    )


if __name__ == '__main__':
    data = [
        {
            'books_id': 10,
            'author_id': 1,
            'title': 'blablabla'
        },
        {
            'books_id': 4,
        },
        {
            'books_id': 8,
        },
        {
            'books_id': 41,
        },
    ]
    print(delete_row(list(data[0].keys()), 'author').as_string())
