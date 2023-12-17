from checkers import checkoutneg
import logging

folder_out1 = '/Users/dmitrii_kobozev/Desktop/Python_autotests/Linux_AutoTest/Sem2/Task1/test_arch/out1'
folder_out2 = '/Users/dmitrii_kobozev/Desktop/Python_autotests/Linux_AutoTest/Sem2/Task1/test_arch/out2'

def test_negstep1():
    STEP = 1
    logging.info(f'Negative Step {STEP}')
    assert checkoutneg(f'cd {folder_out1}; 7zz e arx2bad.7z -o{folder_out2} -y', 'ERROR')

def test_negstep2():
    STEP = 2
    logging.info(f'Negative Step {STEP}')
    assert checkoutneg(f'cd {folder_out1}; 7zz t arx2bad.7z', 'ERROR')



if __name__ == '__main__':
    test_negstep1()
    test_negstep2()