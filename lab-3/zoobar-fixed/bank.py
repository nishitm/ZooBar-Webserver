from zoodb import *
from debug import *

import time

def transfer(sender, recipient, zoobars):
    persondb = person_setup()
    senderp = persondb.query(Person).get(sender)
    recipientp = persondb.query(Person).get(recipient)
    
    if zoobars < 0 or sender == recipient:                  #balance mismatch
        raise ValueError()

    sender_balance = senderp.zoobars - zoobars
    recipient_balance = recipientp.zoobars + zoobars

    if sender_balance < 0 or recipient_balance < 0:
        raise ValueError()

    senderp.zoobars = sender_balance
    recipientp.zoobars = recipient_balance
    persondb.commit()

    transfer = Transfer()
    transfer.sender = sender
    transfer.recipient = recipient
    transfer.amount = zoobars
    transfer.time = time.asctime()

    transferdb = transfer_setup()
    transferdb.add(transfer)
    transferdb.commit()

def balance(username):
    db = person_setup()
    person = db.query(Person).get(username)
    db2 = transfer_setup()
    bal = db2.query(Transfer).all()
    for i in bal:
        if getattr(i,'sender') == username:
            sender_balance = sender_balance - getattr(i,'amount')
        elif getattr(i,'recipient') == username:
            sender_balance = sender_balance + getattr(i,'amount')

    if person.zoobars == sender_balance:
        return person.zoobars
    else:
        raise ValueError()

def get_log(username):
    db = transfer_setup()
    return db.query(Transfer).filter(or_(Transfer.sender==username,
                                         Transfer.recipient==username))

