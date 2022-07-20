from src.backsrc.error.error import Error
from src.bin.ADT import _Var, Number, _Symbol, _Function, _List, Atom


class Var(_Var):
    def __init__(self, token, superType=None):
        self.value = token.value
        self.superType = self.typeSet(token, superType)
        self.type = superType

    def typeSet(self, token, superType=None):
        if superType is None:
            return 'Int' if type(token.value) == int else 'Real'
        else:
            if isinstance(token.value, int):
                return 'Int'
            elif isinstance(token.value, float):
                return "Real"
            elif isinstance(token.value, str):
                return "Symbol"

    def __repr__(self):
        return '__Main__.__object__.Var ' \
               'Value : {value}\nType: {type}\nSuperType: {supertype}'.format(
                value=self.value,
                type=self.type,
                supertype=self.superType)


class Num(Number):
    def __init__(self, value, tokenType=None):
        self.value = value
        self.name = self.__class__.__name__
        self.type = self.setType(value) if tokenType is None else tokenType

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "__Main__.__object__.{name}.value : {value}".format(
            name=self.name,
            value=self.value
        )

    def setType(self, value):
        if isinstance(value, int):
            return 'Int'
        else:
            return 'Real'


class String(_Symbol):
    def __init__(self, token=None):
        self._value = token.value
        self.name = self.__class__.__name__

    def value(self):
        return self._value

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.name + "." + self.value()


class Nil:
    def __init__(self, value=0, type='Nil'):
        self.value = value
        self.type = type

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "__Main__." + self.__class__.__name__ + ".Obj"


class Function(_Function):
    def __init__(self, name=None, body=None):
        self.name = name
        self.body = body

    def __call__(self, *args):
        self.function_evaluation(args)

    def function_evaluation(self, function_init_value):
        if len(function_init_value) != len(self.body.arg):
            raise Exception('This Function arguments take {0} argument not {1}'.format(
                len(self.body.arg), len(function_init_value)
            ))
        if self.body.arg is None or type(self.body.arg) is int:
            raise Exception
        else:
            return self.body


class Function_Body(_Function):
    def __init__(self, arg=None, procedure=None):
        self.arg = arg
        self.procedure = procedure


class List(_List):
    __slots__ = ('list', 'size', 'list_name')

    def __init__(self, list_name=None, size=None, values=None):
        self.size = size
        self.list_name = list_name
        self.type = "LIST"
        self._value = self._inArg(values)
        self.temp = self.value()

    def value(self):
        _ = [self._value[x] for x in range(0, len(self._value))]
        return _

    def _findArg(self, value):
        if self._sizeOfList() == 0:
            raise Error(message='Can\'t find Any Argument. Because list is Empty : (')
        else:
            for rea, reb in self.list.items():
                if reb == value:
                    return f'{reb} is [{rea}] index'
            else:
                return None

    def _sizeOfList(self):
        return len(self.list)

    def _inArg(self, args):
        lisVal = {}
        for rea, reb in enumerate(args):
            lisVal[rea] = reb
        return lisVal

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        result = ""
        for val in range(0, len(self._value)):
            result += str(f" {self._value[val].value} ")
        return result


class Cons:
    def __init__(self, *value):
        self.value = value
        self.cons_output = ''

    def cons_check(self):
        if self.value is None:
            raise Exception
        else:
            for rea in range(len(self.value)):
                try:
                    if self.value[rea].isupper():
                        self.value[rea].upper()
                except ValueError:
                    pass

    def cons_out(self):
        self.cons_output += '( '
        for rea in self.value:
            self.cons_output += rea
            self.cons_output += ' '
            if rea != self.value[-1]:
                self.cons_output += '.'
        self.cons_output += ' )'


class AtomType_Token(Atom):
    def __init__(self, type, value, line_no=None, col_no=None):
        self.type = type
        self.value = value
        self.line_no = line_no
        self.col_no = col_no

    def __str__(self):
        if self.line_no is None and self.col_no is None:
            return '\nATOMTYPE_TOKEN VALUE : {value} TYPE : {type}'.format(
                value=self.value,
                type=self.type
            )
        else:
            return '\nATOMTYPE_TOKEN VALUE : {value} TYPE : {type}\nLine : {line} Col : {col}'.format(
                value=self.value,
                type=self.type,
                line=self.line_no,
                col=self.col_no
            )

    def __repr__(self):
        return self.__str__()


class Unary_Operand_AtomType_Token(AtomType_Token):
    def __init__(self, type, value, line_no=None, col_no=None):
        self.type = type
        self.value = value
        self.line_no = line_no;
        self.col_no = col_no

    def __str__(self):
        if self.line_no is None and self.col_no is None:
            return '\nUNARY_OPERAND_TOKEN_TYPE VALUE : {value}, EXPR: {expr}'.format(
                value=self.type,
                expr=self.value,
            )
        else:
            return '\nUNARY_OPERAND_TOKEN_TYPE VALUE : {value}, EXPR: {expr}\nLine : {line} Col : {col}'.format(
                value=self.type,
                expr=self.value,
                line=self.line_no,
                col=self.col_no
            )

    def __repr__(self):
        return self.__str__()


class Global_Function_Count(_Function):
    def __init__(self):
        self.function_Count = 0b00

    def __add__(self, other):
        self.function_Count += other


class Nil:
    def __init__(self):
        self.type = Nil

    def __call__(self, *args, **kwargs):
        return None


class Bool:
    def __init__(self, value):
        self.value = value

    def __bool__(self):
        if self.value == "#t":
            return True
        elif self.value == "#f":
            return False

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "__Main__." + self.__class__.__name__ + "." + self.value


class Quote:
    def __init__(self, args=None):
        self.value = None if args is None else args
        self.type = "QUOTE"
        self.length = None if args is None else len(args)
        self.args = args

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "__Main__." + self.__class__.__name__ + ".Obj." + self._literal()

    def _literal(self):
        if self.value is None:
            return "Nil"
        result = "("
        for _ in self.value:
            result += f' {_.value} '
        return result + ")"

    def __add__(self, other):
        if self.value is None:
            self.value = [Num(0) for _ in range(0, len(other.value))]
            result = Quote(list(map(lambda x, y: Num(value=x.value + y.value), self.value, other.value)))
            return result
        else:
            if len(self.value) != len(other.value):
                return -1
            else:
                result = Quote(list(map(lambda x, y: Num(value=x.value + y.value), self.value, other.value)))
                return result

    def __sub__(self, other):
        if self.value is None:
            self.value = [Num(0) for _ in range(0, len(other.value))]
            result = Quote(list(map(lambda x, y: Num(x.value - y.value), self.value, other.value)))
            return result
        else:
            if len(self.value) != len(other.value):
                return -1
            else:
                result = Quote(list(map(lambda x, y: Num(x.value - y.value), self.value, other.value)))
                return result

    def __mul__(self, other):
        if self.value is None:
            self.value = [Num(1) for _ in range(0, len(other.value))]
            result = Quote(list(map(lambda x, y: Num(x.value * y.value), self.value, other.value)))
            return result
        else:
            if len(self.value) != len(other.value):
                return -1
            else:
                result = Quote(list(map(lambda x, y: Num(x.value * y.value), self.value, other.value)))
                return result

    def __divmod__(self, other):
        if self.value is None:
            self.value = [Num(1) for _ in range(0, len(other.value))]
            result = Quote(list(map(lambda x, y: Num(x.value / y.value), self.value, other.value)))
            return result
        else:
            if len(self.value) != len(other.value):
                return -1
            else:
                result = Quote(list(map(lambda x, y: Num(x.value / y.value), self.value, other.value)))
                return result


class Lambda:
    def __init__(self, body, arg):
        self.function_body = body
        self.arg = arg
        self.name = self.__class__.__name__
        self.type = "LAMBDA"

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "__Main__." + self.name + ".Obj"

    def setVal(self, node):
        if node is None:
            return self.function_body
        else:
            if len(node) != len(self.arg):
                return -1
            self.arg = dict(zip(self.arg, node))
            for _, _2 in self.arg.items():
                for __ in range(len(self.function_body)):
                    if self.function_body[__].value == _:
                        self.function_body[__] = _2
