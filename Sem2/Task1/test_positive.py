from checkers import checkout
from checkers import calculate_crc32c
from checkers import checkhash
import os
import logging

folder_in = '/Users/dmitrii_kobozev/Desktop/Python_autotests/Linux_AutoTest/Sem2/Task1/test_arch/in'
folder_out1 = '/Users/dmitrii_kobozev/Desktop/Python_autotests/Linux_AutoTest/Sem2/Task1/test_arch/out1'
folder_out2 = '/Users/dmitrii_kobozev/Desktop/Python_autotests/Linux_AutoTest/Sem2/Task1/test_arch/out2'
folder_out3 = '/Users/dmitrii_kobozev/Desktop/Python_autotests/Linux_AutoTest/Sem2/Task1/test_arch/out3'

def error_message(number):
    message = f'Test{number} Fail'
    return message

def log_assert_error(step, message):
    logging.error(f"Step {step}: {message}")

# Простая архивация
def test_step1():
    STEP = 1
    try:
        res1 = checkout(f'cd {folder_in}; 7zz a {folder_out1}/arx2', 'Everything is Ok')
        res2 = checkout(f'ls {folder_out1}', 'arx2.7z')
        logging.info(f'Step {STEP}: \n Result 1:\n{res1} \n Result 2:\n{res2}')
        assert res1 and res2, error_message(STEP)
    except AssertionError as e:
        log_assert_error(STEP, str(e))

# Простое извлечение
def test_step2(): 
    STEP = 2
    try:
        res1 = checkout(f'cd {folder_out1}; 7zz e arx2.7z -o{folder_out2} -y', 'Everything is Ok')
        res2 = checkout(f'ls {folder_out2} ', 'test.txt')
        logging.info(f'Step {STEP}: \n Result 1:\n{res1} \n Result 2:\n{res2}')
        assert res1 and res2, "test2 Fail"
    except AssertionError as e:
        log_assert_error(STEP, str(e))

# Тест архивирования
def test_step3():
    STEP = 3
    try:
        res = checkout (f'cd {folder_out1}; 7zz t arx2.7z', 'Everything is Ok')
        logging.info(f'Step {STEP}: \n Result:\n{res}')
        assert res, error_message(STEP)
    except AssertionError as e:
        log_assert_error(STEP, str(e))

# Обновление архива
def test_step4():
    STEP = 4
    try:
        res = checkout (f'cd {folder_out1}; 7zz u arx2.7z', 'Everything is Ok')
        logging.info(f'Step {STEP}: \n Result:\n{res}')
        assert res, error_message(STEP)
    except AssertionError as e:
        log_assert_error(STEP, str(e))
    
# Удаление данных из архива
def test_step5():
    STEP = 5
    try:
        res = checkout (f'cd {folder_out1}; 7zz d arx2.7z', 'Everything is Ok')
        logging.info(f'Step {STEP}: \n Result:\n{res}')
        assert res, error_message(STEP)
    except AssertionError as e:
        log_assert_error(STEP, str(e))

# Просмотр файлов в архиве
def test_step6(): 
    STEP = 6
    try:
        res = checkout (f'cd {folder_out1}; 7zz l arx2.7z', 'test.txt')
        logging.info(f'Step {STEP}: \n Result:\n{res}')
        assert res, error_message(STEP)
    except AssertionError as e:
        log_assert_error(STEP, str(e))

# Извлечение с общим путем
def test_step7():
    STEP = 7
    try:
        res1 = checkout (f'cd {folder_out1}; 7zz x arx2.7z -o{folder_out3} -y', 'Everything is Ok')
        res2 = os.path.exists(os.path.join(folder_out3, 'folder1', 'file1.txt')) and os.path.exists(os.path.join(folder_out3, 'folder2', 'file2.txt')) and os.path.exists(os.path.join(folder_out3, 'file3.txt'))
        logging.info(f'Step {STEP}: \n Result 1:\n{res1} \n Result 2:\n{res2}')
        assert res1 and res2, error_message(STEP)
    except AssertionError as e:
        log_assert_error(STEP, str(e))
    
def test_step8():
    STEP = 8
    try:
        expected_hash = calculate_crc32c(os.path.join(folder_out1, 'arx2.7z')).upper()
        actual_hash = checkhash(f'cd {folder_out1}; 7z h arx2.7z')
        logging.info(f'Step {STEP}: \n Expected Hash:\n{expected_hash} \n Actual Hash:\n{actual_hash}')
        assert expected_hash in actual_hash, f"{error_message(STEP)}: \n Hash mismatch: Expected {expected_hash}, Actual {actual_hash}"
    except AssertionError as e:
        log_assert_error(STEP, str(e))

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
    
