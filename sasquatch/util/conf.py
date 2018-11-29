import json
import os
from collections import namedtuple
from collections.abc import Iterable, Mapping
from functools import partial
from itertools import chain, zip_longest

from pathlib import PosixPath
from configparser import ConfigParser
from .arg import parse_args
import six
import yaml

from sasquatch import __name__ as pkg_name
from sasquatch import __version__ as pkg_version
from .log import parse_loglvl
from pprint import pprint
# Module level config at bottom

# Sane default values for most things
BUILTIN_DEFAULTS = {
	'meta': {
		'name': pkg_name,
		'version': pkg_version,
		'author': 'Taylor McKinnon',
		'contact':'mail@tmacs.space'
	},
	'logging': {
		"logfile" : None,
		"loglvl" : "debug",
		"log_rotation": False,
		"logfmt" : '%(asctime)s %(name)s %(levelname)s: %(message)s',
		"datefmt" : '%d-%m-%y %I:%M:%S %p',
		'whitelist': [],
		'blacklist': [],
		},
}

# A place for your application specific defaults to live
# Overrides BUILT_IN_DEFAULTS
APP_DEFAULTS = {
	'profiles': {},
	'runtime': {
		'file': None,
		'script': None,
		'version_flag': False,
		'credentials': {
			'profile': None,
			'aws_access_key_id': None,
			'aws_secret_access_key': None,
			'endpoint': None,
		},
	}
  }


# Util functions

def safe_load(func, path):
	try:
		with open(path) as configFile:
			return func(configFile)
	except Exception as e:
		print(e)
	return None


def load_file(path, loaders, default_loader):
	loader = loaders.get(path.suffix, default_loader)
	return safe_load(loader, path)

def look_for_file(filename, paths):
	'''
	Tries to smartly find the absolute path of a config file.
	If the given path is absolute and exists return it unmodified, otherwise do usual leaf based lookup
	If the given path contains only a file name check for existence in _SEARCH_DIRS returning if found
	If the given path contains a relative filepath check for existence in _SEARCH_DIRS joining each with the fragement
	'''
	filename = PosixPath(filename)
	if filename.is_absolute():
		if filename.exists():
			return filename
		return None
	for confDir in paths:
		if confDir.joinpath(filename).exists():
			return confDir.joinpath(filename).resolve()
	return None

def _is_mapping(data):
	return isinstance(data, Mapping)

def _is_iterable(data):
	return not isinstance(data, six.string_types) and isinstance(data, Iterable)

def recurse_update(orig, new):
	'''
	Given a nested dict/list combo, walk each and update orig with new,
	overwiting keys, and positions
	'''
	if orig is None:
		return new
	elif new is None:
		return orig
	elif type(orig) != type(new):
		return new
	# Check for strings specifically because they cause problems with lists
	elif isinstance(orig, six.string_types) and isinstance(new, six.string_types):
		return new
	elif isinstance(orig, Mapping) and isinstance(new, Mapping):
		return {
			k: recurse_update(
				orig.get(k),
				new.get(k)
			) for k in set(
				chain(
					orig.keys(),
					new.keys()
				)
			)
		}
	elif isinstance(orig, Iterable) and isinstance(new, Iterable):
		return [recurse_update(o, n) for o, n in zip_longest(orig, new)]
	return new

def get_from_env(key, default = None):
	print(key)
	return os.environ.get(key, default)

_ROOT_PKG = pkg_name.upper()

def update_from_env(orig, namespace = [_ROOT_PKG]):
	if _is_mapping(orig):
		return {
			k: update_from_env(
				v, namespace + [ k.upper() ]
			) for k, v in orig.items()
		}
	elif _is_iterable(orig):
		return [
			update_from_env(
				v, namespace + [ str(i) ]
			) for i, v in enumerate(orig)
		]
	return get_from_env('_'.join(namespace), orig)

def create_namespace(data, name = 'config'):
	# pprint(data)
	if _is_mapping(data):
		mapping = { k: create_namespace(v, k) for k, v in data.items() }
		return namedtuple(name, list(mapping.keys()))(**mapping)
	elif _is_iterable(data):
		return tuple(create_namespace(v, str(i)) for i, v in enumerate(data))
	else:
		return data

# Module level config to control the behavior of configuration loading
MODULE_CONFIG = {
	'dump': False, # Writes the default config to disk if no config is found
	'load_from_file': True, # Master switch for config file loading, if False only use builtin values
	'load_from_home': True, # Load from ~/.<pkg_name>
	'load_from_env': True,  # Override config values with those from the environment
	'conf_path_from_env': True, # Load the path the the config dir/path from env
	'load_from_pwd': True, # Load config from the current directory
	'extra_search_dirs' : [], # Search theses dirs first
	'base_filename': pkg_name, # Searches `pkgname` `.pkgname` `.pkgname.<ext>` `<pkgname.<ext>`
	# Maps extensions to loaders
	# loaders should expect a file obj and return a dict
	'file_loaders': {
		'.yaml': yaml.load,
		'.yml': yaml.load,
		'.json': json.load,
	},
	'default_loader': yaml.load, # Used for file without extensions
	# Functions should expect no arguments and return a dict
	'additional_loaders': []
}

def loader(*args, **kwargs):
	def dec(f):
		func = partial(f, *args, **kwargs)
		MODULE_CONFIG['additional_loaders'].append(func)
		return f
	return dec


# Config path load order -Not to be edited manually!
_SEARCH_DIRS = []
_FILENAMES = []
_FILEPATHS = []

# Search extra directories first
_SEARCH_DIRS += MODULE_CONFIG['extra_search_dirs']
_SEARCH_DIRS = [PosixPath(p) for p in _SEARCH_DIRS]

if MODULE_CONFIG['conf_path_from_env']:
	path = os.environ.get('%s_CONF_PATH'%pkg_name.upper())
	if path:
		path = Posixpath(path).resolve()
		if path.is_dir(): # If we have a directory
			_SEARCH_DIRS.append(path) # Add it to _SEARCH_DIRS
		else: # Otherwise add it to explicit filenames
			_FILEPATHS.append(path)

if MODULE_CONFIG['load_from_pwd']:
	_SEARCH_DIRS.append(PosixPath('.'))

if MODULE_CONFIG['load_from_home']:
	_SEARCH_DIRS.append(PosixPath(os.path.expanduser('~')))

_SEARCH_DIRS = [p.resolve() for p in _SEARCH_DIRS if p.resolve().exists()]

_FILENAMES = ['.' + MODULE_CONFIG['base_filename']]
for ext in MODULE_CONFIG['file_loaders'].keys():
	_FILENAMES.append(''.join([MODULE_CONFIG['base_filename'], ext]))
	_FILENAMES.append(''.join(['.', MODULE_CONFIG['base_filename'], ext]))

for directory in _SEARCH_DIRS:
	for filename in _FILENAMES:
		_FILEPATHS.append(directory.joinpath(filename).resolve())

_FILEPATHS = [fn for fn in _FILEPATHS if fn.exists()]

@loader()
def aws_credentials():
	creds_path = PosixPath(os.path.expanduser('~/.aws/credentials'))
	if creds_path.exists():
		parser = ConfigParser()
		parser.read(creds_path)
		profiles = {s.replace('-', '_'):dict(parser.items(s)) for s in parser.sections()}
		return dict(profiles=profiles)
	return dict()


@loader()
def cli_loader():
	return parse_args(pkg_name)

def load_config(modconf):
	# Sort out our defaults
	conf = recurse_update(BUILTIN_DEFAULTS, APP_DEFAULTS)
	if modconf['load_from_file']:
		# Iter over our found config files loading each one
		# Do it in reverse so that our highest priority one gets applies last
		for filepath in reversed(_FILEPATHS):
			conf = recurse_update(
						conf,
						load_file(
							filepath,
							MODULE_CONFIG['file_loaders'],
							MODULE_CONFIG['default_loader']
						)
					)
	for loader in MODULE_CONFIG['additional_loaders']:
		conf = recurse_update(conf, loader())
	if modconf['load_from_env']:
		conf = update_from_env(conf)
	conf['logging']['loglvl'] = parse_loglvl(conf['logging']['loglvl']) # Parse the loglvl
	return create_namespace(conf)

config = load_config(MODULE_CONFIG)
