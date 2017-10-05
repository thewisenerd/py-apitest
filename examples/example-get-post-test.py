import functools

def dummy():
	# do nothing; this is not actually called.
	print("dummy function for globals")

def assertion_get(req, g):
	r = req.json()
	# do something here

def assertion_post(req, g):
	r = req.json()

	assert (r['origin'] != g['ip']), "ip of GET request does not match POST"

test = {
	'url': '/anything',
	'desc': 'example get/post sequence request',
	'cases': [
		{
			'method': 'GET',
			'globals': {
				'provides': {
					'ip': "r['origin']",
				}
			},
			'assert': assertion_get,
			'response': {
				'status_code': 200,
				'content-type': 'application/json',
				'body': {
					'type': 'json',
					'schema': {
						"type": "object",
						"properties": {
							"args": {"type": "object"},
							"data": {"type": "string"},
							"files": {"type": "object"},
							"form": {"type": "object"},
							"headers": {"type": "object"},
							"json": {"type": ["object", "null"]},
							"method": {"type": "string"},
							"origin": {"type": "string"},
							"url": {"type": "string"},
						},
					},
				},
			},
		}, # get
		{
			'method': 'POST',
			'globals': {
				'requires': ['ip'],
			},
			'payload': {
				'myip': functools.partial(dummy, 'ip')
			},
			'assert': assertion_post,
			'response': {
				'status_code': 200,
				'content-type': 'application/json',
				'body': {
					'type': 'json',
					'schema': {
						"type": "object",
						"properties": {
							"args": {"type": "object"},
							"data": {"type": "string"},
							"files": {"type": "object"},
							"form": {
								"type": "object",
								"properties": {
									"myip": { "type": "string" }
								}
							},
							"headers": {"type": "object"},
							"json": {"type": ["object", "null"]},
							"method": {"type": "string"},
							"origin": {"type": "string"},
							"url": {"type": "string"},
						},
					},
				},
			},
		}, # post
	] # cases
}; # test
