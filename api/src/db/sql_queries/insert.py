from psycopg.sql import Identifier, SQL, Composed, Placeholder

from src.db.sql_queries.columns import columns_from


def insert_into(table: str, columns: list[str], returning: str) -> Composed:
    template = SQL('insert into {table} ({coumns}) values ({values}) returning {return_vals}')
    if returning == "*":
        return_vals = SQL("*")
    else:
        return_vals = Identifier(returning)
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
