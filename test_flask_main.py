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
  memos = get_memos()

  to_destroy_str = "1,"
  to_destroy = to_destroy_str.strip(',').split(',')
  destroyed = []
  for index in to_destroy:
    destroyed.append(sorted_memos[int(index)-1])
  assert(destroy_helper(to_destroy_str) ==  destroyed)

  #if butto clicked but no boxes checked
  to_destroy_str = ""
  destroyed = []
  assert(destroy_helper(to_destroy_str) ==  destroyed)

  to_destroy_str = "1,5,"
  to_destroy = to_destroy_str.strip(',').split(',')
  destroyed = []
  for index in to_destroy:
    destroyed.append(sorted_memos[int(index)-1])
  assert(destroy_helper(to_destroy_str) ==  destroyed)


def test_humanize():
  """
  test humanization of dates
  """
  now = arrow.now()

  date = now.replace(days =- 2)
  assert(humanize_arrow_date(date) == "2 days ago" )

  date = now.replace(days =- 1)
  assert(humanize_arrow_date(date) == "Yesterday" )

  date = now.replace(days =- 0)
  assert(humanize_arrow_date(date) == "Today" )

  date = now.replace(days =+ 1)
  assert(humanize_arrow_date(date) == "Tomorrow" )

test_database_add()