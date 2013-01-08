#!/usr/bin/env python
from subprocess import Popen, PIPE
import difflib
from argparse import ArgumentParser

import specfile
import fileobserver

# Define ASCII escape characters for special symbols and text colouring
tick = '\xE2\x9C\x94'
cross = '\xE2\x9C\x97'
pass_colour = '\033[92m'
fail_colour = '\033[91m'
end_colour = '\033[0m'
base_indent = '  '


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
            observer = fileobserver.FileObserver(self.run, paths_to_watch=paths_to_watch)
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
        # Import Pystache for templating if needed
        if self.uses_templates():
            try:
                import pystache
            except ImportError:
                print 'Pystache module not installed, tests with templates will not be run'

        num_groups = len(self.groups)

        for i, group in enumerate(self.groups):
            indent_level = 0

            # Skip this iteration if there are no test cases
            try:
                tests = group['tests']
            except KeyError:
                continue

            input_template, output_template = self.extract_templates(group)

            num_tests = len(tests)
            print 'Group %d of %d:' % (i + 1, num_groups)

            for j, test in enumerate(tests):
                indent_level = 1

                cases = test['cases']

                num_cases = len(cases)
                print '  Test %d of %d:' % (j + 1, num_tests)
                print '  The program should %s.' % test['it_should']

                for k, case in enumerate(cases):
                    indent_level = 2

                    # If there is no template for the input, assume the input property is a string.
                    if input_template == None:
                        input_ = case['input']
                    # If there is an input template, assume the input property is a dictionary
                    # of strings to be interpolated into the template.
                    else:
                        input_ = pystache.render(input_template, case['input'])

                    # Same procedure for the output template
                    if output_template == None:
                        expected_output = case['output']
                    else:
                        expected_output = pystache.render(output_template, case['output'])

                    # Spawn a subprocess by running the executable to be tested
                    try:
                        process = Popen([self.filename], stdin=PIPE, stdout=PIPE)
                    except OSError:
                        print 'No file with the name "%s" found in the current directory' % self.filename
                        exit(4)

                    # Send this test case's input to the process
                    output, error = process.communicate(input=input_)

                    did_pass = output == expected_output
                    colour = pass_colour if did_pass else fail_colour
                    symbol = tick if did_pass else cross
                    word = 'passed' if did_pass else 'failed'

                    # Print the results of this test case
                    print '    %sCase %d of %d %s %s%s' % \
                        (colour, k + 1, num_cases, word, symbol, end_colour)

                    # Print the diff of the actual output and the expected output if they do not match
                    if not did_pass:
                        diff = difflib.ndiff(output.splitlines(), expected_output.splitlines())
                        print '\n'.join(diff)

                print ' '
            print ' '


def main():
    Testly()
