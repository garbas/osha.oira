#!/usr/bin/env python

# Author: Wolfgang Thomas <thomas@syslab.com>

"""%(program)s: Check that all po files are sound and don't break when they
are compiled

usage:      %(program)s [directory]
directory:  Path to a directory that contains the 2-letter language directories.
            Defaults to current directory.
"""

import sys
import os
import re
import subprocess

# Define here the patterns for all error messages you want to ignore
messages_to_ignore = [
    '.*?entry ignored',
    '^msgfmt: found .*',
    '.*?warning: source file contains fuzzy translation',
]
ignore = [re.compile(patt) for patt in messages_to_ignore]


def usage(stream, msg=None):
    if msg:
        print >> stream, msg
        print >> stream
    program = os.path.basename(sys.argv[0])
    print >> stream, __doc__ % {"program": program}
    sys.exit(0)

if len(sys.argv) > 2:
    usage(sys.stderr, "\nERROR: Too many arguments")
if len(sys.argv) == 2:
    basedir = sys.argv[1]
else:
    basedir = '.'

if not os.path.isdir(basedir):
    usage(sys.stderr, u"The directory you provided does not exists")

dirs = [x for x in os.listdir(basedir) if len(x) == 2 and os.path.isdir(x)]
houstonwehaveaproblem = False
for dirname in dirs:
    path = "{basedir}/{dirname}/LC_MESSAGES".format(basedir=basedir, dirname=dirname)
    names = [x for x in os.listdir(path) if x.endswith('po') and not x.startswith('._')]
    for name in names:
        args = ["msgfmt", "-C", "%s/%s" % (path, name)]
        out, err = subprocess.Popen(
            args, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

        if err:
            problems = list()
            lines = err.split('\n')
            for line in lines:
                if line.strip() == '':
                    continue
                do_print = True
                for patt_ignore in ignore:
                    if patt_ignore.match(line):
                        do_print = False
                        break
                if do_print:
                    problems.append(line)

            if problems:
                print "\n%s/%s" % (path, name)
                print "\n".join(problems)
                houstonwehaveaproblem = True

if houstonwehaveaproblem:
    sys.exit('FAILURE')
