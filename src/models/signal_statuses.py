from enum import Enum

class SignalStatuses(Enum):
    DUMPED = 'Dumped'
    DONE = 'OK'
    FAILED = 'Failed'
    PENDING = 'Pending'


