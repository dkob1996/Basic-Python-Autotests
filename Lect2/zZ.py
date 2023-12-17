import subprocess

def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if text in result.stdout and result.returncode == 0:
        print(result.stdout)
        return True
    else:
        print(result.stdout)
        return False

folder_in = '/Users/dmitrii_kobozev/Desktop/test1'
folder_out = '/Users/dmitrii_kobozev/Desktop/test2/test2'
folder_out2 = '/Users/dmitrii_kobozev/Desktop/test2'
folder_extract = '/Users/dmitrii_kobozev/Desktop/test3'

if __name__ == '__main__':
    # test1
    if checkout (f'cd {folder_in}; 7zz a {folder_out}', 'Everything is Ok'):
        print('test1 SUCCESS')
    else:
        print('test1 FAIL')

    # test2
    if checkout (f'cd {folder_out2}; 7zz e test2.7z -o{folder_extract} -y', 'Everything is Ok'):
        print('test2 SUCCESS')
    else:
        print('test2 FAIL')

    # test3
    if checkout (f'cd {folder_out2}; 7zz t test2.7z', 'Everything is Ok'):
        print('test3 SUCCESS')
    else:
        print('test3 FAIL')

# sem2 19:17
        
# i - проверить имя
# x - сделать матрешку и архивировать и разархивировать в сложных путях
        
# вместо crc32 - "cksum -o3"