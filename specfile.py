import yaml


class SpecFile:
    def __init__(self):
        self.filename = 'tests.yaml'
        self.file_contents = None
        self.doc = None

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
            exit(2)
