# WSGI-BASIC

## 说明

WSGI-BASIC从openstack/keystone中分离出wsgi相关代码并根据需求进行相关方便开速开发的修改，其目的是用于提供一个可以提供RESTful的HTTP API服务开发框架。


## 生成新项目：

生成一个新项目的方法如下：

```
[stack@dev tmp]$ bash create_project.sh mywsgi MYWSGI
# 输出
......
[stack@dev tmp]$ cd mywsgi/
[stack@dev mywsgi]$ mywsgi-all 
2015-08-21 18:32:40.130 21762 INFO mywsgi.common.environment.eventlet_server [-] Starting /bin/mywsgi-all on 0.0.0.0:5000
2015-08-21 18:32:40.131 21762 INFO oslo_service.service [-] Starting 4 workers
2015-08-21 18:32:40.134 21762 INFO oslo_service.service [-] Started child 21771
2015-08-21 18:32:40.138 21762 INFO oslo_service.service [-] Started child 21772
2015-08-21 18:32:40.145 21771 INFO eventlet.wsgi.server [-] (21771) wsgi starting up on http://0.0.0.0:5000/
2015-08-21 18:32:40.145 21762 INFO oslo_service.service [-] Started child 21773
2015-08-21 18:32:40.151 21762 INFO oslo_service.service [-] Started child 21774
2015-08-21 18:32:40.157 21773 INFO eventlet.wsgi.server [-] (21773) wsgi starting up on http://0.0.0.0:5000/
2015-08-21 18:32:40.160 21772 INFO eventlet.wsgi.server [-] (21772) wsgi starting up on http://0.0.0.0:5000/
2015-08-21 18:32:40.168 21774 INFO eventlet.wsgi.server [-] (21774) wsgi starting up on http://0.0.0.0:5000/
```

create_project.sh脚本可以在git中找到，或者可以使用如下内容代替：

```
[root@dev mywsgi]# cat create_project.sh 
# usage:
# bash create_project.sh [project_name] [PROJECT_NAME]

echo "create project $1 | $2"
git clone https://github.com/QthCN/wsgi-basic.git
mv wsgi-basic $1
cd $1
sed -i "s/wsgi_basic/$1/g" `grep wsgi_basic -rl .`
sed -i "s/wsgi-basic/$1/g" `grep wsgi-basic -rl .`
sed -i "s/WSGI_BASIC/$2/g" `grep WSGI_BASIC -rl .`
mv wsgi_basic $1
oslo-config-generator --config-file=config-generator/wsgi-basic.conf
cp etc/wsgi-basic.conf.sample etc/$1.conf
cp etc/wsgi-basic-paste.ini etc/$1-paste.ini
sudo python setup.py develop
```

## 数据库初始化

数据库的初始化脚本在etc/init_db.sql中，直接执行即可：

```
MariaDB [(none)]> source /tmp/mywsgi/etc/init_db.sql;
```

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
......
```

## 增加一个资源

增加一个资源步骤如下：

1. 建立对应的package，如resource
2. 在resource这个package下建立routers.py/controllers.py/core.py。routers.py中用于存放URL到对应controller method的映射关系，controllers.py中存放控制层代码，core中提供model层代码。core可以决定是否要使用driver，如果要使用driver可以建立backends目录，并在setup.cfg中注册对应的entry point。
3. 在wsgi_basic.server.backends中写上对应的DRIVER初始代码
4. 在wsgi_basic.routers中加入新的resource的router规则

强烈建议参考user这个资源的编写方法来进行新资源代码的开发。
