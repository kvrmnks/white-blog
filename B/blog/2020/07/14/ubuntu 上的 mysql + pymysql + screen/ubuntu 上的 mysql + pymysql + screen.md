安装mysql
```
apt install mysql-server
apt install mysql-client
```
然后先看 mysql 的版本, 一定要注意版本
不同版本的 mysql 改密码的方式是不同的
比如 mysql8.0 的情况下
```
use mysql;
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '你的新密码'
```
退出即可

当然可能不知道一开始的密码
```
vim /etc/mysql/debian.cnf
```
```
screen -S 名字
```

```
ctrl+a     d 离开当前
```

```
screen -r 名字恢复
```

```
Debian平台的my.cnf
在/etc/mysql/mysql.conf.d/mysqld.cnf
```
```
wait_timeout=31536000
interactive_timeout=31536000
```
