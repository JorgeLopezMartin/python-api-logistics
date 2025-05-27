class CargoNotDeletableException(Exception):
    """Cargo cannot be deleted"""

class CargoNotFoundException(Exception):
    """Cargo can not be found"""

class CargoDuplicatedException(Exception):
    """Cargo already exists"""

class CargoAlreadyDeliveredException(Exception):
    """Cargo has already been delivered and cannot move"""

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

class TrackNotDeletableException(Exception):
    """Track cannot be deleted"""

class TrackNotFoundException(Exception):
    """Track can not be found"""

class TrackDuplicatedException(Exception):
    """Track already exists"""

class VesselNotDeletableException(Exception):
    """Vessel cannot be deleted"""

class VesselNotFoundException(Exception):
    """Vessel can not be found"""

class VesselDuplicatedException(Exception):
    """Vessel already exists"""