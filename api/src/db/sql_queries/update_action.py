from psycopg.sql import Composed, SQL, Identifier

from src.db.sql_queries.conditions import add_and_conditions
from src.db.sql_queries.utils import create_column_assignments, is_query_empty, get_returning_values


def update_row(columns: list[str], conditions: list[str], table_name: str, *,
               placeholder_postfix: str = '', returning: list[str] | None = None) -> Composed:
    and_conditions = add_and_conditions(conditions)
    values = create_column_assignments(columns, SQL(', '), placeholder_postfix=placeholder_postfix)

    if is_query_empty(and_conditions) or is_query_empty(values):
        raise ValueError('conditions or values in "update_row" fn must not be empty')

    statement = SQL('update {table_name} set {values} {conditions} returning {return_vals}')

    return statement.format(table_name=Identifier(table_name), values=values, conditions=and_conditions,
                            return_vals=get_returning_values(returning))


if __name__ == '__main__':
    new_data = {
        'column1': 'value1',
        'column2': 'value2'
    }
    conditions = {
        'id': 'id1',
        'column1': 'title1',
        'column2': 'title2',
    }
    print(update_row(list(new_data.keys()), list(conditions.keys()), 'table_name').as_string())
