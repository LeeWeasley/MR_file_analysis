通信系统中4G网络测量报告每时每刻都在生成并上传到服务器，都是以xml格式存储，那么如何读取单个、多个或批量的MR文件呢？

读取多个xml文件名采用的是python自带的os模块中os.walk(file_dir)函数
读取xml文件内容采用的是dom模块
数据清洗采用的是pandas模块
