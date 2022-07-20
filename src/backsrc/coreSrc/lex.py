from src.backsrc.coreSrc.parenChecker import ParenCounter
from src.backsrc.error.error import Error, ErrorToken
from src.backsrc.object.type import Unary_Operand_AtomType_Token, AtomType_Token
from src.bin import keywords
from src.bin.ADT import _Compiler
from src.bin.keywords import RESERVED_KEYWORDS
from src.mainToken import *

class Lexical_Stack(_Compiler):
    def __init__(self, text):
        self.text = text
        self.p = ParenCounter()
        self.reaCount = 0
        self.stack = []
        self.current_token = self.text[self.reaCount]
        self.lineNum = 1
        self.ColNum = 1

    def stack_error(self):
        raise Error(1, ErrorToken.STACK_ERROR)

    def errorRas(self, errMsg):
        raise Error('{0} : {1}, LineNum : {2}, ColNum : {3}'.format(
            errMsg,
            self.text[self.reaCount - 1] if self.current_token is None else self.current_token,
            self.lineNum,
            self.ColNum
        ))

    def advance(self):
        self.reaCount += 1
        if self.reaCount > len(self.text) - 1:
            self.current_token = None
        else:
            self.current_token = self.text[self.reaCount];self.ColNum += 1

    def del_space(self):
        while self.current_token is not None and self.current_token.isspace():
            self.advance()

    def _id(self):
        result, token = '', ''

        while self.current_token is not None and self.current_token.isalnum() or self.current_token == '-' \
                or self.current_token == "?" or self.current_token == "!":
            result += self.current_token
            self.advance()
            try:
                token = RESERVED_KEYWORDS.get(result)
            except Exception as e:
                print(e)
                exit(1)
        if token is None:
            token = AtomType_Token(SYMBOL, str(result), line_no=self.lineNum, col_no=self.ColNum)
            return token

        else:
            token.line_no = self.lineNum
            token.col_no = self.ColNum
            return token

    def make_int(self):
        result = ''
        while self.current_token is not None and self.current_token.isdigit():
            result += self.current_token
            self.advance()
        if self.current_token == '.':
            result += self.current_token
            self.advance()

            while self.current_token is not None and self.current_token.isdigit():
                result += self.current_token
                self.advance()
            token = AtomType_Token(REAL, float(result), line_no=self.lineNum, col_no=self.ColNum)
        else:
            token = AtomType_Token(INT, int(result), line_no=self.lineNum, col_no=self.ColNum)
        return token

    def unary_make_int(self):
        result = ''
        while self.current_token is not None and self.current_token.isdigit():
            result += self.current_token
            self.advance()
        if self.current_token == '.':
            result += self.current_token
            self.advance()

            while self.current_token is not None and self.current_token.isdigit():
                result += self.current_token
                self.advance()
            token = Unary_Operand_AtomType_Token(REAL, -float(result), line_no=self.lineNum, col_no=self.ColNum)
        else:
            token = Unary_Operand_AtomType_Token(INT, -int(result), line_no=self.lineNum, col_no=self.ColNum)
        return token

    def tokenize(self):
        if self.current_token != "(": raise Error("Please check your code", self.current_token)
        while self.current_token is not None:
            if self.current_token.isspace():
                self.del_space()
                continue

            if self.current_token.isalpha():
                token = self._id()
                self.p.tokens.append(token)

            if self.current_token.isdigit():
                token = self.make_int()
                self.p.tokens.append(token)

            if self.current_token == '\'':
                result = self.current_token
                self.advance()
                result = RESERVED_KEYWORDS.get(result)
                result.line_no = self.lineNum
                result.col_no = self.ColNum
                self.p.tokens.append(result)

            if self.current_token == "#":
                result = self.current_token
                self.advance()
                while self.current_token is not None and self.current_token.isalnum():
                    result += self.current_token
                    self.advance()
                try:
                    token = RESERVED_KEYWORDS.get(result)
                except Exception as e:
                    print("Unsupported Token {token}".format(result))
                    exit(-1)
                token.line_no = self.lineNum
                token.col_no = self.ColNum
                self.p.tokens.append(token)

            if self.current_token == '"':
                self.advance();sentence = ""
                while self.current_token is not '"':
                    sentence += self.current_token
                    self.advance()
                if self.current_token != '"':
                    raise Exception("Double quote must pair, Check Your Code")
                else:
                    self.advance()
                    self.p.tokens.append(AtomType_Token(SENTENCE, sentence, line_no=self.lineNum, col_no=self.ColNum))

            if self.current_token == '=':
                self.advance()
                if self.current_token == '=':
                    self.p.tokens.append(AtomType_Token(EQUAL, '==', line_no=self.lineNum, col_no=self.ColNum))
                    self.advance()
                else:
                    node = self.current_token
                    self.advance()
                    raise Error(ErrorToken.UNEXPECTED_TOKEN, node, "Can't Operate this token")

            if self.current_token == '>':
                self.advance()
                if self.current_token == '=':
                    self.p.tokens.append(AtomType_Token(GREAT_EQUAL, '>=', line_no=self.lineNum, col_no=self.ColNum))
                    self.advance()
                else:
                    self.p.tokens.append(AtomType_Token(GREAT, '>', line_no=self.lineNum, col_no=self.ColNum))

            if self.current_token == '<':
                self.advance()
                if self.current_token == '=':
                    self.p.tokens.append(AtomType_Token(LESS_EQUAL, '<=', line_no=self.lineNum, col_no=self.ColNum))
                    self.advance()
                else:
                    self.p.tokens.append(AtomType_Token(LESS, '<', line_no=self.lineNum, col_no=self.ColNum))

            if self.current_token == '+':
                self.advance()
                if self.current_token == '=':
                    self.p.tokens.append(AtomType_Token(IPLUS, '+=', line_no=self.lineNum, col_no=self.ColNum))
                    self.advance()
                else:
                    self.p.tokens.append(AtomType_Token(PLUS, '+', line_no=self.lineNum, col_no=self.ColNum))
                    self.advance()

            if self.current_token == '*':
                self.p.tokens.append(AtomType_Token("MUL", '*', line_no=self.lineNum, col_no=self.ColNum))
                self.advance()

            if self.current_token == '-':
                self.advance()
                self.p.tokens.append(AtomType_Token("MINUS", '-', line_no=self.lineNum, col_no=self.ColNum))
                if self.current_token.isdigit():
                    self.p.tokens.pop()
                    token = self.unary_make_int()
                    self.p.tokens.append(token)

            if self.current_token == '/':
                self.p.tokens.append(AtomType_Token("DIV", '/', line_no=self.lineNum, col_no=self.ColNum))
                self.advance()

            if self.current_token == keywords.LPAREN:
                self.p.ldata += 1
                self.p.tokens.append(AtomType_Token('LPAREN', keywords.LPAREN, line_no=self.lineNum, col_no=self.ColNum))
                self.advance()

            if self.current_token == keywords.RPAREN:
                self.p.rdata += 1
                self.p.tokens.append(AtomType_Token('RPAREN', keywords.RPAREN, line_no=self.lineNum, col_no=self.ColNum))
                if self.p.rdata > self.p.ldata:
                    return self.errorRas("Parentheses Error Occur, Check your parentheses")
                elif self.check():
                    self.stack.append(self.p)
                    self.p = ParenCounter(depth=self.p.depth)
                    self.p.depth += 1
                    self.ColNum = 1
                self.advance()
                if self.current_token is None:
                    if self.check():
                        self.stack.append(self.p)
                        self.p = ParenCounter(depth = self.p.depth)
                        self.p.depth += 1
                        self.lineNum += 1
                    else:
                        return self.errorRas("Parentheses Error Occur, Check your parentheses")

            if self.current_token == '[':
                self.p.tokens.append(AtomType_Token(SQUARE_LPAREN, '[', line_no=self.lineNum, col_no=self.ColNum))
                self.advance()

            if self.current_token == ']':
                self.p.tokens.append(AtomType_Token(SQUARE_RPAREN, ']', line_no=self.lineNum, col_no=self.ColNum))
                self.advance()

            if self.current_token == ':':
                self.p.tokens.append(AtomType_Token(COLON, ':', line_no=self.lineNum, col_no=self.ColNum))
                self.advance()

            if self.current_token == keywords.NEXT_LINE:
                self.lineNum += 1
                self.advance()
        self.stack.append(self.p)

    def check(self):
        return self.p.ldata == self.p.rdata