class PSVError(BaseException): pass
class TooMuchDataError(PSVError, ValueError): pass
class NoSuchClassError(PSVError, ValueError): pass
