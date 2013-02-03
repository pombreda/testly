#!/usr/bin/env python

from argparse import ArgumentParser

import specfile
import fileobserver
from case import *


def parse_args():
    # Define command line arguments
    parser = ArgumentParser()

    # Add the argument for running the program in watch mode
    parser.add_argument('-w', '--watch', action='store_true',
        help='Monitor the source files for changes and run the tests each time')

    parser.add_argument('task', nargs='?', default='run')

    return parser.parse_args()


class Testly:
    def __init__(self):
        spec_file = specfile.SpecFile()

        args = parse_args()

        if args.task == 'init':
            spec_file.create()

        elif args.task == 'run':
            spec_file.read()
            spec_file.parse()
            doc = spec_file.doc

            try:
                self.command = doc['command']
                self.groups = doc['groups']
            except KeyError as e:
                print 'Spec file is missing the %s property' % e
                exit(1)

            if args.watch:
                paths_to_watch = doc['watch'] if 'watch' in doc else None
                observer = fileobserver.FileObserver(self.run, paths_to_watch)
                observer.observe()

            # Run the tests once if not in watch mode
            else:
                self.run()

        else:
            print 'Unrecognised argument %s' % args.task

    def uses_templates(self):
        # Determine whether any templates are used in the test spec file
        for group in self.groups:
            if 'templates' in group:
                return True

        return False

    def extract_templates(self, group):
        inp = out = err = None

        if 'templates' in group:
            templates = group['templates']

            if 'output' in templates:
                out = templates['output']
            if 'input' in templates:
                inp = templates['input']
            if 'error' in templates:
                err = templates['error']

        return inp, out, err

    def run(self):
        num_groups = len(self.groups)

        num_failures = 0
        total_cases = 0

        for i, group in enumerate(self.groups):
            # Skip this iteration if there are no tests
            try:
                tests = group['tests']
            except KeyError:
                continue

            templates = self.extract_templates(group)

            num_tests = len(tests)
            print 'Group %d of %d:' % (i + 1, num_groups)

            for j, test in enumerate(tests):
                num_cases = len(test['cases'])
                print indent + 'Test %d of %d:' % (j + 1, num_tests)
                print indent + 'The program should %s.' % test['it_should']

                cases = (Case(case, k, templates) for k, case in enumerate(test['cases']))

                for case in cases:
                    case.run(self.command)
                    case.print_results(num_cases)

                    total_cases += 1
                    if not case.did_pass:
                        num_failures += 1

                print ' '
            print ' '

        if num_failures == 0:
            print '%sAll %d test cases passed %s%s' % (pass_colour, total_cases, tick, end_colour)
        else:
            print '%s%d of %d test cases failed %s%s' % \
                (fail_colour, num_failures, total_cases, cross, end_colour)


def main():
    Testly()
