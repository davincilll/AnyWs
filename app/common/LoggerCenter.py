# 配置django应用的日志器
import os.path

import nb_log

# 绝对父路径
absolute_path = os.path.dirname(__file__)
# 获取django应用的日志器,info级别
django_logger = nb_log.get_logger("django", log_level_int=20,
                                  log_path=os.path.join(absolute_path, "../logs/django_logs"))
# 获取一般的日志器，用于记录一些非django的日志
common_logger = nb_log.get_logger("common", log_path=os.path.join(absolute_path, "../logs/common_logs"))
# 异常捕获日志
exception_logger = nb_log.get_logger("error", log_path=os.path.join(absolute_path, "../logs/error_logs"))
