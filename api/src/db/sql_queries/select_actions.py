from psycopg.sql import SQL, Identifier, Composed

from src.db.sql_queries.utils import get_returning_values

type QUERY_TYPE = Composed | SQL


def select_from_table(table_name: str, columns: list[str] | None = None) -> Composed:
    """
    Example::

        >>> query = select_from_table(
        ... 'table_name1', [
        ... 'column1',
        ... 'column2'
        ... ])
        >>> print(query.as_string())
        select "column1", "column2" from "table_name1"

    :param columns: sequence of column names
    :param table_name: db table name
    :return: returns sql query
    """
    template = SQL('select {columns} from {table_name}')
    return_vals = get_returning_values(columns)

    return template.format(
        columns=return_vals,
        table_name=Identifier(table_name)
    )


if __name__ == '__main__':
    # print((columns_from(['author', 'title', 'publisher', 'year']) + SQL('')).as_string())
    # print(add_and_conditions({
    #     'first_name': 'Sophie',
    #     'last_name': 'Hillett',
    # }
    # ).as_string())
    print((select_from_table('book', ['title', "book_id"])).as_string())

    # print(str(Composed([add_limit(10, 2), SQL('')])))
