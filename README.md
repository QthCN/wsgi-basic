# WSGI-BASIC

## 说明

WSGI-BASIC从openstack/keystone中分离出wsgi相关代码并根据需求进行相关方便开速开发的修改，其目的是用于提供一个可以提供RESTful的HTTP API服务开发框架。

## 配置文件生成

默认的配置文件通过如下命令生成：

```
[stack@dev wsgi-basic]$ pwd
/opt/stack/wsgi-basic
[stack@dev wsgi-basic]$ oslo-config-generator --config-file=config-generator/wsgi-basic.conf
[stack@dev wsgi-basic]$ ls -l etc/wsgi-basic.conf.sample
-rw-rw-r-- 1 stack stack 27791 Aug 21 17:24 etc/wsgi-basic.conf.sample
```

## 运行测试：

WSGI-BASIC提供了一套API测试框架。代码可以在wsgi_basic.tests下找到。测试前启动服务，然后在test.ini中设置对应服务地址。运行测试的方法为：

```
[stack@dev wsgi-basic]$ cat etc/test.ini
[test]
TARGET_SERVICE_ADDRESS = http://127.0.0.1:5000
ADMIN_USERNAME = admin
ADMIN_PASSWORD = password
USERNAME = user
PASSWORD = password
MYSQL_HOST = 127.0.0.1
MYSQL_PORT = 3306
MYSQL_USER = root
MYSQL_PASSWORD = rootroot
MYSQL_SCEHMA = wsgi_basic

[stack@dev wsgi-basic]$ pwd
/opt/stack/wsgi-basic
[stack@dev wsgi-basic]$ python wsgi_basic/tests/main.py
#测试用例结果输出
```

## 生成新项目：

生成一个新项目的方法如下：

```
```