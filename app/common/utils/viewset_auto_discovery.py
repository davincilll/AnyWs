import importlib.util
import re
import sys
import typing
from os import PathLike
from pathlib import Path

from app.common.LoggerCenter import common_logger
from app.settings import PROJECT_PATH


class ViewSetDiscovery:
    """实现ViewSet的自动扫描机制"""

    _instance = None

    def __new__(cls, project_root_path: typing.Union[PathLike, str],
                booster_dirs: typing.List[typing.Union[PathLike, str]],
                max_depth=1, py_file_re_str: str = None):
        if cls._instance is None:
            cls._instance = super(ViewSetDiscovery, cls).__new__(cls)
            cls._instance.__init__(project_root_path, booster_dirs, max_depth, py_file_re_str)
        return cls._instance

    def __init__(self, project_root_path: typing.Union[PathLike, str],
                 booster_dirs: typing.List[typing.Union[PathLike, str]],
                 max_depth=1, py_file_re_str: str = None):
        """
        :param project_root_path 项目根目录
        :param booster_dirs: @装饰器函数函数所在的模块的文件夹,不用包含项目根目录长路径
        :param max_depth: 查找多少深层级子目录
        """

        self.full_path_dirs = [Path(project_root_path) / Path(boost_dir) / 'views' for boost_dir in booster_dirs]
        self.max_depth = max_depth
        self.py_file_re_str = py_file_re_str
        self.py_files = []
        self.count = 0

    def get_py_files_recursively(self, current_folder_path: Path, current_depth=0, ):
        """先找到所有py文件"""
        if current_depth > self.max_depth:
            return
        for item in current_folder_path.iterdir():
            if item.is_dir():
                self.get_py_files_recursively(item, current_depth + 1)
            elif item.suffix == '.py':
                if self.py_file_re_str:
                    if re.search(self.py_file_re_str, str(item), ):
                        self.py_files.append(str(item))
                else:
                    self.py_files.append(str(item))
        self.py_files = list(set(self.py_files))

    def auto_discovery(self, ):
#         common_logger.debug(f"我在进行第{self.count}次扫描")
        self.count += 1
        for _dir in self.full_path_dirs:
            if not Path(_dir).exists():
                # raise Exception(f'没有这个文件夹 ->  {_dir}')
                continue
            self.get_py_files_recursively(Path(_dir))
            for file_path in self.py_files:
                # common_logger.debug(file_path)
                if Path(file_path) == Path(sys._getframe(1).f_code.co_filename):
                    continue
                module_name = Path(file_path).as_posix().replace('/', '.') + '.' + Path(file_path).stem
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)


class ScanHelper:
    _instance = None

    def __new__(cls, installed_app, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ScanHelper, cls).__new__(cls)
            cls._instance.__init__(installed_app)
        return cls._instance

    def __init__(self, installed_app):
        self.installed_app = installed_app
        self.hasDiscovered = False
        self.to_be_scanned_app_names = []
        self.count = 0

    def extract_to_be_scanned_app_names(self):
        for app in self.installed_app:
            pattern = r"^(.*?)\.apps\."
            match = re.search(pattern, app)
            if match:
                self.to_be_scanned_app_names.append(match.group(1))

    def scan_only_once(self):
        common_logger.debug(f"我在进行第{self.count + 1}次scan_only_once")
        self.count += 1
        if self.hasDiscovered:
            return
        self.extract_to_be_scanned_app_names()
        # common_logger.debug(self.to_be_scanned_app_names)
        ViewSetDiscovery(PROJECT_PATH, self.to_be_scanned_app_names).auto_discovery()
        self.hasDiscovered = True
