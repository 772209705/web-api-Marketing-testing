#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : zhongxin
# @Time     : 2021/7/20 10:11
# @File     : allureoperator.py.py
# @Project  : WYTest
# @Desc     : allure相关操作
# 官网地址:https://docs.qameta.io/allure/
import time
import builtins
import allure
import logging

logging.basicConfig(filename="./logging.log",
                    level=logging.DEBUG,
                    format="[%(asctime)s] |【%(levelname)s】| %(message)s",
                    datefmt='%Y-%m-%d %H:%M:%S')


def compose(**kwargs):
    """
    将头部ALlure装饰器进行封装
    可以采用：
        feature='模块名称'
        story='用户故事'
        title='用例标题'
        testcase='测试用例链接地址'
        severity='用例等级(blocker、critical、normal、minor、trivial)'
        link='链接'
        testcase=("url", "xx测试用例")
        issue=('bug地址', 'bug名称')
    的方式入参数
    :param kwargs:
    :return:
    """

    def deco(f):
        builtins.__dict__.update({'allure': allure})
        # 失败重跑
        # f = pytest.mark.flaky(
        #     reruns=kwargs.get("reruns", 2),  # 默认重试2次
        #     reruns_delay=kwargs.get("reruns_delay", 5)  # 默认等待5秒
        # )(f)
        try:
            kwargs.pop("reruns")
        except Exception:
            pass
        try:
            kwargs.pop("reruns_delay")
        except Exception:
            pass
        _kwargs = [('allure.' + key, value) for key, value in kwargs.items()]
        for allurefunc, param in reversed(_kwargs):
            if param:
                if isinstance(param, tuple):
                    f = eval(allurefunc)(*param)(f)
                else:
                    f = eval(allurefunc)(param)(f)
            else:
                f = eval(allurefunc)(f)
        return f

    return deco


def attach_text(body, name):
    """
    将text放在allure报告上
    :param body: 内容
    :param name: 标题
    :return:
    """
    try:
        allure.attach(body=str(body), name=str(name), attachment_type=allure.attachment_type.TEXT)
        logging.info(f'存放文字 {name}:{body} 成功！')
    except Exception as e:
        logging.error(f'存放文字失败 {name}:{body}！:{e}')


def show_response(response):
    """
    将接口信息展示在报告中
    :param response:
    :return:
    """
    attach_text(f'以「{response.request.method}」方式请求「{response.url}」;'
                f'返回状态码为「{response.status_code}」'
                f'返回内容为「{response.text}」',
                "接口请求")
    attach_text(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "请求时间")
    attach_text(response.url, "url")
    attach_text(response.request.method, "请求方式")
    attach_text(response.status_code, "状态码")
    attach_text(response.text, "返回内容-text")
    attach_text(response.json(), "返回内容-json")
