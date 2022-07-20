import math

from src.bin.ADT import _Compiler, Root_Atom, Atom_Builtin_Function, Atom
from src.bin.keywords import RESERVED_KEYWORDS
from .coreSrc.debug import Debug
from .env import GlobalEnv
from .object.type import AtomType_Token, Unary_Operand_AtomType_Token
from ..mainToken import *
try:
    import traceback
    import os;import time
    import operator as op
    from multiprocessing import Process
    from idna import unicode;
    from src.backsrc import comp
except:
    pass

DEBUG = Debug()

def standard_env():
    env = GlobalEnv()
    env.update(vars(math))
    env.update({
        '+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv,
        '>': op.gt, '<': op.lt, '>=': op.ge, '<=': op.le, '=': op.eq,
        '==' : lambda x,y : x == y,
        'ABS': abs,
        'append': op.add,
        'begin': lambda *x: x[-1],
        'equal?': op.eq,
        'LENGTH': len,
        'list': lambda *x: list(x),
        'list?': lambda x: isinstance(x, list),
        'MAP': map,
        'MAX': max,
        'MIN': min,
        'not': op.not_,
        'null?': lambda x: x == [],
        'procedure?': callable,
        'ROUND': round,
    })
    return env

standard_env = standard_env()

class Procedure(Atom_Builtin_Function):
    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env
    def __call__(self, *args):
        return visit_Atom(self.body, GlobalEnv(self.parms, args, self.env))


cls_fmt = '<builtin_Fuction {value}>'

HELP_RESERVED_KEYWORDS = {
    'CONS' : cls_fmt.format(value = 'CONS'),
    'DEFINE' : cls_fmt.format(value = 'DEFINE'),
    'IF'    : cls_fmt.format(value = 'IF'),
    'LAMBDA' : cls_fmt.format(value = 'LAMBDA'),
    'CAR' : cls_fmt.format(value = 'CAR'),
    'CDR' : cls_fmt.format(value = 'CDR'),
    'ADD' : cls_fmt.format(value = 'ADD'),
    'TRUE' : cls_fmt.format(value = 'TRUE'),
    'FALSE' : cls_fmt.format(value = 'FALSE'),
    'SET' :cls_fmt.format(value = 'SET'),
}


class Lexer(_Compiler):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.unary = self.pos
        self.current_char = self.text[self.pos]

    def __repr__(self):
        return 'CURRENT_CHAR : {value}'.format(value = self.current_char)

    def error(self):
        raise Exception

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def del_space(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def _id(self):
        result, token = '', ''
        while self.current_char is not None and self.current_char.isalpha():
            result += self.current_char
            self.advance()
            try:
                token = RESERVED_KEYWORDS.get(result)
            except:
                continue
        if token is None:
            token = AtomType_Token(SYMBOL, str(result))
            return token
        else:
            return token

    def make_int(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        if self.current_char == '.':
            result += self.current_char
            self.advance()

            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
            token = AtomType_Token(REAL, float(result))
        else:
            token = AtomType_Token(INT, int(result))

        return token

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.del_space()
                continue

            if self.current_char.isalpha():
                return self._id()

            if self.current_char.isdigit():
                return self.make_int()

            if self.current_char == '=':
                self.advance()
                try:
                    if self.current_char == '=':
                        self.advance()

                        token = RESERVED_KEYWORDS.get('ISEQUAL')
                        return token
                except ValueError:
                    pass
                return AtomType_Token(EQUAL, '=')

            if self.current_char == '+':
                self.advance()
                try:
                    if self.current_char == '=':
                        self.advance()
                        token = RESERVED_KEYWORDS.get('IPLUS')
                        return token
                except ValueError:
                    pass
                return AtomType_Token(PLUS, '+')

            #unary op + Just return minus token
            if self.current_char == '-':
                self.advance()
                try:
                    if self.current_char == '=':
                        self.advance()
                        token = RESERVED_KEYWORDS.get('IMIN')
                        return token
                    elif type(int(self.current_char)) == int:
                        result = ''
                        while self.current_char is not None and self.current_char.isdigit():
                            result += self.current_char
                            self.advance()
                        if self.current_char == '.':
                            result += self.current_char
                            self.advance()

                            while self.current_char is not None and self.current_char.isdigit():
                                result += self.current_char
                                self.advance()
                            token = Unary_Operand_AtomType_Token(REAL, -float(result))
                        else:
                            token = Unary_Operand_AtomType_Token(INT, -int(result))

                        return token
                except ValueError:
                    pass
                return AtomType_Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                try:
                    if self.current_char == '=':
                        self.advance()
                        token = RESERVED_KEYWORDS.get('IMUL')
                        return token
                except ValueError:
                    pass
                return AtomType_Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                try:
                    if self.current_char == '=':
                        self.advance()
                        token = RESERVED_KEYWORDS.get('IDIV')
                        return token
                except ValueError:
                    pass
                return AtomType_Token(DIV, '/')

            if self.current_char == '(':
                self.advance()
                return AtomType_Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return AtomType_Token(RPAREN, ')')

            self.error()
            return AtomType_Token(NIL, None)


class Parser(Lexer):
    global global_envs
    global DEBUG_STACK

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def __repr__(self):
        return 'CURRENT TOKEN : {value}'.format(value = self.current_token)

    def error(self):
        raise ValueError

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def opeat(self, token_value):
        if self.current_token.value == token_value:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def expr(self):
        while self.current_token is not None:
            if self.current_token.type == LPAREN:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(LPAREN)

            elif self.current_token.type == RPAREN:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(RPAREN)

            elif self.current_token.type == ABORT:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(ABORT)

            elif self.current_token.type == EQUAL:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(EQUAL)

            elif self.current_token.value == ISEQUAL:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.opeat(ISEQUAL)

            elif self.current_token.type == PLUS:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(PLUS)

            elif self.current_token.type == MINUS:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(MINUS)

            elif self.current_token.type == MUL:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(MUL)

            elif self.current_token.type == DIV:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(DIV)

            elif self.current_token.value == IMUL:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.opeat(IMUL)

            elif self.current_token.value == IDIV:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.opeat(IDIV)

            elif self.current_token.value == IPLUS:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.opeat(IPLUS)

            elif self.current_token.value == IMIN:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.opeat(IMIN)

            elif self.current_token.type == DISPLAY:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(DISPLAY)

            elif self.current_token.type == INPUT:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(INPUT)

            elif self.current_token.type == MAX:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(MAX)

            elif self.current_token.type == MIN:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(MIN)

            elif self.current_token.type == ABS:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(ABS)

            elif self.current_token.type == LENGTH:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(LENGTH)

            elif self.current_token.type == ROUND:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(ROUND)

            elif self.current_token.type == SYMBOL:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(SYMBOL)

            elif self.current_token.type == DEFINE:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(DEFINE)

            elif self.current_token.type == CONS:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(CONS)

            elif self.current_token.type == LAMBDA:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(LAMBDA)

            elif self.current_token.type == IF:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(IF)

            elif self.current_token.type == LET:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(LET)

            elif self.current_token.type == TYPE:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(TYPE)

            elif self.current_token.type == QUOTE:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(QUOTE)

            elif self.current_token.type == INT:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(INT)

            elif self.current_token.type == REAL:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(REAL)

            elif self.current_token.type in CONST:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(CONST)

            elif self.current_token.type == CAR:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(CAR)

            elif self.current_token.type == CDR:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(CDR)

            elif self.current_token.type == CAAR:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(CAAR)

            elif self.current_token.type == CADR:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(CADR)

            elif self.current_token.type == CDDR:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(CDDR)


            elif self.current_token.type == CDAR:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(CDAR)

            elif self.current_token.type == ADD:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(ADD)

            elif self.current_token.type == TRUE:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(TRUE)

            elif self.current_token.type == FALSE:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(FALSE)

            elif self.current_token.type == EQUAL:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(EQUAL)

            elif self.current_token.type == SET:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(SET)

            elif self.current_token.type == DEBUG:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(DEBUG)

            elif self.current_token.type == REPORT:
                DEBUG.__getitem__(self.current_token.type)
                global_envs.append(self.current_token.value)
                self.eat(REPORT)


        return global_envs


class SemanticAnalyzer(Parser):
    def __init__(self, parser):
        self.parser = parser
        self.inter = []

    def __repr__(self):
        return 'PARSER RESULT : {value},'.format(value = self.parser)

    def summin_parser(self):
        global global_envs
        global_envs = []
        return ' '.join(map(str, self.parser))

def factory(storage_name):
    def ty_getter(instance):
        return instance.__dict__[storage_name]

    def ty_setter(instance, value):
        if value > -2 **31 and value < 2 ** 31 -1:
            instance.__dict__[storage_name] = value
        else:
            raise ValueError('Value Must be int or float type')

    return property(ty_getter, ty_setter)

class Const_Token_Type(AtomType_Token):
    def __init__(self, value, name):
        self._value = value
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

    def __repr__(self):
        return 'CONST TOKEN TYPE\nVar : {name}\nValue : {value}'.format(
            name = self._name,
            value = self._value
        )

    def __call__(self):
        pass

def interpret(value):
    return value.replace('(', ' ( ').replace(')', ' ) ').split()

def make_stack(tokens):
    if len(tokens) == 0:
        raise SyntaxError('UNEXPECTED EOF WHILE READING')
    token = tokens.pop(0)
    if '(' == token:
        L = []
        while tokens[0] != ')':
            L.append(make_stack(tokens))
        tokens.pop(0)
        return L
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return atom_cast(token)

def atom_cast(token):
    if token is None:
        return 0
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return str(token)

def visit_Atom(interpret, env=standard_env):
    global DEBUG_CODE_OK
    if isinstance(interpret, str):
        return env.find(interpret)[interpret]

    elif not isinstance(interpret, list):
        return interpret

    elif len(interpret) is 1:
        if type(interpret[0]) == str:
            if interpret[0] == 'ABORT':
                return 'ABORT'
            proc = visit_Atom(interpret[0], env)
            if proc is not None:
                return proc

        return interpret[0]

    elif interpret[0] == '+=':
        (_, exp, val) = interpret
        if type(exp) is str and type(val) is str:
            rea = operand_parser(exp)
            reb = operand_parser(val)
            env[exp] = visit_Atom(rea + reb, env)

        if type(exp) is int and type(val) is int:
            return 'JUST USE OPERAND TYPE \'+\''

        elif type(exp) is str and type(val) is int:
            rea = operand_parser(exp)
            env[exp] = visit_Atom(rea + val, env)

        elif type(exp) is int and type(val) is str:
            reb = operand_parser(val)
            env[val] = visit_Atom(exp + reb, env)

    elif interpret[0] == '-=':
        (_, exp, val) = interpret
        if type(exp) is str and type(val) is str:
            rea = operand_parser(exp)
            reb = operand_parser(val)
            env[exp] = visit_Atom(rea - reb, env)

        if type(exp) is int and type(val) is int:
            return 'JUST USE OPERAND TYPE \'-\''

        elif type(exp) is str and type(val) is int:
            rea = operand_parser(exp)
            env[exp] = visit_Atom(rea - val, env)

        elif type(exp) is int and type(val) is str:
            reb = operand_parser(val)
            env[val] = visit_Atom(exp - reb, env)

    elif interpret[0] == '*=':
        (_, exp, val) = interpret
        if type(exp) is str and type(val) is str:
            rea = operand_parser(exp)
            reb = operand_parser(val)
            env[exp] = visit_Atom(rea * reb, env)

        if type(exp) is int and type(val) is int:
            return 'JUST USE OPERAND TYPE \'*\''

        elif type(exp) is str and type(val) is int:
            rea = operand_parser(exp)
            env[exp] = visit_Atom(rea * val, env)

        elif type(exp) is int and type(val) is str:
            reb = operand_parser(val)
            env[val] = visit_Atom(exp * reb, env)

    elif interpret[0] == '/=':
        (_, exp, val) = interpret
        if type(exp) is str and type(val) is str:
            rea = operand_parser(exp)
            reb = operand_parser(val)
            env[exp] = visit_Atom(rea / reb, env)

        if type(exp) is int and type(val) is int:
            return 'JUST USE OPERAND TYPE \'/\''

        elif type(exp) is str and type(val) is int:
            rea = operand_parser(exp)
            env[exp] = visit_Atom(rea / val, env)

        elif type(exp) is int and type(val) is str:
            reb = operand_parser(val)
            env[val] = visit_Atom(exp / reb, env)

    elif interpret[0] == 'QUOTE':
        (_, exp) = interpret
        return exp

    elif interpret[0] == 'IF':
        (_, test, conseq, alt) = interpret
        exp = (conseq if visit_Atom(test, env) else alt)
        return visit_Atom(exp, env)

    elif interpret[0] == 'DEFINE':
        (_, var, exp) = interpret
        env[var] = visit_Atom(exp, env)

    elif interpret[0] == 'SET':
        (_, var, exp) = interpret
        env.find(var)[var] = visit_Atom(exp, env)

    elif interpret[0] == 'CONST':
        (_, var, exp) = interpret
        const = Const_Token_Type(var, exp)
        return const


    elif interpret[0] == 'LET':
        pass

    elif interpret[0] == 'LAMBDA':
        (_, parms, body) = interpret
        return Procedure(parms, body, env)

    elif interpret[0] == 'DISPLAY':
        (_ , *exp) = interpret
        return exp

    elif interpret[0] == 'INPUT':
        return interpret

    elif interpret[0] == 'CAR':
        (_, *args) = interpret
        return args[0]

    elif interpret[0] == 'CDR':
        (_,exp , *args) = interpret
        return args

    elif interpret[0] == 'MAX':
        (_, *args) = interpret
        return max(args)

    elif interpret[0] == 'MIN':
        (_, *args) = interpret
        return min(args)

    elif interpret[0] == 'ROUND':
        (_, exp) = interpret
        if type(exp) is str:
            proc = eval(exp, env)
            if type(proc) is int:
                return round(proc)

        return round(exp)

    elif interpret[0] == 'LENGTH':
        (_, *args) = interpret
        return len(args)

    elif interpret[0] == 'ABS':
        (_, exp) = interpret
        return abs(exp)

    elif interpret[0] == 'CONS':
        return interpret

    elif interpret[0] == 'CAAR':
        (_, *args) = interpret
        exp = args[0]
        return exp

    elif interpret[0] == 'CADR':
        (_, exp, *val) = interpret
        rea = val[0]
        return rea

    elif interpret[0] == 'CDAR':
        (_, *val, exp) = interpret
        rea = val[0]
        return rea

    elif interpret[0] == 'CDDR':
        (_,exp, *val) = interpret
        temp = val[1:]
        return temp

    elif interpret[0] == 'TYPE':
        (_, exp) = interpret

        if type(exp) is str:
            cls_token = HELP_RESERVED_KEYWORDS.get(exp)
            if cls_token is not None:
                return cls_token
            else:
                proc = visit_Atom(exp, env)
                if type(proc) is int:
                    return 'ATOMTYPE_INT'
                if type(proc) is float:
                    return 'ATOMTYPE_FLOAT'

        elif type(exp) in (int, float):
            if type(exp) is int:
                return 'ATOMTYPE_INT'
            if type(exp) is float:
                return 'ATOMTYPE_FLOAT'

    elif interpret[0] == 'ADD':
        (_, *args) = interpret
        for i in range(len(args)):
            if isinstance(args[i], str):
                args[i] = visit_Atom(args[i], env)
        return sum(args)

    elif interpret[0] == 'EQUAL':
        (_,exp ,val) = interpret
        if exp == val:
            return TRUE
        else:
            return FALSE

    #fix this debug option problem
    elif interpret[0] == 'DEBUG':
        (_, bol) = interpret
        print(interpret)
        if bol is 'TRUE':
            DEBUG_CODE_OK = True
            return DEBUG_CODE_OK
        elif bol is 'FALSE':
            DEBUG_CODE_OK = False
            return DEBUG_CODE_OK

    elif interpret[0] == 'REPORT':
        return 'REPORT'

    else:
        proc = visit_Atom(interpret[0], env)
        args = [visit_Atom(exp, env) for exp in interpret[1:]]
        return proc(*args)

def operand_parser(tokens):
    if type(tokens) == str:
        proc = visit_Atom(tokens, standard_env)
        return proc
    else:
        return 'Undefined Token'


def print_expr(atom,):
    if atom is None:
        return 0

    if atom == 'REPORT':
        print(atom)
        return 'REPORT'

    if atom == 'ABORT':
        print('ABORT FUNCTION ########')
        return 'ABORT'

    if type(atom) is list:
        result = ''

        if atom[0] == 'CONS':
            for i in range(len(atom)):
                if type(atom[i]) is int:
                    atom[i] = str(atom[i])
            return ' . '.join(atom)

        if atom[0] == 'INPUT':
            return atom

        for i in atom:
            result += str(i) + ' '
        return '( ' + result + ')'

    if len(str(atom)):
        if isinstance(atom, float):
            return '(' + ''.join('{0:.3f}'.format(float(atom))) + ')'
        return '( ' + ''.join(str(atom)) + ' )'

