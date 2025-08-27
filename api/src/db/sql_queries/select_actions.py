from typing import Iterable

from psycopg.sql import SQL, Identifier, Composed

from src.db.sql_queries.columns import columns_from

type QUERY_TYPE = Composed | SQL


def select_from_table(columns: Iterable[str] | str, table_name: str) -> Composed:
    """
    Example::

        >>> query = select_from_table([
        ... 'column1',
        ... 'column2'
        ... ], 'table_name1')
        >>> print(query.as_string())
        select "column1", "column2" from "table_name1"

    :param columns: sequence of column names
    :param table_name: db table name
    :return: returns sql query
    """
    template = SQL('select {columns} from {table_name}')
    if isinstance(columns, str):
        result_columns = SQL('*')
    else:
        result_columns = columns_from(columns)
    return template.format(
        columns=result_columns,
        table_name=Identifier(table_name)
    )


if __name__ == '__main__':
    # print((columns_from(['author', 'title', 'publisher', 'year']) + SQL('')).as_string())
    # print(add_and_conditions({
    #     'first_name': 'Sophie',
    #     'last_name': 'Hillett',
    # }
    # ).as_string())
    print((select_from_table(['title', "book_id"], 'book')).as_string())

    # print(str(Composed([add_limit(10, 2), SQL('')])))
