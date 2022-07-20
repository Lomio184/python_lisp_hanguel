INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', '(', ')', 'EOF'
)
class ParenCounter:
    _scopea  = '\n'
    def __init__(self, ldata = None, rdata = None, depth = 0):
        self.ldata = 0
        self.rdata = 0
        self.depth = depth

class Memory:
    __slots__ = ('stack', 'gc')
    def __init__(self, stack = None, gc = None):
        self.stack = []
        self.gc = []

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos  =0
        self.current_token = self.text[self.pos]

    def error(self):
        raise Exception('Invaild character')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_token = None
        else:
            self.current_token = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_token is not None and self.current_token.isspace():
            self.advance()

    def interger(self):
        result = ''
        while self.current_token is not None and self.current_token.isdigit():
            result += self.current_token
            self.advance()
        return int(result)

    def get_next_token(self):
        while self.current_token is not None:
            if self.current_token.isspace():
                self.skip_whitespace()
                continue

            if self.current_token.isdigit():
                return Token(INTEGER, self.interger())

            if self.current_token == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_token == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_token == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_token == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_token == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_token == ')':
                self.advance()
                return Token(RPAREN, ')')

            self.error()
        return Token(EOF, None)

class AST(object):
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_char = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invaild Syntax')

    def eat(self, token_type):
        if self.current_char.type == token_type:
            self.current_char = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_char
        if token.type == PLUS:
            self.eat(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == MINUS:
            self.eat(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node

    def term(self):
        node = self.factor()
        while self.current_char.type in (MUL, DIV):
            token = self.current_char
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)
            node = BinOp(left = node, op = token , right = self.factor())
        return node

    def expr(self):
        node = self.term()

        while self.current_char.type in (PLUS, MINUS):
            token = self.current_char
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinOp(left=node, op = token, right = self.term())
        return node

    def parse(self):
        return self.expr()

class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

class Interpreter(NodeVisitor):
    def __init__(self, parser):
        super(NodeVisitor, self).__init__()
        self.parser = parser

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == PLUS:
            return +self.visit(node.expr)
        elif op == MINUS:
            return -self.visit(node.expr)

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIV:
            return self.visit(node.left) // self.visit(node.right)

    def visit_Num(self, node):
        return node.value

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)