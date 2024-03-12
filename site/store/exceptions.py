class StoreError(Exception):
    pass


class CartNotFoundError(StoreError):
    pass


class PartNotFoundError(StoreError):
    pass


class UserNotOwnerOfOrderError(StoreError):
    pass