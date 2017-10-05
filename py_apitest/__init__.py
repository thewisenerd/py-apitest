import os
import sys

import argparse

from .apiTest import runtest
from .helpers import print, info, success, error, findfilesendingwith

def _real_main():
	parser = argparse.ArgumentParser(description='test an api.')
	parser.add_argument('--testfile', nargs='+', help='testcase files')
	parser.add_argument('--testdir', nargs='+', help='directory containing testcase files [*-test.py]')
	parser.add_argument('BASEURL', help='base url of API')
	args = parser.parse_args()

	if (args.testdir == None and args.testfile == None):
		error("requires at least one of --testdir or --testfile.\n\n")
		parser.print_help();
		return 1;

	files = []

	if args.testdir:
		for DIR in args.testdir:
			if not os.path.isdir(os.path.realpath(DIR)):
				error("[%s] is not a directory.\n" % DIR)
			files = files + list(findfilesendingwith("-test.py", DIR))

	if args.testfile:
		files = files + args.testfile

	info("initializing test suite\n")

	if (len(files)):
		info( "found %d testcase%s\n\n" % (len(files), ('s' if len(files) > 1 else '')) )
	else:
		error("no test cases found\n")
		return 1

	info("running tests:\n")

	count = 0
	total = len(files)
	g = {}

	successes = 0
	failures = 0

	for FILE in files:
		count = count + 1
		if (runtest(FILE, args.BASEURL, g, count, total)):
			successes = successes + 1
		else:
			failures = failures + 1

	print("\n\n")
	if (successes == total):
		success('[%02d/%02d] all passed\n' % (successes, total))
		return 0
	else:
		error('[%02d/%02d] %02d pass / %02d fail\n' % (successes, total, successes, failures))
		return 1

def main():
	try:
		sys.exit(_real_main())
	except KeyboardInterrupt:
		sys.exit('\nERROR: Interrupted by user')
