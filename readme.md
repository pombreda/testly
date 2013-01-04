# Tester

Tester is a tool for testing command line programs that read from `stdin` and write to `stdout`. It only tests the external behaviour of the program, not that of any internal functions, so it is only really suited to very simple programs, to quickly verify that they behave as intended, however this does mean that it is language agnostic.

Test cases are defined in a JSON file called `tests.json`, in the same directory as your program executable. You must run the Tester script from this directory, but you can store it anywhere (although somewhere in your `PATH` is recommended for convenience).

The JSON file contains the name of the executable to test, and an array of objects, each of which represents one test case, and contains a description of the behaviour being tested, the input to provide to the program, and the expected output it should produce. An example spec file is included in this repository.

If the output matches the spec, the test passes. If not, a diff is shown, so you can work out what's going wrong.

Tester requires Python 2.7 to run and has no third party dependencies.

##To Do:
- Exception handling
- Add an option to ignore whitespace
- Quit if input does not cause program being tested to terminate after a specified time limit
- Add some sort of template support so text that the program outputs every time, regardless of input, does not have to be included in every test case.
- Watch for changes in the source files and rerun every time they change
