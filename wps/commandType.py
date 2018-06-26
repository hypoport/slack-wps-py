from enum import Enum


class CommandType(Enum):
    SET = 'set'
    GET = 'get'
    GET_GROUP = 'getGroup'
    CLEAR = 'clear'
