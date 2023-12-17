import subprocess
import logging

# Логгирование
FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(level=logging.INFO, 
                    filename="/Users/dmitrii_kobozev/Desktop/Python_autotests/Linux_AutoTest/Sem2/Task1/7z_logs/7z_logs_checkers_def.log", 
                    filemode="a", format= FORMAT, encoding="utf-8")

def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if text in result.stdout and result.returncode == 0:
        logging.info(f'Result def(checkout): \n {result.stdout}')
        return True
    else:
        logging.info(f'Result def(checkout): \n {result.stdout}')
        return False

def checkoutneg(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    if (text in result.stdout or text in result.stderr) and result.returncode != 0:
        logging.info(f'Result def(checkoutneg): \n {result.stdout}')
        return True
    else:
        logging.info(f'Result def(checkoutneg): \n {result.stdout}')
        return False
    
def checkhash(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    output_hash = result.stdout.strip()
    logging.info(f'Result def(checkhash): \n {output_hash}')
    return output_hash
    
def calculate_crc32c(file_path):
    result = subprocess.run(['cksum','-o3', file_path], stdout=subprocess.PIPE, encoding='utf-8')
    crc32c_hash = int(result.stdout.split()[0])
    crc32c_hex = hex(crc32c_hash)[2:]
    logging.info(f'Result def(calculate_crc32c): \n {crc32c_hex}')
    return crc32c_hex