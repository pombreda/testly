# Testly

## What is it?
Testly is a tool for testing command line programs that read from `stdin` and write to `stdout`. It only tests the external behaviour of the program, not that of any internal functions, so it is only really suited to very simple programs, to quickly verify that they behave as intended, however this does mean that it is language agnostic.

## How do I get it?
`[sudo] pip install testly`

or

```
git clone git://github.com/lavelle/testly.git
cd testly
python setup.py install
```

## How do I use it?
Test cases are defined in a YAML file called `tests.yaml`, in the same directory as your program executable. You must run the Testly script from this directory, but you can store it anywhere (although somewhere in your `PATH` is recommended for convenience).

The YAML file contains the name of the executable to test, and an array of objects, each of which represents one test case, and contains a description of the behaviour being tested, the input to provide to the program, and the expected output it should produce. An example spec file is included in this repository.

Remember that JSON is a subset of YAML so if you are not familiar with YAML you can use JSON. YAML is advised, however, because it has support for multiline strings, allowing you to define your tests with a much cleaner and less verbose syntax.

If the output matches the spec, the test passes. If not, a diff is shown, so you can work out what's going wrong.

You can pass `-w` to the program and it will watch the source files of your program and re-run the tests every time they change. The files and directories to be watched are defined by an array of strings under the `watch` property in the test spec file.

## What does it need?
- Python 2.6
- [Argparse](http://pypi.python.org/pypi/argparse) if using Python version < 2.7
- [PyYAML](http://pypi.python.org/pypi/PyYAML)
- [Watchdog](https://github.com/gorakhargosh/watchdog) if you want the file watch functionality
- [Pystache](https://github.com/defunkt/pystache) if you want templating support

## Changelog

### 0.3
- Added init feature

### 0.2.3
- Added support for testing error messages

### 0.2.2
- Added support for command line arguments, both global and per-case

### 0.2.1
- Added summary message showing total number of failed tests

### 0.2
- Tests are now defined in YAML instead of JSON
- Added support for templates

### 0.1
- Inital Release
