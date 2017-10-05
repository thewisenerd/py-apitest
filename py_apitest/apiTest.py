#!/usr/bin/env python

# -*- coding: utf-8 -*-

import os
import sys
import imp

import requests
import json
import jsonschema

from .helpers import print, nukeline, info, success, error

def getvar(g, key):
	if key in g:
		return g[key];
	return None

def setvar(g, key, var):
	g[key] = var;

def iterable(d, g):
	for k, v in d.items():
		if isinstance(v, dict):
			d[k] = iterable(v)
		elif isinstance(v, list):
			d[k] = map(lambda x: iterable(x), v)
		else:
			if callable(v):
				d[k] = getvar(g, v.args[0])
			else:
				d[k] = v
	return d


def runtest(FILE, baseurl, g, count, total):
	info('[%02d/%02d] initializing [%s]' % (count, total, FILE))
	try:
		# yay for backwards compatibility.
		# deal with this when it is actually removed.
		# really.
		testFILE = imp.load_source('*', FILE)
	except Exception as e:
		nukeline();
		error('[%02d/%02d] error initializing [%s]\n' % (count, total, FILE))
		print('\n' + ('-' * 80) + '\n')
		print(e)
		print('\n' + ('-' * 80) + '\n')
		return False

	if (not hasattr(testFILE, 'test')) or (not 'cases' in testFILE.test):
		nukeline();
		error('[%02d/%02d] error initializing [%s] : does not have required attrs\n' % (count, total, FILE))
		return False

	desc = '' if not 'desc' in testFILE.test else (' : %s' % testFILE.test['desc']);
	nukeline();
	info('[%02d/%02d] running [%s]%s' % (count, total, FILE, desc))

	for case in testFILE.test['cases']:
		if 'payload' in case:
			payload = case['payload']

			# fix variables
			if ('globals' in case):
				if ('requires' in case['globals']):
					for r in case['globals']['requires']:
						if (not r in g):
							nukeline();
							error('[%02d/%02d] error running [%s] : required variable `%s` not set\n' % (count, total, FILE, r))
							return

				# iterate over payload
				payload = iterable(payload, g);
			# globals in case
		# payload in case

		# get response
		if (case['method'] == 'GET'):
			if 'payload' in case:
				req = requests.get(baseurl + testFILE.test['url'], params=payload)
			else:
				req = requests.get(baseurl + testFILE.test['url'])
		else: # todo: handle more cases here
			if 'payload' in case:
				req = requests.post(baseurl + testFILE.test['url'], data=payload)
			else:
				req = requests.post(baseurl + testFILE.test['url'])

		try:
			res = case['response']
			assert (req.status_code == res['status_code']), "status code mismatch"
			assert (req.headers['content-type'] == res['content-type']), "content-type mismatch"

			body = case['response']['body']

			# if resp is json
			if body['type'] == 'json' and 'schema' in body:
				r = req.json()

				def buildrequired(schema):
					if schema['type'] == 'object' and 'properties' in schema:
						schema['additionalProperties'] = False;
						schema['minProperties'] = len(schema['properties'])

						for k,v in schema['properties'].items():
							if v['type'] == 'object':
								schema['properties'][k] = buildrequired(v)

					return schema

				schema = buildrequired(body['schema'])
				jsonschema.validate(r, schema)

				def ordered(obj):
					if isinstance(obj, dict):
						return sorted((k, ordered(v)) for k, v in obj.items())
					if isinstance(obj, list):
						return sorted(ordered(x) for x in obj)
					else:
						return obj

				if 'raw' in body:
					if isinstance(body['raw'], str):
						raw = json.loads(body['raw'])
					else:
						raw = body['raw']
					assert (ordered(raw) == ordered(r)), ("raw validation failed;")

				# store variables
				if 'globals' in case and 'provides' in case['globals']:
					for k,v in case['globals']['provides'].items():
						g[k] = eval(v)

			# check assertions
			if 'assert' in case and callable(case['assert']):
				case['assert'](req, g)

			# success; continue to next case
		except Exception as e:
			nukeline();
			error('[%02d/%02d] error running [%s]%s\n' % (count, total, FILE, desc))
			print('\n' + ('-' * 80) + '\n')
			print("exception:\n\t%s" % e)
			print("\n\nrequest headers:\n")
			print(json.dumps(dict(req.request.headers), indent=2))
			print("\n\nresponse code:\n\t%d" % req.status_code)
			print("\n\nresponse headers:\n")
			print(json.dumps(dict(req.headers), indent=2))
			print("\n\nbody:\n%s" % req.text)
			print("\n")
			print('\n' + ('-' * 80) + '\n')
			return False
		# try
	# for case in cases
	nukeline();
	success('[%02d/%02d] passed [%s]%s\n' % (count, total, FILE, desc))
	return True
# runtest
