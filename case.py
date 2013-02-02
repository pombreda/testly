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
base_indent = '  '


class Case:
    def __init__(self, case, index, templates):
        self.case = case
        self.input_template, self.output_template = templates
        self.index = index + 1

    def run(self, command):
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

        # Same procedure for the output template
        if self.output_template == None:
            self.expected_output = self.case['output']
        else:
            self.expected_output = pystache.render(self.output_template, self.case['output'])

        if 'arguments' in self.case:
            command += self.case['arguments']

        # Spawn a subprocess by running the executable to be tested
        try:
            process = Popen(command, stdin=PIPE, stdout=PIPE)
        except OSError:
            print 'Command "%s" failed to execute. Is the program in your $PATH?' % ' '.join(command)
            exit(4)

        # Send this test case's input to the process
        self.output, error = process.communicate(input=input_)
        self.did_pass = self.output == self.expected_output

    def print_results(self, total):
        colour = pass_colour if self.did_pass else fail_colour
        symbol = tick if self.did_pass else cross
        word = 'passed' if self.did_pass else 'failed'

        # Print the diff of the actual output and the expected output if they do not match
        if not self.did_pass:
            diff = difflib.ndiff(self.output.splitlines(), self.expected_output.splitlines())
            print '\n'.join(diff)

        print '    %sCase %d of %d %s %s%s' % (colour, self.index, total, word, symbol, end_colour)
