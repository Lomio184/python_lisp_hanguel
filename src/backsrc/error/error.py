from enum import Enum
import sys

class ErrorToken(Enum):
    UNEXPECTED_TOKEN = 'Unexpected Token'
    ID_INVALID_TOKEN = 'This Id is unvaild type'
    STACK_ERROR = 'Stack Overflow Error'

class Error(Exception):
    pass