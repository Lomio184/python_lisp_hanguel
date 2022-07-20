import traceback

from PyQt5 import QtWidgets, QtGui, QtCore, Qt
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QKeySequence, QPainter, QColor, QFont, QTextFormat
from PyQt5.QtWidgets import QPlainTextEdit, QAction, QMessageBox, QFileDialog, QTextEdit

from src.backsrc import comp
from src.backsrc.comp import Lexical_Stack, MakeOut
from src.front.syntaxHigh import SyntaxHighlighter
from src.front.textLineNum import LineNumberArea
import asyncio

class NewCodeEditor(QtWidgets.QPlainTextEdit):
    def __init__(self, title = None, prompt = 'PYSP>> ', browser = None):
        QPlainTextEdit.__init__(self)
        self.title = title
        self.prompt = prompt
        self.setWindowTitle('Pysp idle')
        self.settingWindowTitle = 'Settings - PYSP'
        self.print_option = "RESULT >> "
        self.highlight = SyntaxHighlighter(self.document())
        self.setWindowTitle(self.title)
        self.setWordWrapMode(QtGui.QTextOption.WrapAnywhere)
        self.setUndoRedoEnabled(False)
        self.text = []
        self.browser = browser
        self.lineNumberArea = LineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth(0)
        self.setGeometry(150,200,600,800)

        #src menubar
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 22))
        self.menubar.setObjectName("menubar")
        #src menubar end

        #file option
        self.menuFile = self.menubar.addMenu('&File')
        self.menuFile.setObjectName("menuFile")

        self.saveAction = QAction("&Save", self)
        self.saveAction.setShortcut(QKeySequence.Save)
        self.saveAction.triggered.connect(self.fileSave)

        self.loadAction = QAction("&Load", self)
        self.loadAction.setShortcut(QKeySequence.Open)

        self.menuFile.addAction(self.saveAction)
        self.menuFile.addAction(self.loadAction)
        # self.loadAction.triggered.connect(self.fileOpen)
        #file option end

        #file Run option
        self.menuRun = self.menubar.addMenu('&Run')

        self.runAction = QAction("&Run",self)
        self.runAction.setShortcut('F5')
        self.runAction.triggered.connect(self.runCode)

        self.debugAction = QAction("&Debug",self)
        self.debugAction.setShortcut('F6')

        self.menuRun.addAction(self.runAction)
        self.menuRun.addAction(self.runAction)
        # self.debugAction.triggered.connect(self.debugCode)

        self.helpAction = QAction("&Help",self)
        self.helpAction.setShortcut('F10')
        self.helpAction.triggered.connect(self.runHelp)

        self.menuHelp = self.menubar.addMenu('&Help')
        self.menuHelp.addAction(self.helpAction)

        self.fileSaved = True
        self.fileSavedSucceed = 0

    def runCode(self):
        self.fileSave()
        try:
            fp = open(self.filename, 'r')
        except FileNotFoundError:
            messagebox = QMessageBox()
            messagebox.setWindowTitle("Warning")
            messagebox.setText("Can't access the Root Directory!")
            messagebox.show()
            exe = messagebox.exec_()
            return
        codes = fp.read()
        test = Lexical_Stack(codes)
        test.tokenize()
        make = MakeOut(test.stack)
        make.out()
        rea = make.result
        for reb in range(len(rea)):
            self.browser.append(self.print_option + str(rea[reb]))

    def setTitle(self):
        self.setWindowTitle('[' + self.filename + '] - PYSP')

    def runHelp(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText('Dev : Hazard@dev\n'
                    'Day : 2020/10/22\n'
                    'Designed by Hazard @ Thanks to Python:)\n')
        msg.setWindowTitle('HELP @ Info')
        msg.setStandardButtons(QMessageBox.Yes)
        msg.exec_()

    def fileAskSave(self):
        if not self.fileSaved:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText('Save changes to " ' + self.filename + '"?')
            msg.setWindowTitle('Confile')
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            i = msg.exec_()

            if i == QMessageBox.Cancel:
                self.fileSavedSucceed = -1
            elif i == QMessageBox.No:
                self.fileSavedSucceed = 0
            elif i == QMessageBox.Yes:
                tmp = self.fileSave()
                self.fileSavedSucceed = tmp

        else:
            self.fileSavedSucceed = 0

    def fileSetSaved(self, stat=False):
        if stat != self.fileSaved:
            self.fileSaved = stat

    def fileSave(self):
        if self.windowTitle() == self.settingWindowTitle:
            file = open(self.filename, 'w')
            file.write(self.toPlainText())
            file.close()
            self.fileSetSaved(True)
            return 0

        if self.windowTitle() == '*Untitled':
            fd = QFileDialog(self)
            self.filename = fd.getSaveFileName(self, 'Save File', '/Untitled',
                    'Scheme sourse (*.scp);;Racket source (*.rkt);;lisp source(*.lisp);;text (*.txt)')
            self.filename = self.filename[0]
            if self.filename == '':
                self.filename = '*Untitled'
                return -1

        try:
            file = open(self.filename , 'w')
            file.write(self.toPlainText())
            file.close()
            self.fileSetSaved(True)
            if self.windowTitle() != self.settingWindowTitle:
                self.setTitle()
            return 0
        except OSError:
            traceback_lines = traceback.format_exc().split('\n')
            for i in (3, 2, 1, -1):
                traceback_lines.pop(i)
            print(traceback_lines)
        except:
            asyncio.sleep(1)
            print('Error')

    def lineNumberAreaWidth(self):
        digits = 1
        count = max(1, self.blockCount())
        while count >= 10:
            count /= 10
            digits += 1
        space = 12 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(),
                                       rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor(228, 228, 228))

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                painter.setPen(QColor(6))  # Qt.black)
                painter.setFont(QFont('Courier New', 12))
                painter.drawText(0, top, self.lineNumberArea.width(), height,
                                 QtCore.Qt.AlignCenter, number)  # Right, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    def resizeEvent(self, event):
        super().resizeEvent(event)

        cr = self.contentsRect();
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(),
                                              self.lineNumberAreaWidth(), cr.height()))

    def highlightCurrentLine(self):
        extraSelections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()

            lineColor = QColor('yellow').lighter(160)

            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)
