# Testly

## What is it?
Testly is a language-agnostic tool for testing command line programs that read from `stdin` and write to `stdout` and `stderr`. It only tests the external behaviour of the program, not that of any internal functions, meaning that it is suited to testing simple programs, to quickly verify that they behave as intended. Use it to test your next [fun, hacky project](http://zachholman.com/posts/from-hack-to-popular-project/).

## How do I get it?
`[sudo] pip install testly`

or

```
git clone git://github.com/lavelle/testly.git
cd testly
python setup.py install
```

## How do I use it?

### Short version

Run `testly init` to make a spec file in your project's directory, edit it to define your program's behaviour and then run `testly` to run the tests.

### Long version

Test cases are defined in a YAML file called `tests.yaml`, in your project's root directory. You must run Testly from this directory, but you can store it anywhere (although somewhere in your `PATH` is recommended for convenience).

The YAML file contains the command to execute to run your program and an object containing a heirarchy of test cases, defining arguments, input, expected output and errors and more. An [example spec file](tests.yaml) is included in this repository. You can also read the [full specification](https://github.com/lavelle/testly/wiki/Spec-File-Structure) of the file format in the wiki.

Remember that JSON is a subset of YAML so if you are not familiar with YAML you can use JSON. YAML is advised, however, because it has support for multiline strings, allowing you to define your tests with a less verbose syntax.

For every test case, if the output matches the spec, the test passes. If not, a diff is shown, so you can work out what's going wrong.

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
