

# zlAsset
zili的测试



#### event

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


