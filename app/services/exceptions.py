class ClientNotDeletableException(Exception):
    """Client cannot be deleted"""

class ClientNotFoundException(Exception):
    """Client can not be found"""

class ClientDuplicatedException(Exception):
    """Client already exists"""

class ContractNotDeletableException(Exception):
    """Contract cannot be deleted"""

class ContractNotFoundException(Exception):
    """Contract can not be found"""

class ContractDuplicatedException(Exception):
    """Contract already exists"""

class LocationNotDeletableException(Exception):
    """Location cannot be deleted"""

class LocationNotFoundException(Exception):
    """Location can not be found"""

class LocationDuplicatedException(Exception):
    """Location already exists"""

class VesselNotDeletableException(Exception):
    """Vessel cannot be deleted"""

class VesselNotFoundException(Exception):
    """Vessel can not be found"""

class VesselDuplicatedException(Exception):
    """Vessel already exists"""