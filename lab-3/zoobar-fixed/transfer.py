from flask import g, render_template, request

from login import requirelogin
from zoodb import *
from debug import *
import threading
import bank
import traceback

@catch_err
@requirelogin
def transfer():
    warning = None
    try:
        if 'recipient' in request.form:
            zoobars = symint(request.form['zoobars'])
            lock = threading.Lock()
            lock.acquire()
            bank.transfer(g.user.person.username,
                          request.form['recipient'], zoobars)
            lock.release()
            warning = "Sent %d zoobars" % zoobars
    except (KeyError, ValueError, AttributeError) as e:
        traceback.print_exc()
        warning = "Transfer to %s failed" % request.form['recipient']

    return render_template('transfer.html', warning=warning)
