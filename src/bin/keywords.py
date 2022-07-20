import sys;import os

from src.backsrc.object.type import AtomType_Token

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


LPAREN = '('
RPAREN = ')';NEXT_LINE = '\n'
MAIN = 'MAIN';NAME = 'NAME'


RESERVED_KEYWORDS = {
    '\''            : AtomType_Token("QUOTE", "\'"),
    'DOUBLE_QUOTE'  : AtomType_Token('DOUBLE_QUOTE', 'double_quote'),
    'print'         : AtomType_Token('PRINT', 'print'),
    'defun'         : AtomType_Token('DEFUN', 'defun'),
    'defun-module'  : AtomType_Token("DEFUN_MODULE", "defun-module"),
    '#py'           : AtomType_Token("SHARP_PY", "#py"),
    'FUNCTION'      : AtomType_Token('FUNCTION', 'FUNCTION'),
    'NAME'          : AtomType_Token('NAME', 'name'),
    'MAIN'          : AtomType_Token('MAIN', 'main'),

    'Int'           : AtomType_Token('INT', 'Int'),
    'Real'          : AtomType_Token('REAL', 'Real'),
    'Symbol'        : AtomType_Token('SYMBOL', 'Symbol'),
    'const'         : AtomType_Token('CONST', 'const'),

    'list'          : AtomType_Token('LIST', 'list'),
    'size'          : AtomType_Token('SIZE', 'size'),

    'LPAREN'        : AtomType_Token('LPAREN', 'lparen'),
    'RPAREN'        : AtomType_Token('RPAREN', 'rparen'),
    'SQUARE_LPAREN' : AtomType_Token('SQUARE_LPAREN','square_lparen'),
    'SQUARE_RPAREN' : AtomType_Token('SQUARE_RPAREN','square_rparen'),

    'nil'           : AtomType_Token('NIL', 'nil'),
    'Id'            : AtomType_Token('ID', 'id'),
    'var'           : AtomType_Token('VAR', 'Var'),
    'min'           : AtomType_Token('MIN', 'min'),

    'max'           : AtomType_Token('MAX', 'max'),
    'abs'           : AtomType_Token('ABS', 'abs'),
    'round'         : AtomType_Token('ROUND', 'round'),
    'length'        : AtomType_Token('LENGTH', 'length'),
    'sqrt'          : AtomType_Token('SQRT', 'sqrt'),

    'define'        : AtomType_Token('DEFINE', 'define'),
    'set!'          : AtomType_Token("SET!", "set!"),
    'let'           : AtomType_Token("LET", 'let'),
    'if'            : AtomType_Token('IF', 'if'),
    'lambda'        : AtomType_Token('LAMBDA', 'lambda'),
    'cons'          : AtomType_Token('CONS', 'cons'),
    'type'          : AtomType_Token('TYPE', 'type'),
    'quote'         : AtomType_Token('QUOTE', 'quote'),
    'car'           : AtomType_Token('CAR', 'car'),
    'cdr'           : AtomType_Token('CDR', 'cdr'),
    'input'         : AtomType_Token("INPUT", 'input'),

    '#t'            : AtomType_Token('TRUE', '#t'),
    '#f'            : AtomType_Token('FALSE', '#f') ,
    'eq?'           : AtomType_Token('ISEQUAL', 'eq?'),
    'integer?'      : AtomType_Token('ISINTEGER', 'integer?'),
    'real?'         : AtomType_Token("ISREAL", 'real?'),
    'number?'       : AtomType_Token("ISNUM", 'number?'),
    'symbol?'       : AtomType_Token('ISSYMBOL', 'symbol?'),
    'null?'         : AtomType_Token("ISNULL", 'null?'),
    'list?'         : AtomType_Token('ISLIST', 'list?'),
    'sentence?'     : AtomType_Token("ISSENTENCE", 'sentence?'),
    'zero?'         : AtomType_Token("ISZERO", 'zero?'),
    'positive?'     : AtomType_Token("ISPOSITIVE", 'positive?'),
    'negative?'     : AtomType_Token("ISNEGATIVE", 'negative?'),
    'sort'          : AtomType_Token("SORT", 'sort'),

    'set'           : AtomType_Token('SET', 'set'),
    'debug'         : AtomType_Token('DEBUG', 'debug'),
    'report'        : AtomType_Token('REPORT','report'),

    'caar'          : AtomType_Token('CAAR','caar'),
    'cadr'          : AtomType_Token('CADR','cadr'),
    'cdar'          : AtomType_Token('CDAR','cdar'),
    'cddr'          : AtomType_Token('CDDR','cddr'),
    'swap'          : AtomType_Token('SWAP', 'swap'),
    'pow'           : AtomType_Token('POW', 'pow'),
    'sort'          : AtomType_Token('SORT', 'sort'),
    'map'           : AtomType_Token("MAP", 'map'),
    'apply'         : AtomType_Token("APPLY", 'apply'),
    'keep-matching-items'   : AtomType_Token("KEEP_MATCHING_ITEMS", 'keep-matching-items'),
    'delete-matching-items' : AtomType_Token("DELETE_MATCHING_ITEMS", 'delete-matching-items'),

    'let'           : AtomType_Token('LET','let'),
    'display'       : AtomType_Token('DISPLAY', 'display'),
    'input'         : AtomType_Token('INPUT', 'input'),

    'set-car!'      : AtomType_Token('SETCAR', 'set-car!'),
    'set-cdr!'      : AtomType_Token('SETCDR', 'set-cdr!'),

    'IMUL'          : AtomType_Token('IMUL', '*='),
    'IDIV'          : AtomType_Token('IDIV', '/='),
    'IPLUS'         : AtomType_Token('IPLUS', '+='),
    'IMIN'          : AtomType_Token('IMIN', '-='),

    'GREAT'         : AtomType_Token('GREAT', '>'),
    'LESS'          : AtomType_Token('LESS', '<'),
    'COLON'         : AtomType_Token('COLON', ':'),
    'GREAT_EQUAL'   : AtomType_Token('GREAT_EQUAL', '>='),
    'LESS_EQUAL'    : AtomType_Token('LESS_EQUAL', '<='),
    'EQUAL'         : AtomType_Token('EQUAL', '=='),
    'EOF'           : AtomType_Token('EOF', 'EOF'),

    'abort'         : AtomType_Token('ABORT', 'abort'),
    '함수정의'         : AtomType_Token('함수정의', '함수정의'),
    '만약'            : AtomType_Token('만약', '만약'),
    '정수'            : AtomType_Token('정수', '정수'),
    '실수'            : AtomType_Token('실수', '실수'),
    '정의'            : AtomType_Token('정의', '정의'),
    '배열'            : AtomType_Token('배열', '배열'),
    '변수'            : AtomType_Token('변수', '변수'),
}

