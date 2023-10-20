from mysql.connector import connect

conn = connect(
    host="localhost",
    user="root",
    password="",
    database="uhrs"
)
query = conn.cursor(dictionary=True)


def Listing(table, columns=None, condition=None, order=None, single=False):
    _tableName = table
    _columns = ""
    _condition = ""
    _order = ""

    """Get all columns"""
    if columns != None:
        for column in columns:
            _columns += f"{column}, "
        _columns = _columns[:-2]
    else:
        _columns = "*"

        "Select * "

    """Get condition values"""
    if condition != None:
        _condition = "WHERE "
        _condition_keys = condition.keys()
        for key in _condition_keys:
            _condition += f"({key} = %s) AND "
        _condition = _condition[:-5]
    else:
        _condition = ""

    """Get order values"""
    if order != None:
        _order = "ORDER BY "
        for key, value in order.items():
            _order += f"{key} {value}, "
        _order = _order[:-2]
    else:
        _order = "ORDER by id"

    """Create sql query"""
    sql = f"SELECT {_columns} FROM {_tableName} {_condition} {_order}"

    if condition != None:
        query.execute(sql, tuple(condition.values()))
    else:
        query.execute(sql)

    if single:
        data = query.fetchone()
    else:
        data = query.fetchall()
    return data


def Delete(table, condition=None):
    _tableName = table
    _condition = ""

    """Get condition values"""
    if condition != None:
        _condition = "WHERE "
        _condition_keys = condition.keys()
        for key in _condition_keys:
            _condition += f"({key} = %s) AND "
        _condition = _condition[:-5]
    else:
        _condition = ""

    """Create sql query"""
    sql = f"DELETE FROM {_tableName} {_condition}"

    if condition != None:
        _condition_values = tuple(condition.values())
    else:
        _condition_values = None

    query.execute(sql, _condition_values)
    conn.commit()
    data = query.rowcount
    return data


def Create(table, columns):
    _tableName = table
    _column_keys = ""
    _column_values = ""

    """Get columns keys"""
    for key in columns.keys():
        _column_keys += f"{key}, "
    _column_keys = _column_keys[:-2]

    """Get columns keys"""
    _columns_keys = columns.keys()
    for key in _columns_keys:
        _column_values += "%s, "
    _column_values = _column_values[:-2]

    """Create sql query"""
    sql = f"INSERT INTO {_tableName} ({_column_keys}) VALUES ({_column_values})"

    data = query.execute(sql, tuple(columns.values()))
    conn.commit()
    data = query.lastrowid
    return data


def Update(table, columns, condition=None):
    _tableName = table
    _columns = ""
    _condition = ""

    """Get columns keys"""
    for key in columns.keys():
        _columns += f"{key}=%s, "
    _columns = _columns[:-2]

    """Get condition values"""
    if condition != None:
        _condition = "WHERE "
        _condition_keys = condition.keys()
        for key in _condition_keys:
            _condition += f"({key} = %s) AND "
        _condition = _condition[:-5]
    else:
        _condition = ""

    """Create sql query"""
    sql = f"UPDATE {_tableName} SET {_columns} {_condition}"
    values = tuple(columns.values()) + tuple(condition.values())
    data = query.execute(sql, values)
    conn.commit()
    data = query.rowcount
    return data
