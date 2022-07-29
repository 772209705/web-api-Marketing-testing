
import os

import pytest

BASE_PATH = os.path.dirname(os.path.abspath(__file__))  # 根路径

if __name__ == '__main__':
    pytest.main([
        '-s',
        '-v',
        '--durations=0', '--clean-alluredir',
        '--alluredir', f'{BASE_PATH}/allure_results'
    ])
    os.system(f"{BASE_PATH}/allure-2.14.0/bin/allure serve {BASE_PATH}/allure_results")  # 本地执行
