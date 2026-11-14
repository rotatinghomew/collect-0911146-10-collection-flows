# 资料采集步骤与静态流程运行器

这是业务接收链路的现有项目。模块边界、来源行为和消费端格式见 `docs/contracts.md`。
演练仅使用项目自己的合成资料与环回服务，不读取外部账户或真实人员信息。

## 运行

Python 3.11。先在独立环境安装 `requirements.txt`；空文件表示仅用标准库。

```sh
python -m unittest discover -s tests -v
python -m compileall -q .
python demo.py
```

`demo.py` 从干净的临时目录运行当前业务路径，完整打印结构化结果后退出。
HTTP 服务绑定环回随机端口，由上下文管理器关闭；运行时不依赖外网。
原始证据和接收事件可用 `evidence.py` 保存在调用者指定的目录中。

## 容器

```sh
docker build -t collection-product .
docker run --rm --network none collection-product
docker run --rm --network none collection-product python -m unittest discover -s tests -v
```

镜像构建是依赖准备阶段。测试和演练在已准备的镜像中执行；不要在测试内安装依赖。
