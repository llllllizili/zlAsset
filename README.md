# zlAsset
zili的测试






#### celery

使用redis 还需要安装相关组件

pip3 install -U celery[redis]


在项目下 启动work和beat

`export PYTHONOPTIMIZE=1 && celery -A 项目 worker -l info -B`


##### flower

启动默认是amqp
更改为配置的redis消息队列

`celery flower --broker=redis://:123qweASD@192.168.1.244:6379/1`

[localhost:5555](localhost:5555)
