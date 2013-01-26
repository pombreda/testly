#!/usr/bin/env python

from argparse import ArgumentParser

import specfile
import fileobserver
from case import Case


def parse_args():
    # Define command line arguments
    parser = ArgumentParser()

    # Add the argument for running the program in watch mode
    parser.add_argument('-w', '--watch', action='store_true',
        help='Monitor the source files for changes and run the tests each time')
    return parser.parse_args()


class Testly:
    def __init__(self):
        spec_file = specfile.SpecFile()
        spec_file.read()
        spec_file.parse()
        doc = spec_file.doc

        try:
            self.filename = doc['filename']
            self.groups = doc['groups']
        except KeyError as e:
            print 'Spec file is missing the %s property' % e
            exit(3)

        args = parse_args()

        if args.watch:
            paths_to_watch = doc['watch'] if 'watch' in doc else None
            observer = fileobserver.FileObserver(self.run, paths_to_watch)
            observer.observe()

        # Run the tests once if not in watch mode
        else:
            self.run()

    def uses_templates(self):
        # Determine whether any templates are used in the test spec file
        for group in self.groups:
            if 'templates' in group:
                return True

        return False

    def extract_templates(self, group):
        inp = outp = None
        if 'templates' in group:
            templates = group['templates']
            if 'output' in templates:
                outp = templates['output']
            if 'input' in templates:
                inp = templates['input']

        return inp, outp

    def run(self):
        num_groups = len(self.groups)

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
                print '  Test %d of %d:' % (j + 1, num_tests)
                print '  The program should %s.' % test['it_should']

                cases = (Case(case, k, templates) for k, case in enumerate(test['cases']))

                for case in cases:
                    case.run(self.filename)
                    case.print_results(num_cases)

                print ' '
            print ' '


def main():
    Testly()
