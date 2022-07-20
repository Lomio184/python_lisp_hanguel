from src.bin.ADT import _Function


class OperandFunction(_Function):
    __doc__ = "to evaluate binary operand with function"

    def __init__(self):
        self.functionSet = {}

    def toInitSet(self, functionCount , functionTable):
        self.functionSet[functionCount] = functionTable
        return

def greater_than(args):
    for _ in range(0, len(args) - 0b01):
        if args[_].value > args[_ + 0b01].value:
            pass
        else:
            return False
    return True

def less_than(args):
    for _ in range(0, len(args) - 0b01):
        if args[_].value < args[_ + 0b01].value:
            pass
        else:
            return False
    return True

def greater_equal(args):
    for _ in range(0, len(args) - 0b01):
        if args[_].value >= args[_ + 0b01].value:
            pass
        else:
            return False
    return True

def less_equal(args):
    for _ in range(0, len(args) - 0b01):
        if args[_].value <= args[_ + 0b01].value:
            pass
        else:
            return False
    return True

def equal(args):
    for _ in range(0, len(args) - 0b01):
        if args[_].value == args[_ + 0b01].value:
            pass
        else:
            return False
    return True

def quicksort(arr) -> None:
    def sort(less, great):
        if great <= less: return

        mid = merge(less, great)
        sort(less, mid - 1)
        sort(mid, great)

    def merge(less, great):
        pivot = arr[(less + great) // 2].value
        while less <= great:
            while arr[less].value < pivot:
                less += 1
            while arr[great].value > pivot:
                great -= 1
            if less <= great:
                arr[less].value, arr[great].value = arr[great].value, arr[less].value
                less, great = less + 1, great - 1
        return less
    return sort(0, len(arr) - 1)

qsort = quicksort

operandFunction = OperandFunction()