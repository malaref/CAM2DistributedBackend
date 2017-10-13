# CAM2DistributedBackend
A distributed back-end for the CAM<sup>2</sup> project using PySpark and HDFS.

## Architecture

**>> A visual presentation for the architecture alongside accompanying projects is available [here](https://docs.google.com/presentation/d/1hXiHFT1m0mmmVpFhNEOdYfZiU26u7oTLrFYzVyuO91s/edit?usp=sharing).**  
  
The distributed back-end uses Apache Spark for processing and Apache Hadoop Distributed File System (HDFS) for storage. From one end, Spark Standalone cluster setup consists of one master for coordination and several slaves to carry out the actual computation. From the other end, HDFS cluster setup consists of one namenode that stores meta-data information and several datanodes for the actual data storage.  
  
The recommended cluster setup is to run the Spark master daemon and the HDFS namenode daemon on one node (_manager_ node). Similarly, it is recommended to run the Spark slave daemon and the HDFS datanode daemon on the other nodes (_worker_ nodes).

## Requirements

### Requisite software

#### Java
* [Download](https://www.java.com/en/download/) and extract a release (tested with Java 8).

#### Apache Hadoop
* Make sure the requisite software is installed. For example, on Debian-based Linux, issue the command:
  ```shell
  sudo apt install ssh pdsh
  ```
* [Download](http://hadoop.apache.org/releases.html) and extract a release (tested with 2.7.4).
* Prepare its configuration in the `etc/hadoop/` directory as follows:
  - In `etc/hadoop/hadoop-env.sh` find the line `export JAVA_HOME=${JAVA_HOME}` and change it to point to where Java resides.
  - In `etc/hadoop/core-site.xml` add the following property to the `configuration` tag:
    ```xml
    <property>
      <name>fs.defaultFS</name>
      <value>hdfs://namenode_url:9000</value>
    </property>
    ```
    where _namenode_url_ is the namenode host name or IP (must be reachable from the datanodes).
  - In `etc/hadoop/hdfs-site.xml` add the following property to the `configuration` tag:
    ```xml
    <property>
      <name>dfs.replication</name>
      <value>1</value>
    </property>
    ```
  
For more details: check the [docs](http://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/ClusterSetup.html).

#### Apache Spark
* [Download](http://spark.apache.org/downloads.html) and extract a release (tested with 2.2.0).

### CAM2Environment
Create a file `~/CAM2Environment` and use it to set the environment variables `JAVA_HOME`, `HADOOP_HOME` and `SPARK_HOME` to point to the where each software resides:
```shell
JAVA_HOME=/path/to/java
HADOOP_HOME=/path/to/hadoop
SPARK_HOME=/path/to/spark
```
Alternatively, set the environment variables manually and make sure they are available for the upcoming scripts.

## Installation

Using [pip](https://pypi.python.org/pypi/pip):
```shell
pip install git+https://github.com/muhammad-alaref/CAM2DistributedBackend
```

## Start the cluster

On the _manager_ node:
```shell
CAM2StartManager
```

On the _worker_ nodes:
```shell
CAM2StartWorker manager_host maximum_concurrent_tasks
```
where _manager_host_ is the manager host name or IP (must be reachable from the workers) and _maximum_concurrent_tasks_ is the maximum number of tasks (cameras) assigned to this worker concurrently.

## Stop the cluster

On the _worker_ nodes:
```shell
CAM2StopWorker
```

On the _manager_ node:
```shell
CAM2StopManager
```
**>> Note the reversed order.**

## Local setup

Issue the previous (_manager_ + _worker_) commands on the same machine with _manager_host_=`localhost`.

## Usage

The recommended way is to use the [RESTful API](https://github.com/muhammad-alaref/CAM2RESTfulAPI) project.  
Alternatively, the `CAM2DistributedBackend` command can be used on any node on the cluster (preferably the manager node) with the parameters explained by the `CAM2DistributedBackend --help` command.
