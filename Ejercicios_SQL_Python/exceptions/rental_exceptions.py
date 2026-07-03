

class UserNotExists(Exception):
    pass

class UserNotActive(Exception):
    pass

class UserIsDelinquent(Exception):
    pass

class CarNotExists(Exception):
    pass

class CarNotAvailable(Exception):
    pass

class RentalNotFound(Exception):
    pass

class RentalCompletedAlready(Exception):
    pass