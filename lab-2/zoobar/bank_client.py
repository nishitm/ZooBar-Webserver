from debug import *
from zoodb import *
import rpclib

def balance(username):
    ## Fill in code here.
    with rpclib.client_connect('/banksvc/sock') as c:
        ret = c.call('balance',user = username)
        return ret

def transfer(sender, recipient, zoobars, token):
    try:
        with rpclib.client_connect('/banksvc/sock') as c:
            ret = c.call('transfer',sender = sender, recipient = recipient, zoobars = zoobars, token = token)
            return ret
    except Exception, e:
        raise ValueError("User NOt Found")

def register(username):
    with rpclib.client_connect('/banksvc/sock') as c:
        ret = c.call('register',user = username)
        return ret

def get_log(username):
    with rpclib.client_connect('/banksvc/sock') as c:
        ret = c.call('get_log',user = username)
        return ret