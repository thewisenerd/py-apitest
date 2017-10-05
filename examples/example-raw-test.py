import functools

def dummy():
	# do nothing; this is not actually called.
	print("dummy function for globals")

test = {
	'url': '/user-agent',
	'desc': 'example user-agent request',
	'cases': [
		{
			'method': 'GET',
			'response': {
				'status_code': 200,
				'content-type': 'application/json',
				'body': {
					'type': 'json',
					'schema': {
						'type': "object",
						"properties": {
							"user-agent": {"type": "string"}
						}
					},
					'raw': """
						{"user-agent": "python-requests/2.18.1"}
						"""
				}
			}
		} # user-agent GET
	] # cases
}; # test
