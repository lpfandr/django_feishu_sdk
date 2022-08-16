#!/usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:lenovo
@file: setup.py
@time: 2022/8/15  15:35
"""
import setuptools

# 自动读取readme
with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()
setuptools.setup(
    name="django_feishu_sdk",  # Replace with your own username
    version="0.1.1",
    author="lpf_andr",
    author_email="lpf_andr@163.com",
    description="A feishu api package for django",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/lpfandr/django_feishu_sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=['cryptography', 'pydantic', 'aiohttp', 'requests', 'pycryptodome'],  # 安装所需要的库
)
