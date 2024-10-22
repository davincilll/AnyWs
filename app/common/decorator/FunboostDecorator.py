# import time
# import traceback
# from functools import wraps
#
# from django.core.cache import cache
# from funboost import funboost_current_task
#
# from app.common.Constants import Constants
# from app.common.LoggerCenter import task_logger
#
#
# def backOffRetry(initial_delay=15, max_retry_times=15, max_delay=24 * 3600, backoff_factor=2):
#     """使用退避算法的装饰器，需要配合自定义的BoostParams来使用"""
#
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             fct = funboost_current_task()
#             task_id = fct.function_result_status.task_id
#             run_times_key = f"{Constants.REDIS_KEY_TASK_RUN_TIMES}{task_id}"
#             retry_times_key = f"{Constants.REDIS_KEY_TASK_RETRY_TIMES}{task_id}"
#
#             run_times = cache.get(run_times_key, 0)
#             retry_times = cache.get(retry_times_key, 0)
#
#             if run_times == 0:
#                 # 尝试执行
#                 try:
#                     func(*args, **kwargs)
#                 except Exception as e:
#                     run_times += 1
#                     cache.set(run_times_key, run_times)
#                     # 开始重试
#                     while retry_times < max_retry_times:
#                         try:
#                             func(*args, **kwargs)
#                             # 成功后跳出重试
#                             break
#                         except Exception as e:
#                             task_logger.error(str(e) + traceback.format_exc())
#                             retry_times += 1
#                             cache.set(retry_times_key, run_times)
#                             if retry_times == max_retry_times:
#                                 task_logger.info(
#                                     f"task_id: {task_id}, run_times: {run_times},已完成的retry_times: {retry_times},已达最大重试次数{max_retry_times}")
#                                 raise e
#                             else:
#                                 sleep_time = min(initial_delay * backoff_factor ** retry_times, max_delay)
#                                 task_logger.info(
#                                     f"task_id: {task_id}, run_times: {run_times},已完成的retry_times: {retry_times}, 下次重试需要等待sleep_time: {sleep_time}")
#                                 time.sleep(sleep_time)
#             else:
#                 while retry_times < max_retry_times:
#                     try:
#                         func(*args, **kwargs)
#                         # 成功后跳出重试
#                         break
#                     except Exception as e:
#                         retry_times += 1
#                         task_logger.error(str(e) + traceback.format_exc())
#                         if retry_times == max_retry_times:
#                             task_logger.info(
#                                 f"task_id: {task_id}, run_times: {run_times},已完成的retry_times: {retry_times},已达最大重试次数{max_retry_times}")
#                             raise e
#                         else:
#                             sleep_time = min(initial_delay * backoff_factor ** run_times, max_delay)
#                             task_logger.info(
#                                 f"task_id: {task_id}, run_times: {run_times},已完成的retry_times: {retry_times}, 下次重试需要等待sleep_time: {sleep_time}")
#                             time.sleep(sleep_time)
#             return func
#
#         return wrapper
#
#     return decorator
