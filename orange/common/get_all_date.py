
# encoding: utf-8
from datetime import timedelta, datetime


def gen_dates(b_date, days):
    day = timedelta(days=1)
    for i in range(days):
        yield b_date + day*i


def get_date_list(start=None, end=None):

    startday = datetime.strptime(start, '%Y-%m-%d')
    endday = datetime.strptime(end, '%Y-%m-%d')
    if start is None:
        startday = datetime.strptime("2000-01-01", "%Y-%m-%d")
    if end is None:
        endday = datetime.now()
    data = []
    for d in gen_dates(startday, (endday-startday).days):
        g=str(d)
        h=(g.split(' '))[0]
        data.append(str(h))
    return data

