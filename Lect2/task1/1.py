import subprocess

'''result = subprocess.run(['ping', '-c', '3', '-n', 'yandex.ru'], encoding='utf-8', stdout=subprocess.DEVNULL)'''
'''result = subprocess.run(['ping', '-c', '3', '-n', 'yandex.ru'], encoding='utf-8', stdout=subprocess.PIPE)'''
'''result = subprocess.run(['ping', '-c', '3', '-n', 'host.host'], encoding='utf-8', stderr=subprocess.STDOUT,stdout=subprocess.PIPE)'''
result = subprocess.run(['ping', '-c', '3', '-n', 'host.host'], encoding='utf-8', stdout=subprocess.PIPE)

print(result.stdout)