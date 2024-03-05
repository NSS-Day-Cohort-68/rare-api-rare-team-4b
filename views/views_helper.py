# custom dictionary row factory for SQLite
def dict_factory(cursor, row):
    out = {}
    for i, col in enumerate(cursor.description):
        out[col[0]] = row[i]
    return out
