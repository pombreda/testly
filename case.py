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


class Case:
    def __init__(self, case, index, templates):
        self.case = case
        self.input_template, self.output_template = templates
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

        if 'error' in self.case:
            self.expected_error = self.case['error']

        if 'output' in self.case:
            # Same procedure for the output template
            if self.output_template == None:
                self.expected_output = self.case['output']
            else:
                self.expected_output = pystache.render(self.output_template, self.case['output'])

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
            exit(4)

        # Send this test case's input to the process
        self.output, self.error = process.communicate(input=input_)

        # Check that any outputs and errors match what was expected
        if self.expected_output != self.output or self.expected_error != self.error:
            self.did_pass = False

    def print_results(self, total):
        colour = pass_colour if self.did_pass else fail_colour
        symbol = tick if self.did_pass else cross
        word = 'passed' if self.did_pass else 'failed'

        print '    %sCase %d of %d %s %s%s' % (colour, self.index, total, word, symbol, end_colour)

        # Print the diff of the actual output and the expected output if they do not match
        if not self.did_pass:
            if self.expected_output != self.output:
                print '    Differences in output:'
                diff = difflib.ndiff(self.output.splitlines(), self.expected_output.splitlines())
                print '    ' + '\n    '.join(diff)

            if self.expected_error != self.error:
                print '    Differences in errors:'
                diff = difflib.ndiff(self.error.splitlines(), self.expected_error.splitlines())
                print '    ' + '\n    '.join(diff)

            print ' '
