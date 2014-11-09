import hashlib
import os
from base64 import encodestring as encode

DOCUMENTATION = '''

'''

def ssha1(data):
	salt = os.urandom(4)
	hash = hashlib.sha1(data)
	hash.update(salt)

	return encode(hash.digest() + salt).strip()

class FilterModule(object):

	def filters(self):
		return {
			'ssha1' : ssha1,
		}

