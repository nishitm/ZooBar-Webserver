from debug import *
from zoodb import *
import rpclib

def login(username, password):
    ## Fill in code here.
    with rpclib.client_connect('/authsvc/sock') as c:
        ret = c.call('login',user = username,passd = password)
        return ret

def register(username, password):
    ## Fill in code here.
    with rpclib.client_connect('/authsvc/sock') as c:
        ret = c.call('register', user = username,passd = password)
        return ret

def check_token(username, token):
    ## Fill in code here.
    with rpclib.client_connect('/authsvc/sock') as c:
        ret = c.call('check_token',user = username,token = token)
        return ret

def get_token(username):
    ## Fill in code here.
    with rpclib.client_connect('/authsvc/sock') as c:
        ret = c.call('get_token',user = username)
        return ret
