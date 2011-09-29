#!/usr/bin/env python
#
#  This file is part of Bakefile (http://www.bakefile.org)
#
#  Copyright (C) 2009-2011 Vaclav Slavik
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
#  IN THE SOFTWARE.
#

import sys
import logging
from optparse import OptionParser


parser = OptionParser()
parser.add_option("-v", "--verbose",
                  action="store_true", dest="verbose", default=False,
                  help="show verbose output")
parser.add_option("", "--dry-run",
                  action="store_true", dest="dry_run", default=False,
                  help="don't write any files, just pretend to do it")
parser.add_option("", "--debug",
                  action="store_true", dest="debug", default=False,
                  help="show debug log")
parser.add_option("", "--dump-model",
                  action="store_true", dest="dump", default=False,
                  help="dump project's model to stdout instead of generating output")

options, args = parser.parse_args(sys.argv[1:])

if len(args) != 1:
    sys.stderr.write("incorrect number of arguments, exactly 1 .bkl required\n")
    sys.exit(3)

if options.debug:
    log_level = logging.DEBUG
elif options.verbose:
    log_level = logging.INFO
else:
    log_level = logging.WARNING
logging.basicConfig(level=log_level)


# note: we intentionally import bakefile this late so that the logging
# module is already initialized
import bkl.error
from bkl.parser import parse_file
from bkl.interpreter import Interpreter
import bkl.dumper
import bkl.io

try:
    bkl.io.dry_run = options.dry_run
    if options.dump:
        intr = bkl.dumper.DumpingInterpreter()
    else:
        intr = Interpreter()
    intr.process(parse_file(args[0]))
except KeyboardInterrupt:
    sys.exit(2)
except bkl.error.Error as e:
    if options.debug:
        raise
    else:
        sys.stderr.write("%s\n" % e)
        sys.exit(1)
