#!/usr/bin/python
#
# Insert bank server code here.
#
import rpclib
import sys
import bank
import auth_client
from debug import *

class BankRpcServer(rpclib.RpcServer):
	def rpc_balance(self, user):
		return bank.balance(user)

	def rpc_get_log(self, user):
		return bank.get_log(user)

	def rpc_transfer(self, sender, recipient, zoobars, token):
		if not auth_client.check_token(sender, token):
			raise ValueError("Invalid")

		return bank.transfer(sender, recipient, zoobars)

	def rpc_register(self, user):
		return bank.register(user)

## Fill in RPC methods here.
#pass

(_, dummy_zookld_fd, sockpath) = sys.argv

s = BankRpcServer()
s.run_sockpath_fork(sockpath)