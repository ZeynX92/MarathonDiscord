def insert(cur, list, value):
    if list[0] in cur.keys():
        cur[list[0]].append(value)
        return
    elif len(list) == 1:
        cur[list[0]] = value
        return
    if list[0] not in cur.keys():
        cur[list[0]] = {}
    insert(cur[list[0]], list[1:], value)
