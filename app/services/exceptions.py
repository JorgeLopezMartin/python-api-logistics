class ClientNotFoundException(Exception):
    """Client can not be found"""

class ClientDuplicatedException(Exception):
    """Client already exists"""

class LocationNotFoundException(Exception):
    """Location can not be found"""

class LocationDuplicatedException(Exception):
    """Location already exists"""