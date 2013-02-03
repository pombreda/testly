from subprocess import Popen, PIPE
import difflib

try:
    import pystache
except ImportError:
    print 'Pystache module not installed, tests with templates will not be run'

# Define ASCII escape characters for special symbols and text colouring
tick = '\xE2\x9C\x94'
cross = '\xE2\x9C\x97'
pass_colour = '\033[92m'
fail_colour = '\033[91m'
end_colour = '\033[0m'
indent = '  '
indent2 = indent * 2


class Case:
    def __init__(self, case, index, templates):
        self.case = case
        self.input_template, self.output_template, self.error_template = templates
        self.index = index + 1

        self.expected_output = ''
        self.expected_error = ''

        self.did_pass = True

    def run(self, base_command):
        # Create the input string, if there is one, or default to no input
        if 'input' in self.case:
            # If there is no template for the input, assume the input property is a string.
            if self.input_template == None:
                input_ = self.case['input']
            # If there is an input template, assume the input property is a dictionary
            # of strings to be interpolated into the template.
            else:
                input_ = pystache.render(self.input_template, self.case['input'])
        else:
            input_ = ''

        # Same procedure for the outputs and errors
        if 'output' in self.case:
            if self.output_template == None:
                self.expected_output = self.case['output']
            else:
                self.expected_output = pystache.render(self.output_template, self.case['output'])

        if 'error' in self.case:
            if self.error_template == None:
                self.expected_error = self.case['error']
            else:
                self.expected_error = pystache.render(self.error_template, self.case['error'])

        # Ensure some kind of behaviour is being tested for
        if not self.expected_output and not self.expected_error:
            print 'Please provide either an expected error, an expected output, or both'
            exit(1)

        # Python is great
        command = base_command[:]

        # Add this case's arguments to the base command to be executed
        if 'arguments' in self.case:
            command += self.case['arguments']

        # Spawn a subprocess by running the executable to be tested
        try:
            process = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        except OSError:
            print 'Command "%s" failed to execute. Is the program in your $PATH?' % ' '.join(command)
            exit(1)

        # Send this test case's input to the process
        self.output, self.error = process.communicate(input=input_)

        # Check that any outputs and errors match what was expected
        if self.expected_output != self.output or self.expected_error != self.error:
            self.did_pass = False

    def print_diff(expected, actual, name):
        if expected != actual:
            print '%sDifferences in %s:' % (indent2, name)
            diff = difflib.ndiff(actual.splitlines(), expected.splitlines())
            print indent2 + ('\n' + indent2).join(diff)

    def print_results(self, total):
        colour = pass_colour if self.did_pass else fail_colour
        symbol = tick if self.did_pass else cross
        word = 'passed' if self.did_pass else 'failed'

        print '%s%sCase %d of %d %s %s%s' % (indent2, colour, self.index, total, word, symbol, end_colour)

        # Print the diff of the actual output and the expected output if they do not match
        if not self.did_pass:
            self.print_diff(self.expected_output, self.output, 'output')
            self.print_diff(self.expected_error, self.error, 'errors')
            print ' '
