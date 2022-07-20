from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter


def format(color, style=''):
    _color = QColor()
    _color.setNamedColor(color)

    _format = QTextCharFormat()
    _format.setForeground(_color)

    if 'bold' in style:
        _format.setFontWeight(QFont.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)

    return _format

STYLES = {
    'keyword': format('blue'),
    'operator': format('red'),
    'brace': format('darkGray'),
    'defclass': format('black', 'bold'),
    'string': format('magenta'),
    'string2': format('darkMagenta'),
    'comment': format('darkGreen', 'italic'),
    'self': format('black', 'italic'),
    'numbers': format('brown'),
}

class SyntaxHighlighter(QSyntaxHighlighter):
    # 'caaar', 'caadr', 'cadar', 'caddr',
    # 'cdaar', 'cdadr', 'cddar', 'cdddr',
    #^ not yet
    keywords = [
        'CONS', 'CAR', 'CDR',
        'MAX' , 'MIN', 'ROUND','ABS','ABORT',
        #NOT YET
        'CAAR', 'CADR', 'CDAR', 'CDDR','PYSP','CONST',
        #SOME DO WORK
        'LENGTH', 'DISPLAY', 'DEFINE', 'LET', 'COND', 'IF', 'BEGIN', 'INPUT',
        'LAMBDA', 'AND', 'OR', 'TYPE', 'ADD', 'DEBUG', 'REPORT',
        'define', 'defun', 'pow', '정의', '함수정의']
    '''['set!', 'let*',
        'null?', 'eq?', 'equal?',
        'number?', 'symbol?', 'pair?', 'list?',
    ]'''
    operators = [
        '\+', '-', '\*', '/', 'remainder',
        '=', '<', '>', '<=', '>=',
        '!=', '\%', '\*\*', '+=', '-=',
        '*=', '/=',
    ]

    braces = [
        '\{', '\}', '\(', '\)', '\[', '\]',
    ]

    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)
        self.tri_single = (QRegExp("'''"), 1, STYLES['string2'])
        self.tri_double = (QRegExp('"""'), 2, STYLES['string2'])

        rules = []

        rules += [(r'\b%s\b' % w, 0, STYLES['keyword'])
                  for w in SyntaxHighlighter.keywords]
        rules += [(r'%s' % o, 0, STYLES['operator'])
                  for o in SyntaxHighlighter.operators]
        rules += [(r'%s' % b, 0, STYLES['brace'])
                  for b in SyntaxHighlighter.braces]

        rules += [
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),

            (r'\bdefine\b\s*(\w+)', 1, STYLES['defclass']),

            (r';[^\n]*', 0, STYLES['comment']),

            (r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, STYLES['numbers']),
        ]

        self.rules = [(QRegExp(pat), index, fmt) for (pat, index, fmt) in rules]

    def highlightBlock(self, text):
        for expression, nth, format in self.rules:
            index = expression.indexIn(text, 0)

            while index >= 0:
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        in_multiline = self.match_multiline(text, *self.tri_single)
        if not in_multiline:
            in_multiline = self.match_multiline(text, *self.tri_double)

    def match_multiline(self, text, delimiter, in_state, style):
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        else:
            start = delimiter.indexIn(text)
            add = delimiter.matchedLength()


        while start >= 0:
            end = delimiter.indexIn(text, start + add)
            if end >= add:
                length = end - start + add + delimiter.matchedLength()
                self.setCurrentBlockState(0)
            else:
                self.setCurrentBlockState(in_state)
                length = len(text) - start + add
            self.setFormat(start, length, style)
            start = delimiter.indexIn(text, start + length)
        if self.currentBlockState() == in_state:
            return True
        else:
            return False
