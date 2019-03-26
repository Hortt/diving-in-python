import os
import tempfile


class File:

    def __init__(self, filepath):
        self.file = self._get_valid_file(filepath)

    def __str__(self):
        return self.file

    def __add__(self, other):
        new_file_path = os.path.join(tempfile.gettempdir(), self.filename+other.filename)
        with open(new_file_path, 'w') as new_file:
            new_file.write(self.content)
            new_file.write(other.content)
            print('New file written: {}'.format(new_file_path))
            return self.__class__(new_file_path)

    def __getitem__(self, index):
        return self.lines()[index]

    def lines(self):
        with open(self.file, 'r') as f:
            return f.readlines()

    def write(self, line):
        with open(self.file, 'w') as f:
            f.write(line)

    @property
    def filename(self):
        return os.path.split(self.file)[1]

    @property
    def content(self):
        with open(self.file) as f:
            return f.read()

    @staticmethod
    def _get_valid_file(filepath):
        if os.path.isfile(filepath) and os.path.isabs(filepath):
            return filepath
        raise FileNotFoundError('Wrong file path or file doesn\'t exist')


if __name__ == '__main__':
    file = File('/home/user/PycharmProjects/diving-in-python/magic_methods/Readme.md')
    for _line in file:
        print(_line)
