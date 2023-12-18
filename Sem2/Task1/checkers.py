import subprocess
from logging_fucn import log_checkout_func
from logging_fucn import log_checkout_negative_func
from logging_fucn import log_check_hash
from logging_fucn import log_check_crc32_hash


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if text in result.stdout and result.returncode == 0:
        log_checkout_func(result.stdout)
        return True
    else:
        log_checkout_func(result.stdout)
        return False

def checkoutneg(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    if (text in result.stdout or text in result.stderr) and result.returncode != 0:
        log_checkout_negative_func(result.stdout)
        return True
    else:
        log_checkout_negative_func(result.stdout)
        return False
    
def checkhash(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    output_hash = result.stdout.strip()
    log_check_hash(output_hash)
    return output_hash
    
def calculate_crc32c(file_path):
    result = subprocess.run(['cksum','-o3', file_path], stdout=subprocess.PIPE, encoding='utf-8')
    crc32c_hash = int(result.stdout.split()[0])
    crc32c_hex = hex(crc32c_hash)[2:]
    log_check_crc32_hash(crc32c_hex)
    return crc32c_hex