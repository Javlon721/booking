from typing import Iterable

from psycopg.sql import SQL, Identifier, Composed


def columns_from(columns: Iterable[str]) -> Composed:
    """
    Example::

        >>> query = columns_from(['column1', 'column2'])
        >>> print(query.as_string())
        "column1", "column2"

    :param columns: table column/columns
    :return: Composed object with columns identifiers
    """
    return SQL(', ').join(map(Identifier, columns))


if __name__ == '__main__':
    print((columns_from(['author', 'title', 'publisher', 'year']) + SQL('')).as_string())
