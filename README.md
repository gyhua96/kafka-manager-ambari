# Kafka Manager for Ambari

> A custom service of Kafka Manager

## Installation
- 下载release的压缩包并解压
  
- 将KAFKA_MANAGER目录移动到ambari-server机器的如下路径
> /var/lib/ambari-server/resources/stacks/HDP/${stack.version}/services/

- 重启ambari-server
> ambari-server restart

- 在Ambari管理页面，选择添加服务，选择 kafka-manager 按提示进行安装即可