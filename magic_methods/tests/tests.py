import pytest

from ..file import File

CORRECT_README_FILE_ABSPATH = '/home/user/PycharmProjects/diving-in-python/magic_methods/Readme.md'
CORRECT_README_FILE_RELATIVE_PATH = 'magic_methods/Readme.md'


def test_file_path_correct():
    readme = File(CORRECT_README_FILE_ABSPATH)
    assert readme.__str__() == CORRECT_README_FILE_ABSPATH


def test_file_path_not_abs():
    with pytest.raises(FileNotFoundError):
        File(CORRECT_README_FILE_RELATIVE_PATH)


def test_file_path_incorrect():
    with pytest.raises(FileNotFoundError):
        File(CORRECT_README_FILE_ABSPATH+'sdfsfs')


def test_files_concatenation():
    file1 = File('/home/user/PycharmProjects/diving-in-python/magic_methods/tests/test_file_one.txt')
    file2 = File('/home/user/PycharmProjects/diving-in-python/magic_methods/tests/test_file_two.txt')
    file3 = file1+file2
    assert file3.__str__() == '/tmp/test_file_one.txttest_file_two.txt'
    assert file3.content == 'something' \
                            'something else'
