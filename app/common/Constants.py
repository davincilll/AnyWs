from system_module.models import SystemConfiguration


class ProxyConstants:
    # 单例模式
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProxyConstants, cls).__new__(cls)
            cls._instance.__init__()
        return cls._instance

    def __init__(self):
        pass

    def __getattribute__(self, item):
        try:
            # 尝试获取属性
            return super().__getattribute__(item)
        except AttributeError:
            # 如果属性不存在，则从 SystemConfiguration 中获取
            sys_solo = SystemConfiguration.get_solo()
            value = getattr(sys_solo, item)
            return value


Constants = ProxyConstants()
