# 构建倒排索引
import datetime

from entity.global_entity import *

# 目前只实现了and功能
from service.utils import transform_postfix


# boolean搜索
def search(keywords, source=None, date_begin=None, date_end=None, interval=None):
    if len(keywords) == 0:
        return set()
    postfix = transform_postfix(keywords)
    if (not date_begin or not date_end) and interval:
        date_end = datetime.datetime.now()
        n, unit = interval.split()
        if unit == "week":
            date_begin = date_end - datetime.timedelta(weeks=int(n))
        elif unit == "day":
            date_begin = date_end - datetime.timedelta(days=int(n))
        elif unit == "month":
            date_begin = date_end - datetime.timedelta(days=30 * int(n))
    stk = []
    for elem in postfix:
        if elem != "|" and elem != "&":
            stk.append(set(global_db.query_doc_ids_by_word(elem)))
        elif elem == "|":
            tmp = stk[-1].union(stk[-2])
            stk.pop()
            stk.pop()
            stk.append(tmp)
        else:
            tmp = stk[-1].intersection(stk[-2])
            stk.pop()
            stk.pop()
            stk.append(tmp)
    doc_ids = stk[-1]
    docs = global_db.query_specific(doc_ids, date_begin, date_end, source)
    return docs


def test_boolean_and():
    print(search("senior&official|test"))
