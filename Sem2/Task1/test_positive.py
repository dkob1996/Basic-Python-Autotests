from checkers import checkout

folder_in = '/Users/dmitrii_kobozev/Desktop/Python_autotests/Linux_AutoTest/Sem2/Task1/test_arch/in'
folder_out1 = '/Users/dmitrii_kobozev/Desktop/Python_autotests/Linux_AutoTest/Sem2/Task1/test_arch/out1'
folder_out2 = '/Users/dmitrii_kobozev/Desktop/Python_autotests/Linux_AutoTest/Sem2/Task1/test_arch/out2'

def test_step1():    # test1
    res1 = checkout(f'cd {folder_in}; 7zz a {folder_out1}/arx2', 'Everything is Ok')
    res2 = checkout(f'ls {folder_out1}', 'arx2.7z')
    assert res1 and res2, "test1 Fail"

def test_step2():    # test2
    res1 = checkout(f'cd {folder_out1}; 7zz e arx2.7z -o{folder_out2} -y', 'Everything is Ok')
    res2 = checkout(f'ls {folder_out2} ', 'test.txt')
    assert res1 and res2, "test2 Fail"

def test_step3():
    assert checkout (f'cd {folder_out1}; 7zz t arx2.7z', 'Everything is Ok')

def test_step4():
    assert checkout (f'cd {folder_out1}; 7zz u arx2.7z', 'Everything is Ok')

def test_step5():
    assert checkout (f'cd {folder_out1}; 7zz d arx2.7z', 'Everything is Ok')


if __name__ == '__main__':
    test_step1()
    test_step2()
    test_step3()
    test_step4()
    test_step5()
    
    