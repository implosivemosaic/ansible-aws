#
# Filter Collection Extensions for Ansible
#
# This filter plugin provides support for more complex collection-based
# mapping and filtering operations.
#
#
# Assume the following list and dict in all examples below:
#
# list: [{ a: 1, b: 2, c: {x: 100, y: 200} },
#        { a: 3, b: 4, c: {x: 300, y: 400} }]
#
# dict: { a: 1, b: 2, c: 3 }
#

from ansible import errors

def get_path_value(dict, path):
	subTree = dict
	try:
		if (path == None):
			return dict
		for key in path.split('.'):
			subTree = subTree[key]
		return subTree
	except KeyError:
		return None

def dict_merge(dict1, dict2):
	return dict(dict1.items() + dict2.items())

# Given a dictionary, return a list of its values.
# map_values(dict) -> [1, 2, 3]
def dict_values(dict):
	return [v for k, v in dict.iteritems()]

def merge(dict, template):
	return [template.format(key=k, value=v) for k,v in dict.iteritems()]

def sub(list, key):
	return [get_path_value(item) for item in list]

# Given a list of dictionaries, return a new list based on an
# attribute 'attr' with match criteria key == value.
# list_subfilter(list, None, 'c.x', 100) -> [{ a: 1, b: 2, c: {x: 100, y: 200} }]
# list_subfilter(list, 'c.x', 'c.y', 400) -> [300]
def list_subfilter(list, attr, key, value):
	return [v[get_path_value(attr)] for v in list if get_path_value(v, key) == value]

# Given a list of dictionaries, return a new list based on matching key == value
def list_filter(list, key, value):
	return [val for val in list if (value == "") or (get_path_value(val, key) == value)]

def list_flatten(list, key, retainers = []):
	return [ dict(item.items() + dict((k, v) for k, v in inner.iteritems() if k in retainers).items())
		for inner in list for item in (get_path_value(inner, key) or []) ]

def list_to_dict(list, key):
	return dict( [(get_path_value(item, key), item) for item in list] )

def list_to_dict_values(list, key, val):
	return dict( [(get_path_value(item, key), get_path_value(item, val)) for item in list] )

class FilterModule(object):

	def filters(self):
		return {
			'dict_values' : dict_values,
			'list_filter' : list_filter,
			'list_subfilter' : list_subfilter,
			'list_flatten' : list_flatten,
			'list_to_dict' : list_to_dict,
			'list_to_dict_values' : list_to_dict_values,
			'dict_merge' : dict_merge,
			'merge' : merge,
			'sub' : sub,
		}

