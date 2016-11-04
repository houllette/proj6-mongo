"""
Flask web app connects to Mongo database.
Keep a simple list of dated memoranda.

Representation conventions for dates:
   - We use Arrow objects when we want to manipulate dates, but for all
     storage in database, in session or g objects, or anything else that
     needs a text representation, we use ISO date strings.  These sort in the
     order as arrow date objects, and they are easy to convert to and from
     arrow date objects.  (For display on screen, we use the 'humanize' filter
     below.) A time zone offset will
   - User input/output is in local (to the server) time.
"""

import flask
from flask import g
from flask import render_template
from flask import request
from flask import url_for
from flask import jsonify

import json
import logging
import sys

# Date handling
import arrow    # Replacement for datetime, based on moment.js
from dateutil import tz  # For interpreting local times

# Mongo database
import pymongo
from pymongo import MongoClient
import secrets.admin_secrets
import secrets.client_secrets
MONGO_CLIENT_URL = "mongodb://{}:{}@localhost:{}/{}".format(
    secrets.client_secrets.db_user,
    secrets.client_secrets.db_user_pw,
    secrets.admin_secrets.port,
    secrets.client_secrets.db)

###
# Globals
###
import CONFIG
app = flask.Flask(__name__)
app.secret_key = CONFIG.secret_key

####
# Database connection per server process
###

try:
    dbclient = MongoClient(MONGO_CLIENT_URL)
    db = getattr(dbclient, secrets.client_secrets.db)
    collection = db.dated

except:
    print("Failure opening database.  Is Mongo running? Correct password?")
    sys.exit(1)



###
# Pages
###

@app.route("/")
@app.route("/index")
def index():
  app.logger.debug("Main page entry")
  g.memos = get_memos()
  for memo in g.memos:
      app.logger.debug("Memo: " + str(memo))
  return flask.render_template('index.html')


@app.route("/create")
def create():
    app.logger.debug("Create Page")
    return flask.render_template('create.html')

@app.route("/database_add")
def database_add():
    app.logger.debug("Add to Database")
    date = request.args.get("date", type=str)
    memo = request.args.get("memo", type=str)
    collection.insert(database_entry(date, memo))
    rslt = { "key" : "test" }
    return jsonify(result = rslt)

@app.route("/database_delete")
def database_delete():
    app.logger.debug("Deleting from Database")
    checked = request.args.get("checked", type=str)
    remove = database_removal(checked)
    for memo in remove:
        collection.remove({'date': memo['date'], 'text': memo['text']})
    rslt = { "key" : "test" }
    return jsonify(result = rslt)

@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('page_not_found.html',
                                 badurl=request.base_url,
                                 linkback=url_for("index")), 404

#################
#
# Functions used within the templates
#
#################


@app.template_filter( 'humanize' )
def humanize_arrow_date( date ):
    """
    Date is internal UTC ISO format string.
    Output should be "today", "yesterday", "in 5 days", etc.
    Arrow will try to humanize down to the minute, so we
    need to catch 'today' as a special case.
    """
    try:
        then = arrow.get(date).to('local')
        now = arrow.utcnow().to('local')
        yesterday = now.replace(days =- 1)
        tomorrow  = now.replace(days =+ 1)
        if then.date() == now.date():
            human = "Today"
        elif then.date() == yesterday.date():
            human = "Yesterday"
        elif then.date() == tomorrow.date():
            human = "Tomorrow"
        else:
            human = then.humanize(now)
    except:
        human = date
    return human


#############
#
# Functions available to the page code above
#
##############
def get_memos():
    """
    Returns all memos in the database, in a form that
    can be inserted directly in the 'session' object.
    """
    records = [ ]
    for record in collection.find( { "type": "dated_memo" } ):
        record['date'] = arrow.get(record['date']).isoformat()
        del record['_id']
        records.append(record)
    records = sorted(records, key=lambda record: record['date'])
    return records

def database_entry(date, memo):
    """
    Forms entry suitable for database_entry
    """
    date = arrow.get(date).replace(tzinfo=tz.tzlocal())
    entry = {"type": "dated_memo", "date": date.isoformat(), "text": memo}
    return entry

def database_removal(checked):
    """
    Returns array of memos to be removed
    """
    memos = get_memos()
    checked = checked.split(',')
    remove = []
    for check in checked:
        if check == '':
            break
        remove.append(memos[int(check)])
    return remove

if __name__ == "__main__":
    app.debug=CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    app.run(port=CONFIG.PORT,host="0.0.0.0")


