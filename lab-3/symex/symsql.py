## This module wraps SQLalchemy's methods to be friendly to
## symbolic / concolic execution.

import fuzzy
import sqlalchemy.orm

oldget = sqlalchemy.orm.query.Query.get
def newget(query, primary_key):
  ## Exercise 5: your code here.
  ##
  ## Find the object with the primary key "primary_key" in SQLalchemy
  ## query object "query", and do so in a symbolic-friendly way.
  ##
  ## Hint: given a SQLalchemy row object r, you can find the name of
  ## its primary key using r.__table__.primary_key.columns.keys()[0]
  print primary_key;
  x = query.all()
  for q in x:
    key = q.__table__.primary_key.columns.keys()[0]
    # print getattr(q,x),"--<"
    key2 = getattr(q,key)
    # a = fuzzy.__contains__(primary_key,key2)
    # print "a-->",a
    if(primary_key == key2):
      return q
       # print "loll"

  # key = r.__table__.primary_key.columns.keys()[0]
  return None

sqlalchemy.orm.query.Query.get = newget
