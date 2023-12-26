import os
import yaml
from logging_fucn import log_step_info, log_exception
from messages import error_message
from ssh_checkers import ssh_checkout

with open('/Users/dmitrii_kobozev/Desktop/Python_autotests/Linux_AutoTest/Sem2/Task1/config.yaml') as f:
    data = yaml.safe_load(f)

class TestPositive:

    # Простая архивация
    def test_step1(make_folders, clear_folders, make_files):
        STEP = 1
        try:
            res = []
            res.append(ssh_checkout(f"{data['ip']}", 
                                    f"{data['user']}", 
                                    f"{data['password']}", 
                                    f'cd {data["folder_in"]}; 7zz a -t{data["arc_type"]} {data["folder_out1"]}/arx2',
                               f"{data['valid']}"))
            log_step_info(STEP,res)
            res.append(ssh_checkout(f"{data['ip']}", 
                                    f"{data['user']}", 
                                    f"{data['password']}",f'ls {data["folder_out1"]}', f'arx2.{data["arc_type"]}'))
            log_step_info(STEP,res)
            assert all(res), error_message(STEP)
        except AssertionError as e:
            log_exception(STEP, e)

    # Простое извлечение
    def test_step2(clear_folders, make_files): 
        STEP = 2
        try:
            res = []
            res.append(ssh_checkout(f"{data['ip']}", 
                                    f"{data['user']}", 
                                    f"{data['password']}",
                                    f'cd {data["folder_in"]}; 7zz a -t{data["arc_type"]} {data["folder_out1"]}/arx2', 
                                    f"{data['valid']}"))
            log_step_info(STEP,res)
            res.append(ssh_checkout(f"{data['ip']}", 
                                    f"{data['user']}", 
                                    f"{data['password']}",
                                    f'cd {data["folder_out1"]}; 7zz e arx2.{data["arc_type"]} -o{data["folder_out2"]} -y', 
                                    f"{data['valid']}"))
            log_step_info(STEP,res)
            for item in make_files:
                res.append(ssh_checkout(f"{data['ip']}", 
                                        f"{data['user']}", 
                                        f"{data['password']}",
                                        f'ls {data["folder_out2"]} ', item))
                log_step_info(STEP,res)
            assert all(res), "test2 Fail"
        except AssertionError as e:
            log_exception(STEP, e)

    # Тест архивирования
    def test_step3(make_folders, clear_folders, make_files):
        STEP = 3
        try:
            res = ssh_checkout (f"{data['ip']}", 
                                f"{data['user']}", 
                                f"{data['password']}",
                                f'cd {data["folder_out1"]}; 7zz t arx2.{data["arc_type"]}', 
                                f"{data['valid']}")
            log_step_info(STEP,res)
            assert res, error_message(STEP)
        except AssertionError as e:
            log_exception(STEP, e)

    # Обновление архива
    def test_step4(make_folders, clear_folders, make_files):
        STEP = 4
        try:
            res = []
            res.append(ssh_checkout(f"{data['ip']}", 
                                    f"{data['user']}", 
                                    f"{data['password']}",
                                    f'cd {data["folder_in"]}; 7zz a -t{data["arc_type"]} {data["folder_out1"]}/arx2', 
                                    f"{data['valid']}"))
            log_step_info(STEP,res)
            res.append(ssh_checkout(f"{data['ip']}", 
                                    f"{data['user']}", 
                                    f"{data['password']}",
                                    f'cd {data["folder_out1"]}; 7zz u arx2.{data["arc_type"]}', 
                                    f"{data['valid']}"))
            log_step_info(STEP,res)
            assert all(res), error_message(STEP)
        except AssertionError as e:
            log_exception(STEP, e)
        
    # Удаление данных из архива
    def test_step5(make_folders, clear_folders, make_files):
        STEP = 5
        try:
            res = []
            res.append(ssh_checkout(f"{data['ip']}", 
                                    f"{data['user']}", 
                                    f"{data['password']}",
                                    f'cd {data["folder_in"]}; 7zz a -t{data["arc_type"]} {data["folder_out1"]}/arx2', 
                                    f"{data['valid']}"))
            log_step_info(STEP,res)
            res.append(ssh_checkout(f"{data['ip']}", 
                                    f"{data['user']}", 
                                    f"{data['password']}",
                                    f'cd {data["folder_out1"]}; 7zz d arx2.{data["arc_type"]}', 
                                    f"{data['valid']}"))
            log_step_info(STEP,res)
            assert all(res), error_message(STEP)
        except AssertionError as e:
            log_exception(STEP, e)

    # Просмотр файлов в архиве
    def test_step6(make_folders, clear_folders, make_files): 
        STEP = 6
        try:
            res = []
            res.append(ssh_checkout(f"{data['ip']}", 
                                    f"{data['user']}", 
                                    f"{data['password']}",
                                    f'cd {data["folder_in"]}; 7zz a -t{data["arc_type"]} {data["folder_out1"]}/arx2', 
                                    f"{data['valid']}"))
            log_step_info(STEP,res)
            for item in make_files:
                res.append(ssh_checkout (f"{data['ip']}", 
                                        f"{data['user']}", 
                                        f"{data['password']}",
                                        f'cd {data["folder_out1"]}; 7zz l arx2.{data["arc_type"]}', item))
                log_step_info(STEP,res)
            assert all(res), error_message(STEP)
        except AssertionError as e:
            log_exception(STEP, e)

    # Извлечение с общим путем
    def test_step7(clear_folders, make_files, make_subfolder):
        STEP = 7
        try:
            res = []
            # архивация
            res.append(ssh_checkout(f"{data['ip']}", 
                                    f"{data['user']}", 
                                    f"{data['password']}",
                                    f'cd {data["folder_in"]}; 7zz a -t{data["arc_type"]} {data["folder_out1"]}/arx2', 
                                    f"{data['valid']}"))
            log_step_info(STEP,res)
            # разархивация
            res.append(ssh_checkout (f"{data['ip']}", 
                                    f"{data['user']}", 
                                    f"{data['password']}",
                                    f'cd {data["folder_out1"]}; 7zz x arx2.{data["arc_type"]} -o{data["folder_out3"]} -y', 
                                    f"{data['valid']}"))
            log_step_info(STEP,res)
            # проверка с помощью subprocess что есть файлы не в под папке 
            for item in make_files:
                res.append(ssh_checkout(f"{data['ip']}", 
                                        f"{data['user']}", 
                                        f"{data['password']}",
                                        f'ls {data["folder_out3"]}', item))
                log_step_info(STEP,res)
            # проверка с помощью os что есть файлы не в под папке 
            for item in make_files:
                res.append(os.path.exists(os.path.join(data["folder_out3"], item)))
                log_step_info(STEP,res)
            # проверка с помощью subprocess что есть подпапка 
            res.append(ssh_checkout(f"{data['ip']}", 
                                    f"{data['user']}", 
                                    f"{data['password']}",
                                    f'ls {data["folder_out3"]}', make_subfolder[0]))
            log_step_info(STEP,res)
            # проверка с помощью subprocess что в подпапке есть файл
            res.append(ssh_checkout(f"{data['ip']}", 
                                    f"{data['user']}", 
                                    f"{data['password']}",
                                    f'ls {data["folder_out3"]}', make_subfolder[1]))
            log_step_info(STEP,res)
            # проверка с помощью os что в подпапке есть файл
            res.append(os.path.exists(os.path.join(data["folder_out3"], make_subfolder[0], make_subfolder[1])))
            log_step_info(STEP,res)
            assert all(res), error_message(STEP)
        except AssertionError as e:
            log_exception(STEP, e)

    # очищаем все папки с файлами и проверяем что отчистилось
    def test_step0(clear_folders):
        STEP = 0
        assert clear_folders, error_message(STEP, clear_folders)
