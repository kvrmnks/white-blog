建一篇blog记录一下进度
<!--more-->

#### 2020-4-28
起步
试图安装双系统，失败
用虚拟机的Qt有点辣眼睛
简单学了一下Qt基本内容，试了试QSocket

#### 2020-5-02
今天又收获了好多好多的坑呢

##### markdown->html
https://github.com/hoedown/hoedown
纯c手写，clone之后直接nmake一下，调用方法的话写 hoedown.exe -h 就好啦

##### nmake 相关
这个东西是Vs自带的，也就是说要装一个Vs
用everything 找 nmake.exe
然后注意这个的环境变量设置
要一个INCLUDE和LIB 都找一下
有的可能缺kernel32在LIB下找一下

##### webenginewidgets 中的 QWebEngineView
这个需要编译器是MSVC 2015+大约
然后只需要setHtml + show就好了
别忘记show

##### 资源文件相关
资源文件是直接编译进exe的所以只可读
资源文件的格式只有（目前发现）QFile能解析

##### 资源文件的地址转绝对地址
建一个虚拟文件目录 QTemporaryDir
const QString tmp = mainDir->path()+"/hoedown.exe";
QFile::copy(":/new/prefix1/project/hoedown.exe",tmp）；
然后把资源目录的文件复制进去
就可以用tmp访问了

##### 文件读写
```cpp
    QFile out("dududusdshdksjhdksout.txt");
    if(out.open(QIODevice::WriteOnly)){
       QTextStream ts(&out);
        ts<<textTextEdit->toPlainText();
        process->start(mainDir->path()+"/hoedown.exe --all-block --all-span --all-flags "+"dududusdshdksjhdksout.txt");
    }else{
        qDebug("wrong");
    }
```
##### 
##### 如何调用外部的exe
QProcess
https://blog.csdn.net/wzj0808/article/details/79367314

##### QProcess 中stdout的文件编码
https://blog.csdn.net/liukang325/article/details/80986472