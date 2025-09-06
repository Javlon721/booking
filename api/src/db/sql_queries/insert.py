from psycopg.sql import Identifier, SQL, Composed, Placeholder

from src.db.sql_queries.columns import columns_from
from src.db.sql_queries.utils import get_returning_values


def insert_into(table: str, columns: list[str], *, returning: list[str] | None = None) -> Composed:
    template = SQL('insert into {table} ({coumns}) values ({values}) returning {return_vals}')
    return_vals = get_returning_values(returning)
    return template.format(
        table=Identifier(table),
        coumns=columns_from(columns),
        values=SQL(', ').join(map(Placeholder, columns)),
        return_vals=return_vals
    )


if __name__ == '__main__':
    data = {
        'column1': 'value1', 'column2': 'value2'
    }
    print(insert_into('table_name', list(data.keys()), 'user_id').as_string())
