from disnake.ext.commands import BadArgument


def getseconds(string):
    b = ''
    a = ''
    for i in string:
        try:
            i = int(i)
            a = a + str(i)
        except:
            b = b + i
    if b == 'm':
        return int(a) * 60
    elif b == 's':
        return int(a)
    elif b == 'h':
        return int(a) * 3600
    elif b == 'd':
        return int(a) * 86400
    elif b == 'w':
        return int(a) * 604800
    elif b == 'y':
        return int(a) * 31536000
    else:
        raise BadArgument()
