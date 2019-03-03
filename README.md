

# zlAsset
zili的测试



#### event

##### 2019/2/24

自动化-作业 完成50&  ,下次写作业测试.如果有时间吧执行也写了

##### 2019/1/30

OS同步完成.

##### 2019/1/12

码一点,争取把ilo撸完,然后停段时间,要充电..讲课..


##### 2019/1/7

停止更新.
近期暂无时间撸了...


#### celery

使用redis 还需要安装相关组件

pip3 install -U celery[redis]


在项目下 启动work和beat

`export PYTHONOPTIMIZE=1 && celery -A zlAsset worker -l info -B`


##### flower

启动默认是amqp
更改为配置的redis消息队列

`celery flower --broker=redis://:123qweASD@192.168.1.244:6379/1`

[localhost:5555](localhost:5555)



#### 功能介绍

##### 资产/组织设置.

可配置常用设备和型号等,联系人信息等等,供后续添加设备时进行选择.

![资产设置](https://github.com/dl1548/zlAsset/blob/master/zlAsset/readme_img/setData.png)

![组织设置](https://github.com/dl1548/zlAsset/blob/master/zlAsset/readme_img/setOrg.png)

##### 服务器信息

可添加服务器资产,并设置信息的同步(同步可开启/关闭,默认开启)

![添加资产](https://github.com/dl1548/zlAsset/blob/master/zlAsset/readme_img/addHd.png)

![资产列表](https://github.com/dl1548/zlAsset/blob/master/zlAsset/readme_img/hdData.png)

![同步信息](https://github.com/dl1548/zlAsset/blob/master/zlAsset/readme_img/hdSync.png)

##### 操作系统信息

功能等同于服务器.

![添加系统](https://github.com/dl1548/zlAsset/blob/master/zlAsset/readme_img/addOs.png)

![同步信息](https://github.com/dl1548/zlAsset/blob/master/zlAsset/readme_img/osSync.png)

![同步信息-01](https://github.com/dl1548/zlAsset/blob/master/zlAsset/readme_img/osSync-01.png)

![同步信息02](https://github.com/dl1548/zlAsset/blob/master/zlAsset/readme_img/osSync-02.png)

##### 自动化

功能: 新建作业(也就是脚本). 后期调用作业名进行对主机的批量操作

![作业主页](https://github.com/dl1548/zlAsset/blob/master/zlAsset/readme_img/jobs_index.png)

添加作业可运行代码测试,如果感觉自己的脚本没问题,当然也可以不运行

![作业添加](https://github.com/dl1548/zlAsset/blob/master/zlAsset/readme_img/add_job.png)

执行结果展示.

![作业测试](https://github.com/dl1548/zlAsset/blob/master/zlAsset/readme_img/test_job.png)
