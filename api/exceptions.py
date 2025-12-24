"""
自定義異常
"""


class OrderAlreadyExistsError(Exception):
    """訂單已存在"""
    pass


class OrderNotFoundError(Exception):
    """訂單不存在"""
    pass


class InvalidOrderDataError(Exception):
    """訂單資料無效"""
    pass
