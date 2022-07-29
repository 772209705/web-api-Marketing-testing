
import pytest
from requests import Session

from allureoperator import compose, show_response

"""
地址: https://hometest.xzm.cn/#/login
账号: testA123@bank888
密码: test666
"""

base_url = "https://api-hometest.xzm.cn"
base_url1 = "https://test-server.xzm.cn"
base_url2 = "https://group01-api-hometest.xzm.cn"
url1 = f"{base_url}/upm/user/login"
url2 = f"{base_url}/vuebasic/account/getAccountInfo"
url3 = f"{base_url}/vuebasic/account/getServerConfig"
url4 = f"{base_url1}/todo/getTaskCount"
url5 = f"{base_url1}/upm/common/getLoginInfo"
url6 = f"{base_url1}/upm/common/getTreeGroup"
url7 = f"{base_url2}/vuecrm/customerInfoSet/getFieldByRoleCode"
url8 = f"{base_url2}/vuecrm/customerInfoSet/role/fields"
url9 = f"{base_url1}/upm/user/getCompanyLogoUrl"
url10 = f"{base_url1}/news/getNewsNoticeNoReadCount"
url11 = f"{base_url2}/call/outboundController/getUserLoginType"
url12 = f"{base_url1}/todo/getTaskInfoList"
url13 = f"{base_url}/vuebasic/project/workOs/list"
url14 = f"{base_url2}/vuecrm/customer/statistic/need/contact"
url15 = f"{base_url2}/call/project/workOs/status/list"
url16 = f"{base_url2}/vuecrm/customer/statistic/need/contact"


@pytest.fixture(scope='module')
def session():
    s = Session()
    yield s


@pytest.fixture(scope='module')
def account_info():
    account_info = {}
    yield account_info


@compose(feature="企业一站式营销服务平台", story="用户", title='登录')
@pytest.mark.parametrize('username,password,msg', [
    ["testA123@bank888", "test123", "登录失败-用户名或密码错误"],
    ["!@#@$@bank888", "test123", "登录失败-企业账户不存在"],
    ["testA123@bank888", "test666", "登录成功"]
])
def test_login(session, username, password, msg):
    data = {"loginName": username, "password": password, "platform": "VUE"}
    response = session.post(url1, json=data)
    show_response(response)
    res_json = response.json()
    assert response.status_code == 200, "请求成功后状态码不为200"
    if "登录失败" in msg:
        if "用户名或密码错误" in msg:
            assert res_json['code'] == 40101, f"用户名或密码错误返回的code不为40101"
        elif "企业账户不存在" in msg:
            assert res_json['code'] == 40201, f"企业账户不存在返回的code不为40201"
    else:
        assert res_json['code'] == 40000, f"请求成功返回的code不为40000"
        assert res_json['data'].get("refLocalToken"), f"登录成功后没有refLocalToken信息"
        assert res_json['data'].get("token"), f"登录成功后没有token信息"
        # 登录成功后将token信息添加到头部
        session.headers.update({"Authorization": f"Bearer {res_json['data'].get('token')}"})


@compose(feature="企业一站式营销服务平台", story="概述", title='获取账号信息')
def test_account_info(session, account_info):
    response = session.get(url2)
    show_response(response)
    res_json = response.json()
    assert response.status_code == 200, "请求成功后状态码不为200"
    assert res_json['code'] == 40000, f"请求成功返回的code不为40000"
    account_info["userCode"] = res_json['data']['userCode']
    account_info["domainCode"] = res_json['data']['domainCode']
    account_info["staffCode"] = res_json['data']['staffCode']


@compose(feature="企业一站式营销服务平台", story="概述", title='获取服务配置')
def test_server_config(session, account_info):
    response = session.get(url3, params={"userCode": account_info["userCode"]})
    show_response(response)
    res_json = response.json()
    assert response.status_code == 200, "请求成功后状态码不为200"
    assert res_json['code'] == 40000, f"请求成功返回的code不为40000"
    account_info["gatewayUrl"] = res_json['data']['gatewayUrl']


@compose(feature="企业一站式营销服务平台", story="概述", title='获取任务数量')
def test_task_count(session, account_info):
    data = {
        "domainCode": account_info["domainCode"],
        "createUser": account_info["staffCode"],
        "userCode": account_info["userCode"]
    }
    response = session.post(url4, json=data)
    show_response(response)
    res_json = response.json()
    assert response.status_code == 200, "请求成功后状态码不为200"
    assert res_json['code'] == 40000, f"请求成功返回的code不为40000"


@compose(feature="企业一站式营销服务平台", story="概述", title='获取登录信息')
def test_login_info(session, account_info):
    response = session.get(url5, params={"userCode": account_info["userCode"],
                                         "staffCode": account_info["staffCode"]})
    show_response(response)
    res_json = response.json()
    assert response.status_code == 200, "请求成功后状态码不为200"
    assert res_json['code'] == 40000, f"请求成功返回的code不为40000"
    account_info["roleCode"] = res_json["data"]["staff"]["roleCode"]


@compose(feature="企业一站式营销服务平台", story="概述", title='获取组信息')
def test_tree_group(session, account_info):
    response = session.get(url6, params={"userCode": account_info["userCode"],
                                         "isLoadStaff": True})
    show_response(response)
    res_json = response.json()
    assert response.status_code == 200, "请求成功后状态码不为200"
    assert res_json['code'] == 40000, f"请求成功返回的code不为40000"


@compose(feature="企业一站式营销服务平台", story="概述", title='根据权限过滤展示')
def test_field_by_role_code(session, account_info):
    response = session.get(url7, params={
        "userCode": account_info["userCode"],
        "roleCode": account_info["roleCode"]
    })
    show_response(response)
    res_json = response.json()
    assert response.status_code == 200, "请求成功后状态码不为200"
    assert res_json['code'] == 40000, f"请求成功返回的code不为40000"


@compose(feature="企业一站式营销服务平台", story="概述", title='过滤展示')
def test_fields(session, account_info):
    response = session.get(url8, params={"userCode": account_info["userCode"],
                                         "roleCode": account_info["roleCode"]})
    show_response(response)
    res_json = response.json()
    assert response.status_code == 200, "请求成功后状态码不为200"
    assert res_json['code'] == 40000, f"请求成功返回的code不为40000"


@compose(feature="企业一站式营销服务平台", story="概述", title='获取公司logo地址')
def test_company_logo_url(session, account_info):
    response = session.get(url9, params={"userCode": account_info["userCode"],
                                         "getType": 1})
    show_response(response)
    res_json = response.json()
    assert response.status_code == 200, "请求成功后状态码不为200"
    assert res_json['code'] == 40000, f"请求成功返回的code不为40000"


@compose(feature="企业一站式营销服务平台", story="概述", title='获取新的未读消息数量')
def test_news_notice_noread_count(session, account_info):
    response = session.post(url10,
                            json={"domainCode": account_info["domainCode"], "userCode": account_info["userCode"]})
    show_response(response)
    res_json = response.json()
    assert response.status_code == 200, "请求成功后状态码不为200"
    assert res_json['code'] == 40000, f"请求成功返回的code不为40000"


@compose(feature="企业一站式营销服务平台", story="概述", title='获取用户登录类型')
def test_user_login_type(session, account_info):
    response = session.get(url11)
    show_response(response)
    res_json = response.json()
    assert response.status_code == 200, "请求成功后状态码不为200"
    assert res_json['code'] == 40000, f"请求成功返回的code不为40000"


@compose(feature="企业一站式营销服务平台", story="概述", title='获取用户登录类型')
def test_user_login_type(session, account_info):
    response = session.get(url12, params={
        "pageNum": 0,
        "pageSize": 4,
        "domainCode": account_info["domainCode"],
        "todoType": 3,
        "doneType": 2,
        "createUser": account_info["staffCode"],
    })
    show_response(response)
    res_json = response.json()
    assert response.status_code == 200, "请求成功后状态码不为200"
    assert res_json['code'] == 40000, f"请求成功返回的code不为40000"


@compose(feature="企业一站式营销服务平台", story="概述", title='获取项目列表')
def test_project_list(session, account_info):
    response = session.get(url13)
    show_response(response)
    res_json = response.json()
    assert response.status_code == 200, "请求成功后状态码不为200"
    assert res_json['code'] == 40000, f"请求成功返回的code不为40000"


@compose(feature="企业一站式营销服务平台", story="概述", title='获取需要联系顾客信息')
def test_need_contact(session, account_info):
    response = session.get(url14, params={
        "userCode": account_info["userCode"],
        "staffCode": account_info["staffCode"],
        "days": 7,
    })
    show_response(response)
    res_json = response.json()
    assert response.status_code == 200, "请求成功后状态码不为200"
    assert res_json['code'] == 40000, f"请求成功返回的code不为40000"


@compose(feature="企业一站式营销服务平台", story="概述", title='获取项目状态列表')
def test_project_status_list(session, account_info):
    data = {"userCode": account_info["userCode"]}
    response = session.post(url15, json=data)
    show_response(response)
    res_json = response.json()
    assert response.status_code == 200, "请求成功后状态码不为200"
    assert res_json['code'] == 40000, f"请求成功返回的code不为40000"


@compose(feature="企业一站式营销服务平台", story="概述", title='获取近几天需要联系的顾客信息')
@pytest.mark.parametrize('day', [15, 30, 60, 90])
def test_customer_need_contact(session, account_info, day):
    response = session.get(url16, params={"userCode": account_info["userCode"],
                                          "staffCode": account_info["staffCode"],
                                          "days": day})
    show_response(response)
    res_json = response.json()
    assert response.status_code == 200, "请求成功后状态码不为200"
    assert res_json['code'] == 40000, f"请求成功返回的code不为40000"
