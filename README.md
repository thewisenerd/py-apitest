py-apitest - test apis.

- [DESCRIPTION](#description)
- [OPTIONS](#options)
- [TEST TEMPLATE](#test-template)
- [TODO](#todo)
- [FAQ](#faq)
- [LICENSE](#license)

# DESCRIPTION
**py-apitest** is a command-line program to test an API workflow.
It requires the Python interpreter, version 2.7 or above.
Please install the dependencies specified in [requirements.txt](/requirements.txt).

    py-apitest [OPTIONS] BASEURL

# OPTIONS

## positional arguments
    BASEURL               base url of API

## optional arguments
    -h, --help            show this help message and exit
    --testfile TESTFILE [TESTFILE ...]
                          testcase files
    --testdir TESTDIR [TESTDIR ...]
                          directory containing testcase files [*-test.py]

# TEST TEMPLATE

The template test for py-apitest are python files that contain an object `test`.

The `--testfile` option allows you to indicate which files to run, while the
`--testdir` option allows you to define a directory containing test files.
Currently, with the `--testdir` option, py-apitest searches for files ending
with `-test.py` and executes them.

below is the test template jsonschema written in python.
For a better example, please refer to tests defined in the [examples/](/examples) folder.

```python

schema = {
	"type": "object",
	"properties": {
		"url": {"type": "string"}, # BASEDIR + url to test
		"desc": {"type": "string"}, # describe this test case
		"cases": {
			"type": "array",
			"items": {
				"type": "object",
				"properties": {
					"method": {"type": "string"}, # method to use [get/post]
					"globals": {
						"type": "object",
						"properties": {
							"requires": {
								"type": "array",
								"items": {"type": "string"} # global variables that `need` to exist before test is run
							},
							"provides": {
								"type": "object",
								"properties": {
									"key": {"type": "string"} # an evaluable string with `r` as request.json()
								},
							},
						},
					}, # globals
					"payload": {
						# payload to send with request
						# can contain function partials FOO(dummyfunction, 'key')
						#   that get replaced with GLOBALS['key']
						#   refer to examples/
						"type": "object"
					},
					"response": {
						"type": "object",
						"properties": {
							"status_code": {"type": "number"},
							"content-type": {"type": "string"},
							"body": {
								"type": "object",
								"properties": {
									"type": {"type": "string"},
									"schema": {"type": "object"}, # json schema for validation
									"raw": {"type": ["object", "string"]}, # raw object or json string for comparison
								}
							}
						}, # response properties
						"required": ["status_code"],
					}, # response
					# assertion
					# commented out as "function" is not a valid datatype;
					# "assert": { "type": "function" }, # an assertion function foo(request, GLOBALS)
				}, # cases[i] properties
				"required": ["method", "response"],
			} # cases[i]
		} # cases
	}, # schema properties
	"required": ["url", "cases"],
}; # schema

```

# TODO

 - [ ] package into a proper python module
 - [ ] make executable from commandline (install scripts)
 - [ ] optional suffixes for `--testdir`
 - [ ] more request methods
 - [ ] custom request handler
 - [ ] more platforms support

# FAQ

### why?

> Your scientists were so preoccupied with whether or not they could, they didn’t stop to think if they should.
>
> -- Ian malcolm, Jurassic Park

# LICENSE

py-apitest is released into the public domain by [thewisenerd](https://github.com/thewisenerd).
