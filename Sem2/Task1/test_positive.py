import os
import string
import random
import pytest
import yaml
from checkers import checkout, calculate_crc32c, checkhash
from logging_fucn import log_step_info, log_assert_error
from messages import error_message, positive_result


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
    


# Простая архивация
def test_step1(make_folders, clear_folders, make_files):
    STEP = 1
    try:
        res = []
        res.append(checkout(f'cd {data["folder_in"]}; 7zz a {data["folder_out1"]}/arx2', positive_result()))
        log_step_info(STEP,res)
        res.append(checkout(f'ls {data["folder_out1"]}', 'arx2.7z'))
        log_step_info(STEP,res)
        assert all(res), error_message(STEP)
    except AssertionError as e:
        log_assert_error(STEP, str(e))

# Простое извлечение
def test_step2(clear_folders, make_files): 
    STEP = 2
    try:
        res = []
        res.append(checkout(f'cd {data["folder_in"]}; 7zz a {data["folder_out1"]}/arx2', positive_result()))
        log_step_info(STEP,res)
        res.append(checkout(f'cd {data["folder_out1"]}; 7zz e arx2.7z -o{data["folder_out2"]} -y', positive_result()))
        log_step_info(STEP,res)
        for item in make_files:
            res.append(checkout(f'ls {data["folder_out2"]} ', item))
            log_step_info(STEP,res)
        assert all(res), "test2 Fail"
    except AssertionError as e:
        log_assert_error(STEP, str(e))

# Тест архивирования
def test_step3(make_folders, clear_folders, make_files):
    STEP = 3
    try:
        res = checkout (f'cd {data["folder_out1"]}; 7zz t arx2.7z', positive_result())
        log_step_info(STEP,res)
        assert res, error_message(STEP)
    except AssertionError as e:
        log_assert_error(STEP, str(e))

# Обновление архива
def test_step4(make_folders, clear_folders, make_files):
    STEP = 4
    try:
        res = []
        res.append(checkout(f'cd {data["folder_in"]}; 7zz a {data["folder_out1"]}/arx2', positive_result()))
        log_step_info(STEP,res)
        res.append(checkout(f'cd {data["folder_out1"]}; 7zz u arx2.7z', positive_result()))
        log_step_info(STEP,res)
        assert all(res), error_message(STEP)
    except AssertionError as e:
        log_assert_error(STEP, str(e))
    
# Удаление данных из архива
def test_step5(make_folders, clear_folders, make_files):
    STEP = 5
    try:
        res = []
        res.append(checkout(f'cd {data["folder_in"]}; 7zz a {data["folder_out1"]}/arx2', positive_result()))
        log_step_info(STEP,res)
        res.append(checkout(f'cd {data["folder_out1"]}; 7zz d arx2.7z', positive_result()))
        log_step_info(STEP,res)
        assert all(res), error_message(STEP)
    except AssertionError as e:
        log_assert_error(STEP, str(e))

# Просмотр файлов в архиве
def test_step6(make_folders, clear_folders, make_files): 
    STEP = 6
    try:
        res = []
        res.append(checkout(f'cd {data["folder_in"]}; 7zz a {data["folder_out1"]}/arx2', positive_result()))
        log_step_info(STEP,res)
        for item in make_files:
            res.append(checkout (f'cd {data["folder_out1"]}; 7zz l arx2.7z', item))
            log_step_info(STEP,res)
        assert all(res), error_message(STEP)
    except AssertionError as e:
        log_assert_error(STEP, str(e))

# Извлечение с общим путем
def test_step7(clear_folders, make_files, make_subfolder):
    STEP = 7
    try:
        res = []
        # архивация
        res.append(checkout(f'cd {data["folder_in"]}; 7zz a {data["folder_out1"]}/arx2', positive_result()))
        log_step_info(STEP,res)
        # разархивация
        res.append(checkout (f'cd {data["folder_out1"]}; 7zz x arx2.7z -o{data["folder_out3"]} -y', positive_result()))
        log_step_info(STEP,res)
        # проверка с помощью subprocess что есть файлы не в под папке 
        for item in make_files:
            res.append(checkout(f'ls {data["folder_out3"]}', item))
            log_step_info(STEP,res)
        # проверка с помощью os что есть файлы не в под папке 
        for item in make_files:
            res.append(os.path.exists(os.path.join(data["folder_out3"], item)))
            log_step_info(STEP,res)
        # проверка с помощью subprocess что есть подпапка 
        res.append(checkout(f'ls {data["folder_out3"]}', make_subfolder[0]))
        log_step_info(STEP,res)
        # проверка с помощью subprocess что в подпапке есть файл
        res.append(checkout(f'ls {data["folder_out3"]}', make_subfolder[1]))
        log_step_info(STEP,res)
        # проверка с помощью os что в подпапке есть файл
        res.append(os.path.exists(os.path.join(data["folder_out3"], make_subfolder[0], make_subfolder[1])))
        log_step_info(STEP,res)
        assert all(res), error_message(STEP)
    except AssertionError as e:
        log_assert_error(STEP, str(e))
    
def test_step8(make_folders, clear_folders, make_files):
    STEP = 8
    try:
        res = []
        # архивация
        res.append(checkout(f'cd {data["folder_in"]}; 7zz a {data["folder_out1"]}/arx2', positive_result()))
        log_step_info(STEP,res)
        # разархивация
        res.append(checkout(f'cd {data["folder_out1"]}; 7zz e arx2.7z -o{data["folder_out2"]} -y', positive_result()))
        log_step_info(STEP,res)
        
        # проверка хэша файлов до разархивации
        for item in make_files:
            res.append(checkout(f'cd {data["folder_in"]}; 7zz h {item}', positive_result()))
            log_step_info(STEP, res)
            ## считаем хэш через 7z
            actual_hash = checkhash(f'cd {data["folder_in"]}; 7zz h {item}')
            log_step_info(STEP, actual_hash)
            ## считаем хэш через аналог crc32 для macos - cksum
            expected_hash = calculate_crc32c(os.path.join(data["folder_in"], item)).upper()
            log_step_info(STEP, expected_hash)
            ## сравниваем хэши
            res.append(checkout(f'cd {data["folder_in"]}; 7zz h {item}', expected_hash))
            log_step_info(STEP,res)
       
        # проверка хэша архива
        ## проверяем что хэш успешно посчитался через 7z
        res.append(checkout(f'cd {data["folder_out1"]}; 7zz h arx2.7z', positive_result()))
        log_step_info(STEP, res)
        ## считаем хэш через 7z
        actual_hash = checkhash(f'cd {data["folder_out1"]}; 7zz h arx2.7z')
        log_step_info(STEP, actual_hash)
        ## считаем хэш через аналог crc32 для macos - cksum
        expected_hash = calculate_crc32c(os.path.join(data["folder_out1"], 'arx2.7z')).upper()
        log_step_info(STEP, expected_hash)
        ## сравниваем хэши
        res.append(checkout(f'cd {data["folder_out1"]}; 7zz h arx2.7z', expected_hash))
        log_step_info(STEP,res)
        
        # проверка хэша файлов после разархивации
        ## проверяем что хэш успешно посчитался через 7z
        for item in make_files:
            res.append(checkout(f'cd {data["folder_out2"]}; 7zz h {item}', positive_result()))
            log_step_info(STEP, res)
            ## считаем хэш через 7z
            actual_hash = checkhash(f'cd {data["folder_out2"]}; 7zz h {item}')
            log_step_info(STEP, actual_hash)
            ## считаем хэш через аналог crc32 для macos - cksum
            expected_hash = calculate_crc32c(os.path.join(data["folder_out2"], item)).upper()
            log_step_info(STEP, expected_hash)
            ## сравниваем хэши
            res.append(checkout(f'cd {data["folder_out2"]}; 7zz h {item}', expected_hash))
            log_step_info(STEP,res)

        assert all(res), f"{error_message(STEP)}: \n Hash mismatch: Expected {expected_hash}, Actual {actual_hash}"
    except AssertionError as e:
        log_assert_error(STEP, str(e))

# очищаем все папки с файлами и проверяем что отчистилось
def test_step0(clear_folders):
    STEP = 0
    assert clear_folders, error_message(STEP, clear_folders)

if __name__ == '__main__':
    test_step1()
    test_step2()
    test_step3()
    test_step4()
    test_step5()

    test_step1()
    test_step6()
    test_step7()
    test_step8()

    test_step0()
    
    
