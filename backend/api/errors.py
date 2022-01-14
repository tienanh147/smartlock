class RequestBodyError(Exception): 
    '''
    Raise if parsing data does not meet required fields
    '''
    pass 


class UserNotFoundError(Exception):
    '''
    Raise if user not exist in database
    '''
    pass

class AuthenticatedError(Exception):
    '''
    Raise if username/password not match
    '''
    pass

class NotAllowedError(Exception):
    '''
    raise if the operation is not allowed
    '''
    pass

class NotFoundError(Exception): 
    '''
    raise if the object can not be found in the database
    '''
    pass