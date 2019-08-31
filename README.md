QQ空间点赞机 
========= 
Pure Python project
 
![Environment](https://img.shields.io/badge/python-2.7-blue.svg)
[![License](https://img.shields.io/badge/licence-GPL%203.0-brightgreen.svg)](https://github.com/build2last/QzoneLiker/blob/master/LICENSE)

## Declaration
* It's a pure python project based on [QzoneLiker](https://github.com/zeruniverse/QzoneLiker).
* I Added web interface to it with Tornado framework.
* New process will be created on QLiker's activation.
* Configure conf.py before execution.

Run with:
> python main.py

## Function   
+ 自动对空间说说内容点赞，每N秒刷新一次，以子进程的形式在后台挂机运行

## Requirements
* Python 3
* PyExecJS
* **JavaScript runtime** 环境变量
* Tornado

## 2019-09 开发计划
- [x] 向 Python 3 升级，兼容 python 2.7
- [ ] 代码重构
- [ ] 白名单 / 黑名单 功能
- [ ] 日志精简
- [ ] 稳定性测试 / 容量测试
