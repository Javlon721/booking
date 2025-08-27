from psycopg.sql import SQL, Composed, Placeholder

from src.db.sql_queries.utils import create_column_assignments

type QUERY_TYPE = Composed | SQL


def add_and_conditions(conditions: list[str]) -> Composed:
    """
         Example::

            >>> query = add_and_conditions(['column1', 'column2'])
            >>> print(query.as_string())
             where "column1" = %(column1)s and "column2" = %(column2)s

        :param conditions: dict of pair column names -> value to compare
        :return: Composed object with columns compared with equal sign
        """

    if not len(conditions):
        return Composed('')

    return SQL(' where ') + create_column_assignments(conditions, SQL(' and '))


def add_limit(limit: int = 0) -> Composed:
    """
     Example::

        >>> query = add_limit(10, 5)
        >>> print(query.as_string())
         limit %(limit)s offset %(offset)s

    """
    if limit < 1:
        return Composed('')
    return SQL(' limit {} offset {}').format(Placeholder("limit"), Placeholder("offset"))


if __name__ == '__main__':
    data = {
        'first_name': 'Sophie',
        'last_name': 'Hillett',
    }
    print(add_and_conditions(list(data.keys())).as_string())
