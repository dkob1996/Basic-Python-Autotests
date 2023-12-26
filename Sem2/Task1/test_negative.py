from logging_fucn import log_neg_step_info
import yaml
from ssh_checkers import ssh_checkout_negative
from messages import error_message

with open('/Users/dmitrii_kobozev/Desktop/Python_autotests/Linux_AutoTest/Sem2/Task1/config.yaml') as f:
    data = yaml.safe_load(f)

class TestNegative:
    def test_negstep1(self, make_bad_arx):
        STEP = 1
        log_neg_step_info(STEP)
        res = ssh_checkout_negative(f"{data['ip']}", f"{data['user']}", f"{data['password']}",
                                        f"cd {data['folder_out1']}; 7zz e bad_arx.{data['arc_type']} -o{data['folder_out2']} -y",
                                        "ERRORS")
        assert res, error_message(STEP)

    def test_negstep2(self):
        STEP = 2
        log_neg_step_info(STEP)
        res = ssh_checkout_negative(f"{data['ip']}", f"{data['user']}", f"{data['password']}",
                                     f"cd {data['folder_out1']}; 7z t bad_arx.{data['arc_type']}",  "ERRORS"), 'test2 FAIL'
        assert res, error_message(STEP)