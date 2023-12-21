import pytest
from checkers import checkout
import yaml
import random, string

with open('/Users/dmitrii_kobozev/Desktop/Python_autotests/Linux_AutoTest/Sem2/Task1/config.yaml') as f:
    data = yaml.safe_load(f)

# создание папок для тестовых данных
@pytest.fixture()
def make_folders():
    return checkout('mkdri {} {} {} {}'.format(data["folder_in"], data["folder_out1"],data["folder_out2"],data["folder_out3"]), '')

# очистка папок с тестовыми данными после тестов
@pytest.fixture()
def clear_folders():
    return checkout('rm -rf {}/* {}/* {}/* {}/*'.format(data["folder_in"], data["folder_out1"],data["folder_out2"],data["folder_out3"]), '')

# создание тестовых файлов
# k - длина строки
# range(5) - 5 файлов
@pytest.fixture()
def make_files():
    list_of_files = []
    for i in range(data["count_test_files"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 5))
        if checkout('cd {}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock'.format(data["folder_in"], filename),''):
            list_of_files.append(filename)
    return list_of_files

# создание подпапки и файла в нем
@pytest.fixture()
def make_subfolder():
    testfile_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 5))
    subfolder_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 5))
    if not checkout('cd {}; mkdir {}'.format(data["folder_in"], subfolder_name), ''):
        return None, None
    if not checkout('cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock'.format(data["folder_in"], subfolder_name, 
                                                                                          testfile_name),''):
        return subfolder_name, None
    else:
        return subfolder_name, testfile_name
    