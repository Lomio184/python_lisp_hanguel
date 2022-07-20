from src.backsrc.buffer.standardIn import _input
from src.backsrc.buffer.standartOut import Print
from src.backsrc.env import globalEnv
from src.backsrc.error.error import Error, ErrorToken
from src.backsrc.object.type import AtomType_Token, Var, Function_Body, Function, List, Num, \
    Global_Function_Count, Bool, Quote, Lambda, Nil
from src.backsrc.coreSrc.operandFunction import greater_than, less_than, greater_equal, less_equal, \
    equal, qsort
from src.bin.ADT import _Compiler
from src.mainToken import *
import importlib
import colorama
import math

colorama.init(autoreset=True)

class LocalEnv(dict):
    def __init__(self, params=(), args=(), outer=None):
        self.update(zip(params, args))
        self.outer = outer

    def __del__(self):
        del self

localEnvi = LocalEnv()
nodeVal = []

class Compiler(_Compiler):
    def __init__(self, object_area=None):
        self.object = object_area
        self.pos = 0
        self.GLOBAL_FUNCTION_COUNT = Global_Function_Count()
        self.print_ok = True
        if self.object is not None:
            self.current_syn = self.object[self.pos]

    def eat(self, token_type):
        if self.current_syn.type == token_type:
            self.advance()
        else:
            raise Exception

    def advance(self):
        self.pos += 1
        if self.pos > len(self.object) - 1:
            self.current_syn = EOF
            return
        else:
            self.current_syn = self.object[self.pos]

    def checkNextNode(self):
        return self.object[self.pos+1]

    def func_eat(self):
        function_body = []
        if self.current_syn.type == LPAREN:
            lv = 1
        rv = 0
        while lv != rv:
            if self.current_syn.type == LPAREN:
                lv += 1
            elif self.current_syn.type == RPAREN:
                rv += 1
            function_body.append(self.current_syn)
            self.advance()
        return function_body

    def isEof(self):
        return self.object[self.pos + 1].type == EOF

    def clean(self):
        while self.current_syn.type != EOF:
            self.advance()
        if self.current_syn.type == RPAREN:
            self.advance()
        return

    def delRparen(self):
        while self.current_syn.type == RPAREN:
            self.advance()
        if self.current_syn.type == RPAREN:
            self.delRparen()
        return

    def isScope(self):
        if self.current_syn.type == LPAREN:
            return self.scope_eval1()
        elif self.current_syn.type == SYMBOL:
            if globalEnv.get(self.current_syn.value):
                proc = globalEnv.get(self.current_syn.value)
                self.eat(SYMBOL)
                return proc
            else:
                return self.current_syn
        else:
            token = self.current_syn
            self.advance()
            return token

    def setOperand(self):
        if self.current_syn.type == PLUS or self.current_syn.type == MINUS \
                or self.current_syn.type == DIV or self.current_syn.type == MUL:
            operand = self.current_syn
            self.advance()
        elif self.current_syn.type == SYMBOL:
            pass
        elif self.current_syn.type == LPAREN:
            operand = self.scope_eval1()
        return operand

    def errorRas(self, errMsg):
        if self.current_syn.line_no is None or self.current_syn.col_no is None:
            raise Error("{0} : {1}".format(
                errMsg,
                self.current_syn.value
            ))
        raise Error('{0} : {1}, LineNum : {2}, ColNum : {3}'.format(
            errMsg,
            self.current_syn.value,
            self.current_syn.line_no,
            self.current_syn.col_no
        ))

    def argument(self):
        arg = []
        if self.current_syn.type == LPAREN:
            self.eat(LPAREN)
            while self.current_syn.type != RPAREN:
                arg.append(self.current_syn.value)
                self.advance()
            self.eat(RPAREN)
            return arg
        else:
            return self.errorRas("Check your code :(")

    def scope_base(self):
        if self.current_syn.type == LPAREN or self.current_syn.type == GREAT or \
                self.current_syn.type == LESS or self.current_syn.type == GREAT_EQUAL or \
                self.current_syn.type == LESS_EQUAL or self.current_syn.type == EQUAL:
            if self.current_syn.type == LPAREN:
                self.eat(LPAREN)

            if self.current_syn.type == GREAT:
                self.eat(GREAT)
                compareObj = []
                while self.current_syn.type != RPAREN:
                    if self.current_syn.type == SYMBOL or self.current_syn.type == INT or \
                            self.current_syn.type == REAL or self.current_syn.type == SENTENCE:
                        if self.current_syn.type == SYMBOL:
                            val1 = globalEnv.get(self.current_syn.value)
                            if val1.type == FUNCTION:
                                compareObj.append(self.scope_eval1())
                            else:
                                self.eat(SYMBOL)
                            if val1 is None: raise Error(message="NoneType Object can't evaluate",
                                                         token=self.current_syn)

                        else:
                            compareObj.append(self.current_syn)
                            self.advance()

                self.eat(RPAREN)
                if greater_than(compareObj):
                    del compareObj
                    return Bool("#t")
                else:
                    del compareObj
                    return Bool("#f")

            elif self.current_syn.type == LESS:
                self.eat(LESS)
                compareObj = []
                while self.current_syn.type != RPAREN:
                    if self.current_syn.type == SYMBOL or self.current_syn.type == INT or \
                            self.current_syn.type == REAL or self.current_syn.type == SENTENCE:
                        if self.current_syn.type == SYMBOL:
                            val1 = globalEnv.get(self.current_syn.value)
                            if val1.type == FUNCTION:
                                compareObj.append(self.scope_eval1())
                            else:
                                self.eat(SYMBOL)
                            if val1 is None: raise Error(message="NoneType Object can't evaluate",
                                                         token=self.current_syn)

                        else:
                            compareObj.append(self.current_syn)
                            self.advance()
                self.eat(RPAREN)
                if less_than(compareObj):
                    del compareObj
                    return Bool("#t")
                else:
                    del compareObj
                    return Bool("#f")

            elif self.current_syn.type == GREAT_EQUAL:
                self.eat(GREAT_EQUAL)
                compareObj = []
                while self.current_syn.type != RPAREN:
                    if self.current_syn.type == SYMBOL or self.current_syn.type == INT or \
                            self.current_syn.type == REAL or self.current_syn.type == SENTENCE:
                        if self.current_syn.type == SYMBOL:
                            val1 = globalEnv.get(self.current_syn.value)
                            if val1.type == FUNCTION:
                                compareObj.append(self.scope_eval1())
                            else:
                                self.eat(SYMBOL)
                            if val1 is None: raise Error(message="NoneType Object can't evaluate",
                                                         token=self.current_syn)

                        else:
                            compareObj.append(self.current_syn)
                            self.advance()

                self.eat(RPAREN)
                if greater_equal(compareObj):
                    del compareObj
                    return Bool("#t")
                else:
                    del compareObj
                    return Bool("#f")

            elif self.current_syn.type == LESS_EQUAL:
                self.eat(LESS_EQUAL)
                compareObj = []
                while self.current_syn.type != RPAREN:
                    if self.current_syn.type == SYMBOL or self.current_syn.type == INT or \
                            self.current_syn.type == REAL or self.current_syn.type == SENTENCE:
                        if self.current_syn.type == SYMBOL:
                            val1 = globalEnv.get(self.current_syn.value)
                            if val1.type == FUNCTION:
                                compareObj.append(self.scope_eval1())
                            else:
                                self.eat(SYMBOL)
                            if val1 is None: raise Error(message="NoneType Object can't evaluate",
                                                         token=self.current_syn)

                        else:
                            compareObj.append(self.current_syn)
                            self.advance()

                self.eat(RPAREN)
                if less_equal(compareObj):
                    del compareObj
                    return Bool("#t")
                else:
                    del compareObj
                    return Bool("#f")

            elif self.current_syn.type == EQUAL:
                self.eat(EQUAL)
                compareObj = []
                while self.current_syn.type != RPAREN:
                    if self.current_syn.type == SYMBOL or self.current_syn.type == INT or \
                            self.current_syn.type == REAL or self.current_syn.type == SENTENCE:
                        if self.current_syn.type == SYMBOL:
                            val1 = globalEnv.get(self.current_syn.value)
                            if val1.type == FUNCTION:
                                compareObj.append(self.scope_eval1())
                            else:
                                self.eat(SYMBOL)
                            if val1 is None: raise Error(message="NoneType Object can't evaluate",
                                                         token=self.current_syn)

                        else:
                            compareObj.append(self.current_syn)
                            self.advance()

                self.eat(RPAREN)
                if equal(compareObj):
                    del compareObj
                    return Bool("#t")
                else:
                    del compareObj
                    return Bool("#f")
        else:
            self.scope_eval1()

    def scope_eval1(self):
        if self.current_syn.type == LPAREN:
            self.eat(LPAREN)
            if self.current_syn.type == RPAREN:
                return Nil()
            elif self.current_syn.type == EOF:
                raise Error("Please check your code", self.current_syn.value)
        # ----- #
        if self.current_syn.type == SYMBOL:
            if globalEnv.get(self.current_syn.value) is None:
                temp = self.current_syn
                self.eat(SYMBOL)
                if self.current_syn.type == RPAREN:
                    self.eat(RPAREN)
                return temp
            elif localEnvi.get(self.current_syn.value) is None:
                temp = self.current_syn
                self.eat(SYMBOL)
                if self.current_syn.type == RPAREN:
                    self.eat(RPAREN)
                return temp
            else:
                find_value = globalEnv.get(self.current_syn.value)
                self.advance()
                try:
                    if find_value.superType:
                        if find_value.superType == VAR:
                            return find_value
                except AttributeError:
                    pass
                if find_value.type == FUNCTION:
                    return self.function_eval(find_value.value)
                elif find_value.type == LIST:
                    if self.current_syn.type == SQUARE_LPAREN:
                        self.eat(SQUARE_LPAREN)
                        if self.current_syn.type == INT:
                            find_idx = self.current_syn.value
                            self.eat(INT)
                            self.eat(SQUARE_RPAREN)
                            try:
                                node = find_value.value.list[find_idx]
                                if self.isEof():
                                    self.eat(RPAREN)
                                    return node
                                else:
                                    node = globalEnv.get(node.value)
                                    if node.type == FUNCTION:
                                        return self.function_eval(node.value)
                            except KeyError:
                                return self.errorRas("Invaild Index! Check the index number")
                        else:
                            return self.errorRas("Can't executed this option. Only can Integer value")
                    else:
                        print(f"( {find_value.value} )")
                        self.clean()
                        return
                else:
                    self.clean()
                    node = setTheTokenTypeClass(find_value)
                    return node
        elif self.current_syn.type == INT:
            temp = self.current_syn
            self.eat(INT)
            if self.current_syn.type == RPAREN:
                self.eat(RPAREN)
            return temp
        elif self.current_syn.type == REAL:
            temp = self.current_syn
            self.eat(REAL)
            if self.current_syn.type == RPAREN:
                self.eat(RPAREN)
            return temp
        elif self.current_syn.type == SENTENCE:
            temp = self.current_syn
            self.advance()
            return temp
        elif self.current_syn.type == QUOTE:
            self.eat(QUOTE)
            _ = []
            if self.current_syn.type == LPAREN:
                self.eat(LPAREN)
                while self.current_syn.type != RPAREN:
                    _.append(self.current_syn)
                    self.advance()
                self.eat(RPAREN)
                quote = Quote(_)
                del _
                return quote
            else:
                return self.errorRas("Not a Literal Type")
        return self.scope_eval2()

    def scope_eval2(self):
        if self.current_syn.type == ISNULL:
            self.eat(ISNULL)
            if self.current_syn.type != LPAREN:
                raise Error(ErrorToken.UNEXPECTED_TOKEN, self.current_syn.value, "Can't Operate This Sentence")
            self.eat(LPAREN)
            if self.current_syn.type == RPAREN:
                self.clean()
                return Bool("#t")
            else:
                self.clean()
                return Bool("#f")

        elif self.current_syn.type == ISEQUAL:
            self.eat(ISEQUAL)
            node1 = self.isScope()
            node2 = self.isScope()
            if node1.value == node2.value:
                self.clean()
                return Bool("#t")
            else:
                self.clean()
                return Bool("#f")

        elif self.current_syn.type == ISZERO:
            self.eat(ISZERO)
            if self.current_syn.type == LPAREN:
                node = self.scope_eval1()
                if node.value == 0:
                    self.clean()
                    return Bool("#t")
                self.clean()
                return Bool("#f")
            else:
                if self.current_syn.type == SYMBOL:
                    if globalEnv.get(self.current_syn.value):
                        node = globalEnv.get(self.current_syn.value)
                        if node.value == 0:
                            self.clean()
                            return Bool("#t")
                        self.clean()
                        return Bool("#f")
                    elif localEnvi.get(self.current_syn.value):
                        node = localEnvi.get(self.current_syn.value)
                        if node.value == 0:
                            self.clean()
                            return Bool("#t")
                        self.clean()
                        return Bool("#f")
                    else:
                        return self.errorRas("Can't find this identifier!")
                else:
                    if self.current_syn.value == 0:
                        self.clean()
                        return Bool("#t")
                    self.clean()
                    return Bool("#f")

        elif self.current_syn.type == ISINTEGER:
            self.eat(ISINTEGER)
            if self.current_syn.type == LPAREN:
                node = self.scope_eval1()
                if node.type == INT:
                    self.clean()
                    return Bool("#t")
                self.clean()
                return Bool("#f")
            if self.current_syn.type == SYMBOL:
                if globalEnv.get(self.current_syn.value):
                    node = globalEnv.get(self.current_syn.value)
                    if node.type == INT:
                        self.clean()
                        return Bool("#t")
                    if node.type == VAR:
                        if node.superType == INT:
                            self.clean()
                            return Bool("#t")
                    self.clean()
                    return Bool("#f")
                elif localEnvi.get(self.current_syn.value):
                    node = localEnvi.get(self.current_syn.value)
                    if node.type == INT:
                        self.clean()
                        return Bool("#t")
                    self.clean()
                    return Bool("#f")
                else:
                    return self.errorRas("Can't find this identifier!")
            else:
                if self.current_syn.value == 0:
                    self.clean()
                    return Bool("#t")
                self.clean()
                return Bool("#f")

        elif self.current_syn.type == ISREAL:
            self.eat(ISREAL)
            if self.current_syn.type == LPAREN:
                node = self.scope_eval1()
                if node.type == REAL:
                    self.clean()
                    return Bool("#t")
                self.clean()
                return Bool("#f")
            if self.current_syn.type == SYMBOL:
                if globalEnv.get(self.current_syn.value):
                    node = globalEnv.get(self.current_syn.value)
                    if node.type == REAL:
                        self.clean()
                        return Bool("#t")
                    if node.type == VAR:
                        if node.superType == REAL:
                            self.clean()
                            return Bool("#t")
                    self.clean()
                    return Bool("#f")
                elif localEnvi.get(self.current_syn.value):
                    node = localEnvi.get(self.current_syn.value)
                    if node.type == REAL:
                        self.clean()
                        return Bool("#t")
                    self.clean()
                    return Bool("#f")
                else:
                    return self.errorRas("Can't find this identifier!")
            else:
                if self.current_syn.value == 0:
                    self.clean()
                    return Bool("#t")
                self.clean()
                return Bool("#f")

        elif self.current_syn.type == ISNUM:
            self.eat(ISNUM)
            if self.current_syn.type == LPAREN:
                node = self.scope_eval1()
                if node.type == REAL or node.type == INT:
                    self.clean()
                    return Bool("#t")
                self.clean()
                return Bool("#f")
            if self.current_syn.type == SYMBOL:
                if globalEnv.get(self.current_syn.value):
                    node = globalEnv.get(self.current_syn.value)
                    if node.type == REAL:
                        self.clean()
                        return Bool("#t")
                    if node.type == VAR:
                        if node.type == REAL or node.type == INT:
                            self.clean()
                            return Bool("#t")
                    self.clean()
                    return Bool("#f")
                elif localEnvi.get(self.current_syn.value):
                    node = localEnvi.get(self.current_syn.value)
                    if node.type == REAL or node.type == INT:
                        self.clean()
                        return Bool("#t")
                    self.clean()
                    return Bool("#f")
                else:
                    return self.errorRas("Can't find this identifier!")
            else:
                if self.current_syn.value == 0:
                    self.clean()
                    return Bool("#t")
                self.clean()
                return Bool("#f")

        elif self.current_syn.type == ISLIST:
            self.eat(ISLIST)
            if self.current_syn.type != SYMBOL:
                return self.errorRas("This identifier can't be list name : (")
            else:
                if globalEnv.get(self.current_syn.value):
                    node = globalEnv.get(self.current_syn.value)
                    if node.type == LIST:
                        self.clean()
                        return Bool("#t")
                    self.clean()
                    return Bool("#t")
                elif localEnvi.get(self.current_syn.value):
                    node = localEnvi.get(self.current_syn.value)
                    if node.type == LIST:
                        self.clean()
                        return Bool("#t")
                    self.clean()
                    return Bool("#f")
                else:
                    return self.errorRas("Dosen't exist")

        elif self.current_syn.type == ISPOSITIVE:
            self.eat(ISPOSITIVE)
            if self.current_syn.type == SYMBOL:
                if globalEnv.get(self.current_syn.value):
                    self.eat(SYMBOL)
                elif localEnvi.get(self.current_syn.value):
                    self.eat(SYMBOL)
                else:
                    return self.errorRas("Dosen't exist this value")
            elif self.current_syn.type == INT or self.current_syn.type == REAL:
                if self.current_syn.type == INT:
                    node = self.current_syn
                    self.eat(INT)
                    if node.value > 0:
                        self.clean()
                        return Bool("#t")
                    self.clean()
                    return Bool("#f")
                elif self.current_syn.type == REAL:
                    node = self.current_syn
                    self.eat(REAL)
                    if node.value > 0:
                        self.clean()
                        return Bool("#t")
                    self.clean()
                    return Bool("#f")

            elif self.current_syn.type == LPAREN:
                node = self.scope_eval1()
                if node.value > 0:
                    self.clean()
                    return Bool("#t")
                self.clean()
                return Bool("#f")

        elif self.current_syn.type == ISNEGATIVE:
            self.eat(ISNEGATIVE)
            if self.current_syn.type == SYMBOL:
                if globalEnv.get(self.current_syn.value):
                    self.eat(SYMBOL)
                elif localEnvi.get(self.current_syn.value):
                    self.eat(SYMBOL)
                else:
                    return self.errorRas("Dosen't exist this value")
            elif self.current_syn.type == INT or self.current_syn.type == REAL:
                if self.current_syn.type == INT:
                    node = self.current_syn
                    self.eat(INT)
                    if node.value < 0:
                        self.clean()
                        return Bool("#t")
                    self.clean()
                    return Bool("#f")
                elif self.current_syn.type == REAL:
                    node = self.current_syn
                    self.eat(REAL)
                    if node.value < 0:
                        self.clean()
                        return Bool("#t")
                    self.clean()
                    return Bool("#f")

            elif self.current_syn.type == LPAREN:
                node = self.scope_eval1()
                if node.value < 0:
                    self.clean()
                    return Bool("#t")
                self.clean()
                return Bool("#f")

        elif self.current_syn.type == PLUS:
            self.eat(PLUS)
            result = 0
            functionDoTable = []
            if self.current_syn.type == INT or self.current_syn.type == SYMBOL or \
                    self.current_syn.type == REAL or self.current_syn.type == LPAREN:
                while self.current_syn.type != RPAREN:
                    try:
                        if self.current_syn.type == LPAREN:
                            result += self.scope_eval1().value
                        elif self.current_syn.type == SYMBOL:
                            proc = globalEnv.get(self.current_syn.value)
                            if proc is None:
                                try:
                                    proc = localEnvi.get(self.current_syn.value)
                                except NameError:
                                    return self.errorRas("Can't find this identifier! Check the Code")
                                if proc is None:
                                    if self.current_syn.line_no is not None:
                                        return self.errorRas("Can't find this identifier! Check the Code")
                                    else:
                                        return self.errorRas("This Identifier is NoneType")
                                else:
                                    if proc.type == INT or proc.type == REAL:
                                        result += proc.value
                                        self.eat(SYMBOL)
                            else:
                                if proc.type == INT or proc.type == REAL:
                                    result += proc.value
                                    self.advance()

                                elif proc.type == FUNCTION:
                                    self.GLOBAL_FUNCTION_COUNT + 0b01
                                    while self.current_syn.type != RPAREN:
                                        functionDoTable.append(self.current_syn)
                                        self.advance()
                                    functionDoTable.append(self.current_syn)
                                    self.eat(RPAREN)
                                    result += function_new_eval_table(functionDoTable).value
                                    functionDoTable = []

                                elif proc.type == LIST:
                                    proc = self.scope_eval1()
                                    result += proc.value

                                else:
                                    result += proc.value
                                    self.eat(SYMBOL)
                        elif self.current_syn.type == INT:
                            result += self.current_syn.value
                            self.eat(INT)
                        elif self.current_syn.type == REAL:
                            result += self.current_syn.value
                            self.eat(REAL)

                    except ValueError:
                        break
            # --- return Area --- #
            if type(result) is int:
                self.eat(RPAREN)
                return Num(result, INT)
            elif type(result) is float:
                self.eat(RPAREN)
                return Num(result, REAL)
            else:
                return AtomType_Token(NIL, NIL)

        elif self.current_syn.type == MINUS:
            self.eat(MINUS)
            result = 0
            if self.current_syn.type == INT or self.current_syn.type == SYMBOL or \
                    self.current_syn.type == REAL or self.current_syn.type == LPAREN:
                if self.current_syn.type == SYMBOL:
                    if globalEnv.get(self.current_syn.value):
                        result = globalEnv.get(self.current_syn.value)
                    elif localEnvi.get(self.current_syn.value):
                        result = localEnvi.get(self.current_syn.value)
                    # ------ #
                    if result.type == FUNCTION:
                        result = self.scope_eval1().value
                    elif result.type == VAR:
                        result = result.value
                    elif result.type == INT or result.type == REAL:
                        result = result.value
                    self.advance()
                elif self.current_syn.type == INT:
                    result = self.current_syn.value
                    self.eat(INT)
                elif self.current_syn.type == REAL:
                    result = self.current_syn.value
                    self.eat(REAL)
                while self.current_syn.type != RPAREN:
                    try:
                        if self.current_syn.type == LPAREN:
                            node_result = self.scope_eval1().value
                            result -= node_result
                        elif self.current_syn.type == SYMBOL:
                            if globalEnv.get(self.current_syn.value):
                                node = globalEnv.get(self.current_syn.value)
                                if node.type == FUNCTION:
                                    node = self.scope_eval1().value
                                    result -= node
                                elif node.type == VAR:
                                    result -= node.value
                                self.advance()
                            elif localEnvi.get(self.current_syn.value):
                                node = localEnvi.get(self.current_syn.value)
                                if node.type == FUNCTION:
                                    pass
                                elif node.type == VAR:
                                    result -= node.value
                                elif node.type == INT:
                                    result -= node.value
                                self.advance()
                            else:
                                return self.errorRas("Can't find this identifier! Check your code")
                        elif self.current_syn.type == INT:
                            result -= self.current_syn.value
                            self.eat(INT)
                        elif self.current_syn.type == REAL:
                            result -= self.current_syn.value
                            self.eat(REAL)
                    except ValueError:
                        if self.current_syn.type == LPAREN:
                            return self.errorRas("Invalid Expression")
                if type(result) == int:
                    self.eat(RPAREN)
                    return Num(result, INT)
                elif type(result) == float:
                    self.eat(RPAREN)
                    return Num(result, REAL)
                else:
                    return AtomType_Token(NIL, NIL)

        elif self.current_syn.type == IPLUS:
            self.eat(IPLUS)
            if self.current_syn.type == SYMBOL:
                temp = self.current_syn.value
                self.eat(SYMBOL)
                if self.current_syn.type == INT:
                    globalEnv[temp].value += self.current_syn.value

        else:
            return self.scope_eval3()

    def scope_eval3(self):
        token = self.current_syn
        if token.type == MUL:
            self.eat(MUL)
            result = 1
            if self.current_syn.type == INT or self.current_syn.type == SYMBOL or \
                    self.current_syn.type == REAL or self.current_syn.type == VAR or \
                    self.current_syn.type == LPAREN:
                while self.current_syn.type != RPAREN:
                    try:
                        if self.current_syn.type == LPAREN:
                            node_result = self.scope_eval1()
                            result *= node_result.value
                        elif self.current_syn.type == SYMBOL:
                            if globalEnv.get(self.current_syn.value):
                                proc = globalEnv.get(self.current_syn.value)
                            elif localEnvi.get(self.current_syn.value):
                                proc = localEnvi.get(self.current_syn.value)
                            self.advance()
                            # ----- #
                            if proc.type == FUNCTION:
                                functionTable = []
                                while self.current_syn.type != RPAREN:
                                    functionTable.append(self.current_syn)
                                    self.advance()
                                functionTable.append(self.current_syn)
                                self.eat(RPAREN)
                                functionDoEval = function_new_eval_table(functionTable)
                                result = result * functionDoEval.value
                            else:
                                result = result * proc.value
                        elif self.current_syn.type == VAR:
                            result = result * self.current_syn.value
                            self.eat(VAR)
                        elif self.current_syn.type == INT:
                            result *= self.current_syn.value
                            if self.current_syn.type == INT:
                                self.eat(INT)
                            elif self.current_syn.type == INT:
                                self.eat(INT)
                        elif self.current_syn.type == REAL:
                            result *= self.current_syn.value
                            if self.current_syn.type == REAL:
                                self.eat(REAL)
                            elif self.current_syn.type == REAL:
                                self.eat(REAL)
                    except ValueError:
                        return self.errorRas("This Value can't operate this engine")
            if type(result) == int:
                self.eat(RPAREN)
                return Num(result, 'Int')
            elif type(result) == float:
                self.eat(RPAREN)
                return Num(result, REAL)
            else:
                return AtomType_Token(NIL, NIL)

        elif token.type == DIV:
            self.eat(DIV);
            result = 0
            if self.current_syn.type == INT or self.current_syn.type == SYMBOL or \
                    self.current_syn.type == REAL or self.current_syn.type == LPAREN:
                if self.current_syn.type == SYMBOL:
                    result = globalEnv.get(self.current_syn.value)
                    if result is None:
                        return self.errorRas("NoneType Error")
                    self.eat(SYMBOL)
                elif self.current_syn.type == INT:
                    result = self.current_syn.value
                    self.eat(INT)
                elif self.current_syn.type == REAL:
                    result = self.current_syn.value
                    self.eat(REAL)
                elif self.current_syn.type == LPAREN:
                    result = self.scope_eval1().value
                while self.current_syn.type != RPAREN:
                    try:
                        if self.current_syn.type == LPAREN:
                            result /= self.scope_eval1().value
                        elif self.current_syn.type == SYMBOL:
                            proc = globalEnv.get(self.current_syn.value)
                            result /= proc.value
                            self.eat(SYMBOL)
                        else:
                            if self.current_syn.type == INT:
                                result /= self.current_syn.value
                                self.eat(INT)
                            elif self.current_syn.type == REAL:
                                result /= self.current_syn.value
                                self.eat(REAL)
                    except ValueError:
                        return self.errorRas("This Value can't operate this engine")
                if type(result) == int:
                    return Num(result, 'Int')
                elif type(result) == float:
                    return Num(result, 'Float')
                else:
                    return AtomType_Token(NIL, NIL)
        else:
            return self.scope_eval4()

    def scope_eval4(self):
        token = self.current_syn
        if token.type == DEFINE or token.type == 정의:
            if token.type == DEFINE:
                self.eat(DEFINE)
            elif token.type == 정의:
                self.eat(정의)
            temp = self.current_syn.value
            self.advance()
            if self.current_syn.type == SYMBOL or self.current_syn.type == SENTENCE \
                    or self.current_syn.type == QUOTE or self.current_syn.type == INT or \
                    self.current_syn.type == REAL or self.current_syn.type == LPAREN:
                if self.current_syn.type == INT:
                    var = Var(self.current_syn, VAR)
                    self.eat(INT)
                    globalEnv[temp] = var

                elif self.current_syn.type == REAL:
                    var = Var(self.current_syn, VAR)
                    self.eat(REAL)
                    globalEnv[temp] = var

                elif self.current_syn.type == QUOTE:
                    _ = []
                    self.eat(QUOTE)
                    if self.current_syn.type == LPAREN:
                        self.eat(LPAREN)
                        while self.current_syn.type != RPAREN:
                            _.append(self.current_syn)
                            self.advance()
                        self.eat(RPAREN)
                        quote = Quote(_)
                        del _
                        globalEnv[temp] = quote
                    else:
                        return self.errorRas("This is not a Literal Type")

                elif self.current_syn.type == LPAREN:
                    node = self.scope_eval1()
                    if node.type == QUOTE:
                        globalEnv[temp] = node
                    else:
                        globalEnv[temp] = Var(node, VAR)

                elif self.current_syn.type == SENTENCE:
                    var = Var(self.current_syn, VAR)
                    globalEnv[temp] = var

                elif self.current_syn.type == SYMBOL:
                    if globalEnv.get(self.current_syn.value):
                        node = globalEnv.get(self.current_syn.value)
                        if node.type == FUNCTION:
                            globalEnv[temp] = node
                            self.eat(SYMBOL)
                        else:
                            globalEnv[temp] = node
                            self.eat(SYMBOL)

        elif token.type == SET:
            self.eat(SET)
            node = self.current_syn
            self.advance()
            node2=self.scope_eval1()
            localEnvi[node.value]=node2
            return node2

        elif token.type == IF or token.type == 만약:
            if token.type == IF:
                self.eat(IF)
            elif token.type == 만약:
                self.eat(만약)
            if self.current_syn.type != LPAREN:
                return self.errorRas('It can\'t operate this control option')
            else:
                condition = self.scope_base()
                if condition:
                    first_expr_node = self.scope_eval1()
                    return first_expr_node
                else:
                    while self.current_syn.type != RPAREN:
                        self.advance()
                    self.eat(RPAREN)
                while self.current_syn.type != LPAREN:
                    self.advance()
                if self.current_syn.type == LPAREN:
                    second_expr_node = self.scope_eval1()
                    return second_expr_node
                else:
                    return self.errorRas("Can't read this expression")


        elif token.type == DEFUN or token.type == 함수정의:
            if token.type == DEFUN:
                self.eat(DEFUN)
            elif token.type == 함수정의:
                self.eat(함수정의)
            function_name = self.current_syn.value
            argument = []
            self.eat(SYMBOL)
            if self.current_syn.type == LPAREN:
                self.eat(LPAREN)
                while self.current_syn.type != RPAREN:
                    if self.current_syn.type == SYMBOL:
                        argument.append(self.current_syn.value)
                        self.eat(SYMBOL)
                    elif self.current_syn.type == INT:
                        argument.append(self.current_syn.value)
                        self.eat(INT)
                    elif self.current_syn.type == REAL:
                        argument.append(self.current_syn.value)
                        self.eat(REAL)
                self.eat(RPAREN)
            function_body = self.func_eat()
            fb = Function_Body(argument, function_body)
            globalEnv[function_name] = AtomType_Token(FUNCTION, Function(function_name, fb))
            return

        elif token.type == LAMBDA:
            self.eat(LAMBDA)
            arg = self.argument()
            if self.current_syn.type == LPAREN:
                functionBody = []
                while self.current_syn.type != RPAREN:
                    functionBody.append(self.current_syn)
                    self.advance()
                functionBody.append(self.current_syn)
                self.delRparen()
                lam = Lambda(functionBody, arg = arg)
                return lam

        elif token.type == LET:
            self.eat(LET)
            if self.current_syn.type == LPAREN:
                self.eat(LPAREN)
                lvalue, rvalue = 1, 0
                while self.current_syn.type != EOF:
                    if lvalue == rvalue:
                        if self.current_syn.type == LPAREN:
                            if self.checkNextNode().type == LET:
                                self.eat(LPAREN)
                                self.eat(LET)
                                self.eat(LPAREN)
                                lvalue += 1
                            else:
                                break
                    else:
                        if self.current_syn.type == LPAREN:
                            lvalue += 1
                            self.eat(LPAREN)
                            node = self.current_syn.value
                            nodeVal.append(node)
                            self.advance()
                            if self.current_syn.type == LPAREN:
                                lvalue += 1;self.eat(LPAREN);rvalue+=1
                                localEnvi[node] = self.scope_eval1()
                            else:
                                localEnvi[node] = self.current_syn
                                self.advance()
                        elif self.current_syn.type == RPAREN:
                            rvalue += 1
                            self.eat(RPAREN)
                if self.current_syn.type == LPAREN:
                    result = self.scope_eval1()
                    return result
            else:
                raise Error(ErrorToken.UNEXPECTED_TOKEN, self.current_syn.value,
                            f"line num : {self.current_syn.line_no}, Col Num : {self.current_syn.col_no}")

        elif token.value == "defun-module":
            self.eat(DEFUN_MODULE)
            libName = self.current_syn.value
            self.eat(SYMBOL)
            libName = importlib.import_module(libName)
            globalEnv[libName.__name__] = libName


        elif token.type == TYPE:
            self.eat(TYPE)
            if self.current_syn.type == SYMBOL:
                node = globalEnv.get(self.current_syn.value)
                if node is None:
                    return self.errorRas("NoneType object")
                return node.type

        elif token.type == MAX:
            self.eat(MAX)
            max_temp = []
            while self.current_syn.type != RPAREN:
                max_temp.append(self.current_syn.value)
                self.advance()
            self.eat(RPAREN)
            return max(max_temp)

        else:
            return self.scope_eval5()

    def scope_eval5(self):
        if self.current_syn.type == LIST or self.current_syn.type == 배열:
            if self.current_syn.type == LIST:
                self.eat(LIST)
            elif self.current_syn.type == 배열:
                self.eat(배열)
            if self.current_syn.type == LPAREN:
                list_name = self.scope_eval1()
                list_value = [];
                self.eat(LPAREN)
                while self.current_syn.type != RPAREN:
                    if self.current_syn.value in globalEnv:
                        pass
                    list_value.append(self.current_syn)
                    self.advance()
                globalEnv[list_name.value] = AtomType_Token(LIST, List(list_name=list_name, size=len(list_value),
                                                                       values=list_value))
            else:
                return None
        elif self.current_syn.type == SIZE:
            if self.current_syn.type == SIZE:
                self.eat(SIZE)
            token = self.current_syn
            self.eat(SYMBOL)
            if globalEnv[token.value]:
                node = globalEnv.get(token.value)
                return Num(node.value.size, INT)
            else:
                raise Error('Can\'t find Any Object! value : {0}, line num : {1}, Col num : {2}'.format(token.value,
                                                                                                        token.line_no,
                                                                                                        token.col_no))

        else:
            return self.scope_eval6()

    # BUILT_IN FUNCTION HERE EVALUATION
    def scope_eval6(self):
        # car function
        if self.current_syn.type == CAR:
            self.eat(CAR)
            if self.current_syn.type == LPAREN:
                node = self.scope_eval1()
                return Num(node.value, INT)
        elif self.current_syn.type == CDR:
            self.eat(CDR)
            temp = AtomType_Token('Nil', 'Nil')
            if self.current_syn.type == LPAREN:
                node = self.scope_eval1()
                return node.value
            else:
                while self.current_syn.type != RPAREN:
                    temp = self.current_syn
                    self.advance()
                    if self.current_syn.type == RPAREN:
                        if temp.type == SYMBOL:
                            temp = globalEnv.get(temp.value)
                if temp is None:
                    return 'Nil'
                return temp.value
        # caar function
        elif self.current_syn.type == CAAR:
            pass
        elif self.current_syn.type == CADR:
            pass
        elif self.current_syn.type == CDAR:
            pass
        elif self.current_syn.type == CDDR:
            pass
        elif self.current_syn.type == SWAP:
            pass
        elif self.current_syn.type == POW:
            self.eat(POW)
            if self.current_syn.type == SYMBOL:
                node = globalEnv.get(self.current_syn.value)
                self.eat(SYMBOL)
                if self.current_syn.type == INT or self.current_syn.type == REAL:
                    node2 = self.current_syn
                    self.advance()
                    return AtomType_Token(REAL, float(node.value ** node2.value))
                elif self.current_syn.type == SYMBOL:
                    node2 = globalEnv.get(self.current_syn.value)
                    self.eat(SYMBOL)
                    return AtomType_Token(REAL, float(node.value ** node2.value))

            elif self.current_syn.type == INT or self.current_syn.type == REAL:
                node = self.current_syn
                self.advance()
                if self.current_syn.type == INT or self.current_syn.type == REAL:
                    node2 = self.current_syn
                    self.advance()
                    return Num(float(node.value ** node2.value), INT)
                elif self.current_syn.type == SYMBOL:
                    node2 = globalEnv.get(self.current_syn.value)
                    self.eat(SYMBOL)
                    return Num(float(node.value ** node2.value), REAL)

        elif self.current_syn.type == ROUND:
            self.eat(ROUND)
            if self.current_syn.type == INT:
                raise Exception("It can't be operate, because argument type is INT type")
            if self.current_syn.type == REAL:
                node = round(self.current_syn.value)
                self.advance()
                self.eat(RPAREN)
                return AtomType_Token(INT, node)
            elif self.current_syn.type == SYMBOL:
                node = globalEnv.get(self.current_syn.value)
                if node is None:
                    raise Exception("It can't be operate, because arguement type is SYMBOL type")
                elif node.type == INT:
                    raise Exception("It can't be operate, because argument type is INT type")
                else:
                    node = round(node.value)
                    globalEnv[self.current_syn.value] = AtomType_Token(INT, node)
                    self.advance()
                    self.eat(RPAREN)
                    return AtomType_Token(INT, node)

        elif self.current_syn.type == SQRT:
            self.eat(SQRT)
            if self.current_syn.type == SYMBOL:
                node = globalEnv.get(self.current_syn.value)
                if node is None:
                    raise Exception("It Can't be Operate")
                else:
                    node = Num(math.sqrt(self.current_syn.value), REAL)
                    while self.current_syn.type != RPAREN:
                        self.advance()
                    self.eat(RPAREN)
                    return node
            else:
                node = Num(math.sqrt(self.current_syn.value), REAL)
                while self.current_syn.type != RPAREN:
                    self.advance()
                self.eat(RPAREN)
                return node

        elif self.current_syn.type == SORT:
            self.eat(SORT)
            if self.current_syn.type == QUOTE:
                self.eat(QUOTE)
                _ = []
                if self.current_syn.type == LPAREN:
                    self.eat(LPAREN)
                    while self.current_syn.type != RPAREN:
                        _.append(self.current_syn.value)
                        self.advance()
                    self.eat(RPAREN)
                    qsort(_)
                    return Quote(_)
                else:
                    return self.errorRas("This Type can't be iterate")
            elif self.current_syn.type == SYMBOL:
                if globalEnv.get(self.current_syn.value):
                    name = self.current_syn.value
                    node = globalEnv.get(self.current_syn.value)
                    self.advance()
                    if node.type == LIST:
                        qsort(node.value.temp)
                        globalEnv[name] = AtomType_Token(LIST, List(list_name=name, size=len(node.value.temp),
                                                                    values=node.value.temp))
                        del name, node
                        self.clean()
                    else:
                        return self.errorRas("This Type is not List Type")
                elif localEnvi.get(self.current_syn.value):
                    pass
                else:
                    return self.errorRas("Wrong Identifier")
            else:
                return self.errorRas("This Type can't iterate")

        elif self.current_syn.type == MAP:
            self.eat(MAP)
            operand = self.setOperand()
            arg = []
            lvalue = 1;rvalue = 0
            if self.current_syn.type == QUOTE:
                result = Quote()
                while lvalue > rvalue:
                    if self.current_syn.type == QUOTE:
                        self.eat(QUOTE)
                        self.eat(LPAREN)
                        lvalue += 1
                        _ = []
                        while self.current_syn.type != RPAREN:
                            _.append(self.current_syn)
                            self.advance()
                        self.eat(RPAREN)
                        rvalue += 1
                        quote = Quote(_)
                        result = quoteOperand(result, quote, operand)
                        del quote
                    elif self.current_syn.type == SYMBOL:
                        pass
                    elif self.current_syn.type == RPAREN:
                        rvalue += 1
                    elif self.current_syn.type == LPAREN:
                        node = self.scope_eval1()
                        result = quoteOperand(result, node, operand)
                        del node
                return result

            elif self.current_syn.type == INT or self.current_syn.type == REAL or \
                    self.current_syn.type == SYMBOL:
                while self.current_syn.type != RPAREN:
                    if self.current_syn.type == SYMBOL:
                        if globalEnv.get(self.current_syn.value):
                            if globalEnv.get(self.current_syn.value).type == QUOTE:
                                arg.append(globalEnv.get(self.current_syn.value))
                                self.eat(SYMBOL)
                            else:
                                arg.append(globalEnv.get(self.current_syn.value))
                                self.eat(SYMBOL)
                        elif localEnvi.get(self.current_syn.value):
                            arg.append(globalEnv.get(self.current_syn.value))
                            self.eat(SYMBOL)
                    elif self.current_syn.type == INT or self.current_syn.type == REAL:
                        arg.append(self.current_syn)
                        self.advance()
                self.eat(RPAREN)
                if operand.type == LAMBDA:
                    if operand.setVal(arg) == -1:
                        return self.errorRas("Argument Number is not match with this lambda expression")
                    node = function_new_eval_table(operand.function_body)
                    return node

                elif arg[0].type == QUOTE:
                    result = Quote()
                    result = quoteOperand(result, arg, operand)
                    return result

        elif self.current_syn.type == APPLY:
            self.eat(APPLY)
            operand = []
            while self.current_syn.type != QUOTE:
                operand.append(self.current_syn)
                self.advance()
            if self.current_syn.type == QUOTE:
                self.eat(QUOTE)
                self.eat(LPAREN)
                _ = []
                while self.current_syn.type != RPAREN:
                    _.append(self.current_syn)
                    self.advance()
                self.clean()
                result = function_new_eval_table(operand + _)
                del operand, _
                return result

            elif self.current_syn.type == SYMBOL:
                pass

        elif self.current_syn.type == KEEP_MATCHING_ITEMS:
            self.eat(KEEP_MATCHING_ITEMS)
            _ = []
            if self.current_syn.__class__.__name__ == 'Quote':
                node = self.current_syn;operand = None
                self.advance()
                if self.current_syn.type == LPAREN:
                    operand = self.scope_eval1()
                elif self.current_syn.type == SYMBOL:
                    operand = self.current_syn
                    self.eat(SYMBOL)
                else:
                    operand = self.current_syn
                    self.advance()
                result = Quote(filtering(node.args, operand))
                del node, operand
                self.clean()
                return result
            elif self.current_syn.type == QUOTE:
                self.eat(QUOTE)
                if self.current_syn.type ==  LPAREN: self.eat(LPAREN)
                while self.current_syn.type != RPAREN:
                    _.append(self.current_syn)
                    self.advance()
                self.eat(RPAREN)
            elif self.current_syn.type == SYMBOL:
                if globalEnv.get(self.current_syn.value):
                    node = globalEnv.get(self.current_syn.value)
                    self.eat(SYMBOL)
                elif localEnvi.get(self.current_syn.value):
                    node = globalEnv.get(self.current_syn.value)
                    self.eat(SYMBOL)
            operand = self.current_syn
            self.advance()
            if len(_) != 0:
                result = Quote(filtering(_, operand))
                del _, operand
                self.clean()
                return result
            else:
                result = Quote(filter(node.arg, operand))
                del node, operand
                self.eat(RPAREN)
                return result

        elif self.current_syn.type == DELETE_MATCHING_ITEMS:
            self.eat(DELETE_MATCHING_ITEMS)
            if self.current_syn.type == QUOTE:
                self.eat(QUOTE)
                self.eat(LPAREN)
                _ = []
                while self.current_syn.type != RPAREN:
                    _.append(self.current_syn)
                    self.advance()
                self.eat(RPAREN)
                operand = self.current_syn
                self.advance()
                result = Quote(filtering(_, operand))
                del _, operand
                self.eat(RPAREN)
                return result

        else:
            return self.scope_eval7()

    def scope_eval7(self):
        if self.current_syn.type == PRINT:
            self.eat(PRINT)
            bufferIo = []
            while self.current_syn.type != RPAREN:
                if self.current_syn.type == SENTENCE:
                    bufferIo.append(self.current_syn.value)
                    self.eat(SENTENCE)
                elif self.current_syn.type == SYMBOL:
                    if globalEnv.get(self.current_syn.value):
                        node = globalEnv.get(self.current_syn.value)
                        if node.type == LIST:
                            self.eat(SYMBOL)
                            bufferIo.append(node.value)
                        elif node.type == QUOTE:
                            self.advance()
                            bufferIo.append(node)
                        elif node.type == VAR:
                            self.advance()
                            bufferIo.append(node.value)
                    elif localEnvi.get(self.current_syn.value):
                        pass
                    else:
                        return self.errorRas(f"Name {self.current_syn.value} is not defined")
                elif self.current_syn.type == LPAREN:
                    bufferIo.append(self.scope_eval1().value)
                    self.eat(RPAREN)
                elif self.current_syn.type == EOF:
                    break
            self.clean()
            stdOut = Print(bufferIo)
            stdOut.standardOut()
            return

        elif self.current_syn.type == INPUT:
            self.eat(INPUT)
            var = self.current_syn.value
            self.advance()
            globalEnv[var] = Var(setTheTypeClass(_input()), VAR)

        else:
            return self.scope_eval8()

    def scope_eval8(self):
        if self.current_syn.type == SHARP_PY:
            self.eat(SHARP_PY)

            if self.current_syn.type != LPAREN:
                return eval(self.current_syn.value)
            else:
                self.eat(LPAREN)
                node = globalEnv.get(self.current_syn.value)
                self.eat(SYMBOL)
                if node:
                    doEval = self.current_syn.value;
                    self.eat(SYMBOL)
                    arg = self.current_syn.value;
                    self.advance()
                    moduleEval = getattr(node, doEval)
                    moduleEval(arg)
                else:
                    print(f"{colorama.Back.RED}{colorama.Fore.BLACK}This Package is not Loaded!")
        else:
            return self.scope_eval9()

    def scope_eval9(self):
        if self.current_syn.type == SETCAR:
            self.eat(SETCAR)
            if self.current_syn.type == LPAREN:
                self.eat(LPAREN)

            else:
                raise self.errorRas("Can't Operate this Expression")
        elif self.current_syn.type == SETCDR:
            pass
        else:
            return self.scope_eval1()

    def function_eval(self, func):
        cal_var = []
        func_copy = []
        if self.current_syn.type == LPAREN:
            self.eat(LPAREN)
            while self.current_syn.type != RPAREN:
                if self.current_syn.type == SYMBOL:
                    node = globalEnv.get(self.current_syn.value)
                    node_name = self.current_syn
                    new_eval = []
                    cnt = 0
                    self.eat(SYMBOL)

                    if node.type == VAR:
                        cal_var.append(node)

                    if node.type == FUNCTION:
                        new_eval.append(AtomType_Token(LPAREN, '('))
                        new_eval.append(node_name)
                        while self.current_syn.type != RPAREN:
                            new_eval.append(self.current_syn)
                            self.advance()
                        self.eat(RPAREN)
                        for rea in new_eval:
                            if rea.type == LPAREN:
                                new_eval.append(AtomType_Token(RPAREN, ')'))
                                cnt += 1
                        node_result = function_new_eval_table(new_eval)
                        cal_var.append(node_result)

                    elif node.type == QUOTE:
                        cal_var.append(node)

                    if node is None:
                        raise Exception("Invaild Argument Error : Check your code")
                    else:
                        if node.type == LIST:
                            self.eat(SQUARE_LPAREN)
                            if self.current_syn.type == INT:
                                find_idx = self.current_syn.value
                                self.eat(INT)
                                self.eat(SQUARE_RPAREN)
                                cal_var.append(node.value.list[find_idx])
                            else:
                                raise Exception("Can't executed this option. Only can Integer value")

                        elif node.type == INT or node.type == REAL:
                            cal_var.append(node)
                            self.advance()

                elif self.current_syn.type == INT:
                    cal_var.append(self.current_syn)
                    self.advance()

                elif self.current_syn.type == REAL:
                    cal_var.append(self.current_syn)
                    self.advance()

                elif self.current_syn.type == PLUS or self.current_syn.type == MINUS or \
                        self.current_syn.type == MUL or self.current_syn.type == DIV:
                    node = self.scope_eval1()
                    cal_var.append(node)

                elif self.current_syn.type == LPAREN:
                    node_value = self.scope_eval1()
                    cal_var.append(node_value)

        # argument evaluation end point #
        argu_map = dict(zip(func.body.arg, cal_var))
        for rea in range(len(func.body.procedure)):
            if func.body.procedure[rea].value in globalEnv.keys():
                node = globalEnv.get(func.body.procedure[rea].value)
                if node.type == LIST:
                    func_copy.append(AtomType_Token(SYMBOL, func.body.procedure[rea].value))
                elif node.type == FUNCTION:
                    func_copy.append(AtomType_Token(SYMBOL, func.body.procedure[rea].value))
                else:
                    func_copy.append(globalEnv.get(func.body.procedure[rea].value))
                self.advance()
            elif func.body.procedure[rea].type == SYMBOL:
                func_copy.append(argu_map.get(func.body.procedure[rea].value))
            else:
                func_copy.append(func.body.procedure[rea])
        while self.current_syn.type is not RPAREN:
            self.advance()
        self.eat(RPAREN)
        arg_result = function_new_eval_table(func_copy)
        return arg_result


def function_new_eval_table(eval_function):
    if eval_function[-1].type != RPAREN:
        eval_function.append(AtomType_Token(RPAREN, ")"))
    eval_function.append(AtomType_Token(EOF, EOF))
    result = Compiler(eval_function)
    value = result.scope_eval1()
    del result
    return value


def setTheTokenTypeClass(node):
    if type(node) is str:
        return
    elif type(node) is int:
        return Num(node.value, INT)
    elif type(node) is float:
        return Num(node.value, REAL)
    else:
        return node


def setTheTypeClass(node):
    try:
        node = int(node)
        return Num(node, INT)
    except ValueError:
        try:
            node = float(node)
            return Num(node, REAL)
        except ValueError:
            node = str(node)
            return

def filtering(node, type):
    if type.type == ISPOSITIVE:
        result = list(filter(lambda x : x.value > 0, node))
        return result
    elif type.type == ISNEGATIVE:
        result = list(filter(lambda x: x.value < 0, node))
        return result

def quoteOperand(result, node, operand):
    if isinstance(node, list):
        if operand.type == PLUS:
            for _ in range(len(node)):
                result += node[_]
        elif operand.type == MINUS:
            for _ in range(len(node)):
                result -= node[_]
        elif operand.type == MUL:
            for _ in range(len(node)):
                result *= node[_]
        elif operand.type == DIV:
            for _ in range(len(node)):
                result /= node[_]
    else:
        if operand.type == PLUS:
            result += node
        elif operand.type == MINUS:
            result -= node
        elif operand.type == MUL:
            result *= node
        elif operand.type == DIV:
            result /= node
    return result
