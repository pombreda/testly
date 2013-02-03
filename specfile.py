import yaml
import os.path

base_document = \
"""command: ['program_name', 'args', '-flags']

watch:
- path: path_here
  recursive': false

groups:
- tests:
  - it_should: do something
    cases:
    - input: Some input
      output: Some output

  - it_should: do something else
    cases:
    - arguments: ['-a', 'invaid_value']
      error: |
        Argument is invalid


- templates:
    output: |
      Some common string {{ var_name }}

  tests:
  - it_should: do a third thing
    cases:
    - input: Some input
      output:
        var_name: Value to interpolate here
"""


class SpecFile:
    def __init__(self):
        self.filename = 'tests.yaml'
        self.file_contents = None
        self.doc = None

    def create(self):
        if os.path.isfile(self.filename):
            print '%s already exists in this directory' % self.filename
            exit(1)

        try:
            f = open(self.filename, 'w')
        except IOError:
            print 'Could not create test spec file in current directory'
            exit(1)

        f.write(base_document)

        f.close()

    def read(self):
        # Open the YAML file and read its contents to a string
        try:
            self.file_contents = open(self.filename).read()
        except IOError:
            print 'No file named %s in the current directory' % self.filename
            exit(1)

    def parse(self):
        # Parse the file contents into a Python dictionary
        try:
            self.doc = yaml.load(self.file_contents)
        except ValueError as e:
            print 'Spec file is not a valid YAML document'
            print e
            exit(1)
