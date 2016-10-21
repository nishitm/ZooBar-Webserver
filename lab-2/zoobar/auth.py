from zoodb import *
from debug import *
from base64 import b64encode

import hashlib
import random
import pbkdf2


def newtoken(db, cred):
    hashinput = "%s%.10f" % (cred.password, random.random())
    cred.token = hashlib.md5(hashinput).hexdigest()
    db.commit()
    return cred.token

# def login(username, password):
#     db = person_setup()
#     person = db.query(Person).get(username)
#     if not person:
#         return None
#     if person.password == password:
#         return newtoken(db, person)
#     else:
#         return None

def login(username, password):
    db = cred_setup()
    person = db.query(Cred).get(username)
    
    if not person:
        return None

    salt=person.salt
    password=pbkdf2.PBKDF2(password,salt).hexread(32)

    if person.password == password:
        return newtoken(db, person)
    else:
        return None

# def register(username, password):
#     print "registring "
#     db = person_setup()
#     person = db.query(Person).get(username)
#     if person:
#         return None
#     newperson = Person()
#     newperson.username = username
#     newperson.password = password
#     db.add(newperson)
#     db.commit()
#     return newtoken(db, newperson)

def register(username, password):
    db = person_setup()
    db2 = cred_setup()
    #db3 = bank_setup()
    person = db.query(Person).get(username)

    if person:
        return None

    #generates 64 bit salt
    salt = b64encode(os.urandom(8)).decode('utf-8')
    newperson = Person()
    newperson2 = Cred()
    #newperson3 = Bank()
    
    #salt=unicode(salt)
    newperson2.salt=salt
    
    newperson.username = username
    newperson2.username = username
    #newperson3.username = username

    password=pbkdf2.PBKDF2(password,salt).hexread(32)
    newperson2.password = password

    db.add(newperson)
    db2.add(newperson2)
    #db3.add(newperson3)

    db.commit()
    db2.commit()
    #db3.commit()
    return newtoken(db2, newperson2)

# def check_token(username, token):
#     db = person_setup()
#     person = db.query(Person).get(username)
#     if person and person.token == token:
#         return True
#     else:
#         return False

def check_token(username, token):
    db = cred_setup()
    person = db.query(Cred).get(username)
    if person and person.token == token:
        return True
    else:
        return False

def get_token(username):
    db = cred_setup()
    person = db.query(Cred).get(username)
    if not person:
        raise ValueError("INVALID")
    else:
        return person.token