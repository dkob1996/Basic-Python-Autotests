import pytest
from checkers import checkout, getout
from ssh_checkers import ssh_checkout_get, ssh_checkout, upload_files
import yaml
import random, string
from datetime import datetime

with open('/Users/dmitrii_kobozev/Desktop/Python_autotests/Linux_AutoTest/Sem2/Task1/config.yaml') as f:
    data = yaml.safe_load(f)

# создание папок для тестовых данных
@pytest.fixture(autouse=True, scope='module')
def make_folders():
    return ssh_checkout(f"{data['ip']}",
                        f"{data['user']}",
                        f"{data['password']}",
                        f"mkdir -p {data['folder_in']} {data['folder_out1']} "
                        f"{data['folder_out2']} {data['folder_out3']}",
                        "")

# очистка папок с тестовыми данными после тестов
@pytest.fixture()
def clear_folders():
    return ssh_checkout(f"{data['ip']}",
                        f"{data['user']}",
                        f"{data['password']}",
                        'rm -rf {}/* {}/* {}/* {}/*'.format(data['folder_in'], data['folder_out1'],
                                                            data['folder_out2'], data['folder_out3']),
                        "")

# создание тестовых файлов
@pytest.fixture(autouse=True)
def make_files():
    list_of_files = []
    for i in range(data['count']):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=data["length_name_file"]))
        if ssh_checkout(f"{data['ip']}",
                        f"{data['user']}",
                        f"{data['password']}",
                        f"cd {data['folder_in']}; dd if=/dev/urandom of={filename} b"
                        f"s={data['bs']} count=1 iflag=fullblock",
                        ''):
            list_of_files.append(filename)
    return list_of_files

# создание подпапки и файла в нем
@pytest.fixture()
def make_subfolder():
    testfile_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k = data["length_name_file"]))
    subfolder_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k = data["length_name_file"]))
    if not ssh_checkout(f"{data['ip']}",
                        f"{data['user']}", f"{data['password']}",
                        f"cd {data['folder_in']}; mkdir {subfolder_name} ",
                        ''):
        return None, None
    if not ssh_checkout(f"{data['ip']}",
                        f"{data['user']}",
                        f"{data['password']}",
                        f"cd {data['folder_in']}/{subfolder_name};"
                        f" dd if=/dev/urandom of={testfile_name} bs={data['bs']} count=1 iflag=fullblock",
                        ''):
        return subfolder_name, None
    else:
        return subfolder_name, testfile_name
    

@pytest.fixture(autouse=True, scope='module')
def deploy():
    res = []
    upload_files(f"{data['ip']}",
                 f"{data['user']}",
                 f"{data['password']}",
                 '/home/user/p7zip-full.deb',
                 '/home/user2/p7zip-full.deb')
    res.append(ssh_checkout(f"{data['ip']}",
                            f"{data['user']}",
                            f"{data['password']}",
                            'echo "1111" | sudo -S dpkg -i /home/user2/p7zip-full.deb',
                            'Настраивается пакет'))
    res.append(ssh_checkout(f"{data['ip']}",
                            f"{data['user']}",
                            f"{data['password']}",
                            'echo "1111" | sudo -S dpkg -s p7zip-full',
                            'Status: install ok installed'))
    return all(res)


# создание плохих архивов
@pytest.fixture()
def make_bad_arx():
    ssh_checkout(f"{data['ip']}",
                 f"{data['user']}",
                 f"{data['password']}",
                 f"cd {data['folder_in']}; 7z a {data['folder_out']}/bad_arx -t{data['type']}",
                 "Everything is Ok")
    ssh_checkout(f"{data['ip']}",
                 f"{data['user']}",
                 f"{data['password']}",
                 f"truncate -s 1 {data['folder_out']}/bad_arx.{data['type']}",
                 "")

# печать времени
@pytest.fixture(autouse=True)
def print_time():
    print(f'Start: {datetime.now().strftime("%H:%M:%s.%f")}')
    yield
    print(f'\nFinish: {datetime.now().strftime("%H:%M:%s.%f")}')

# простые статы
@pytest.fixture(autouse=True)
def stat_log():
    yield
    time = datetime.now().strftime("%H:%M:%s.%f")
    stat = ssh_checkout_get(f"{data['ip']}",
                            f"{data['user']}",
                            f"{data['password']}",
                            'cat /proc/loadavg')     ## тут линукс команда, так как мы уже зашли на удаленную машину
    ssh_checkout(f"{data['ip']}",
                 f"{data['user']}",
                 f"{data['password']}",
                 f"echo 'time:{time} count:{data['count']} size;{data['bs']} stat:{stat}' >> {data['stat_ssh_file_path']}",
                 '')



# время начала
@pytest.fixture()
def start_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# расширеные статы
@pytest.fixture(autouse=True)
def stat(start_time):
    yield
    stat = ssh_checkout_get(f"{data['ip']}",
                            f"{data['user']}",
                            f"{data['password']}",'cat /proc/loadavg')   ## тут линукс команда, так как мы уже зашли на удаленную машину
    log_load = (f"Start: {start_time}, time: {datetime.now().strftime('%H:%M:%S')},"
                f" count:{data['count']} size;{data['bs']} stat:{stat} \n Finish: {stat}")
    with open('stat', 'a') as f:
        f.write(log_load + "\n")