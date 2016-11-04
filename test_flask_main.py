from flask_main import *
import arrow

def test_database_add():
    date = "2016-11-01"
    memo = "RANDOM TEXT"
    entry = database_entry(date, memo)
    assert(entry["date"] == arrow.get(date).replace(tzinfo = tz.tzlocal()).isoformat())
    assert(entry["text"] == memo)

    date = "2016-02-28"
    memo = "RANDOM TEXT 2"
    entry = database_entry(date, memo)
    assert(entry["date"] == arrow.get(date).replace(tzinfo = tz.tzlocal()).isoformat())
    assert(entry["text"] == memo)

    date = "2016-01-01"
    memo = ""
    entry = database_entry(date, memo)
    assert(entry["date"] == arrow.get(date).replace(tzinfo = tz.tzlocal()).isoformat())
    assert(entry["text"] == memo)

def test_database_delete():
    date = "2016-01-01"
    memo = ""
    for i in range(0,10):
        collection.insert(database_entry(date, memo))
    memos = get_memos()

    checkboxes = "1,3"
    test_delete = checkboxes.split(',')
    deleted = []
    for index in test_delete:
        deleted.append(memos[int(index)])
    assert(database_removal(checkboxes) ==  deleted)

    checkboxes = "2,5,"
    test_delete = checkboxes.split(',')
    deleted = []
    for index in test_delete:
        if index == '':
            break
        deleted.append(memos[int(index)])
    assert(database_removal(checkboxes) ==  deleted)

    checkboxes = ""
    deleted = []
    assert(database_removal(checkboxes) ==  deleted)


def test_humanize():
    date = arrow.now().replace(days =- 5)
    assert(humanize_arrow_date(date) == "5 days ago" )

    date = arrow.now().replace(days =- 1)
    assert(humanize_arrow_date(date) == "Yesterday" )

    date = arrow.now().replace(days =- 0)
    assert(humanize_arrow_date(date) == "Today" )

    date = arrow.now().replace(days =+ 1)
    assert(humanize_arrow_date(date) == "Tomorrow" )