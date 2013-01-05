#!/usr/bin/env python

import json
from subprocess import Popen, PIPE
import difflib
import time
from argparse import ArgumentParser

# Define ASCII escape characters for special symbols and text colouring
tick = '\xE2\x9C\x94'
cross = '\xE2\x9C\x97'
pass_colour = '\033[92m'
fail_colour = '\033[91m'
end_colour = '\033[0m'

# Open the JSON file
try:
    file_ = open('tests.json').read()
except IOError:
    print 'No file named tests.json in the current directory'
    exit(1)

# Parse the file contents into a Python dictionary
try:
    json_ = json.loads(file_)
except ValueError:
    print 'tests.json does not contain a valid JSON object'
    exit(2)

try:
    filename = json_['filename']
    tests = json_['tests']
except KeyError as e:
    print 'tests.json is missing the %s property' % e
    exit(3)


def run_tests():
    i = 1
    num_tests = len(tests)

    for test in tests:
        # Skip this iteration if there are no test cases
        try:
            cases = test['cases']
        except KeyError:
            continue

        before = [test['before']] if 'before' in test else []
        after = [test['after']] if 'after' in test else []

        j = 1
        num_cases = len(cases)
        print 'Test %d of %d:' % (i, num_tests)

        for case in cases:
            line_separator = case['line_separator'] if 'line_separator' in case else '\n'

            input_ = '\n'.join(case['input'])
            expected_output = line_separator.join(before + case['output'] + after)

            # Spawn a subprocess by running the executable to be tested
            try:
                process = Popen([filename], stdin=PIPE, stdout=PIPE)
            except OSError:
                print 'No file with the name "%s" found in the current directory' % filename
                exit(4)

            # Send this test case's input to the process
            output, error = process.communicate(input=input_)

            didPass = output == expected_output
            colour = pass_colour if didPass else fail_colour
            symbol = tick if didPass else cross
            word = 'passed' if didPass else 'failed'

            # Print the results of this test case
            print '%sCase %d of %d %s %s%s' % (colour, j, num_cases, word, symbol, end_colour)
            print 'The program should %s.' % case['it_should']

            # Print the diff of the actual output and the expected output if they do not match
            if not didPass:
                diff = difflib.ndiff(output.splitlines(), expected_output.splitlines())
                print '\n'.join(diff)

            j += 1

        i += 1
        print ' '

# Define command line arguments
parser = ArgumentParser()

# Add the argument for running the program in watch mode
parser.add_argument('-w', '--watch', action='store_true',
    help='Monitor the source files for changes and run the tests each time')
args = parser.parse_args()

if args.watch:
    # Import Watchdog for monitoring the filesystem
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    except ImportError:
        print 'Watchdog module not installed. File watch functionality disabled'
        exit(7)

    # Get the array of paths to watch from the JSON file
    default_paths = [
        {
            'path': '.',
            'recursive': True
        }
    ]
    paths_to_watch = json_['watch'] if 'watch' in json_ else default_paths

    if len(paths_to_watch) < 1:
        print '"watch" property in tests.json is empty'
        exit(6)

    # Override the base event handler class to run the tests when the files change
    class TestEventHandler(FileSystemEventHandler):
        def on_modified(self, event):
            run_tests()

    # Create an instance of the new event handler and an observer
    event_handler = TestEventHandler()
    observer = Observer()

    # Register the event for each path in the array
    for path in paths_to_watch:
        path_string = path['path'] if 'path' in path else '.'
        recursive = path['recursive'] if 'recursive' in path else True

        observer.schedule(event_handler, path=path_string, recursive=recursive)

    # Start watching changes
    print 'Watching for changes. Press Ctrl+C to cancel'
    observer.start()

    # Allow the monitoring loop to be interrupted by a keyboard event
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Run the tests once if not in watch mode
else:
    run_tests()
