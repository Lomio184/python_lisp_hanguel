import os
import sys
import time
import traceback

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QIcon, QFont, QKeySequence
from PyQt5.QtWidgets import QTextBrowser, QGridLayout, QWidget, QAction, QMessageBox, QFileDialog, QInputDialog
import idna

from src.backsrc.coreSrc.lex import Lexical_Stack
from src.backsrc.coreSrc.makeOut import MakeOut
from src.backsrc.interpret import Lexer, Parser, SemanticAnalyzer, make_stack, interpret, visit_Atom, standard_env, \
    print_expr, DEBUG
from src.front.mainCodeEditor import CodeEditor
from src.front.newEditWindow import NewCodeEditor


class Console(QtWidgets.QMainWindow):
    def __init__(self):
        self.welcome_message = '''
         -------------------------------------------------------
             Welcome to a primitive PYSP interpreter.
                             {time}
                 PYSP INTERPRETER VER## 0.0.1
         -------------------------------------------------------
        '''.format(time=time.ctime())
        super().__init__()
        self.history = []
        self.namespace = {}
        self.construct = []
        self.setWindowIcon(QIcon("Assets/ICON.png"))

        # Window Layout
        self.setWindowTitle('Pysp idle')
        self.settingWindowTitle = 'Settings - PYSP'
        self.setGeometry(150, 200, 600, 800)

        self.editor = CodeEditor()
        self.editor.setFont(QFont('Consolas', 15))
        self.editor.setWordWrapMode(QtGui.QTextOption.WrapAnywhere)
        self.editor.setUndoRedoEnabled(False)
        self.newPrompt()

        self.text_res = QTextBrowser()
        self.text_res.setFont(QFont('Courier New', 13))
        self.text_res.append(self.welcome_message)

        self.layout = QGridLayout()
        self.layout.addWidget(self.editor, 0, 0, 5, 1)
        self.layout.addWidget(self.text_res, 5, 0, 3, 1)

        self.c_widget = QWidget()
        self.c_widget.setLayout(self.layout)
        self.setCentralWidget(self.c_widget)

        self.filename = '*Untitled'
        self.settings = ''
        self.fileSaved = True
        self.fileSavedSucceed = 0
        self.txtClearRun = False
        self.DebugFileOpen = True
        self.DebugRunSource = True
        self.DebugSettings = True
        self.settingFileName = './data/settings.scp'

        self.editor.textChanged.connect(self.fileSetSaved)
        self.settingInitialize()

        self.debug_stack = DEBUG

        self.statusBar()
        mainMenu = self.menuBar()

        fileMenu = mainMenu.addMenu('&File')

        newAction = QAction('&New', self)
        newAction.setShortcut(QKeySequence.New)
        newAction.triggered.connect(self.fileNew)

        saveAction = QAction('&Save', self)
        saveAction.setShortcut(QKeySequence.Save)
        saveAction.triggered.connect(self.fileSave)

        openAction = QAction('&Open', self)
        openAction.setShortcut(QKeySequence.Open)
        openAction.triggered.connect(self.fileOpen)

        fileMenu.addAction(newAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(openAction)

        editMenu = mainMenu.addMenu('&Edit')

        undoAction = QAction('&Undo', self)
        undoAction.setShortcut(QKeySequence.Undo)
        undoAction.triggered.connect(self.editor.undo)

        redoAction = QAction('&Redo', self)
        redoAction.setShortcut(QKeySequence.Redo)
        redoAction.triggered.connect(self.editor.redo)

        cutAction = QAction('Cu&t', self)
        cutAction.setShortcut(QKeySequence.Cut)
        cutAction.triggered.connect(self.editor.cut)

        copyAction = QAction('&Copy', self)
        copyAction.setShortcut(QKeySequence.Copy)
        copyAction.triggered.connect(self.editor.copy)

        pasteAction = QAction('&Paste', self)
        pasteAction.setShortcut(QKeySequence.Paste)
        pasteAction.triggered.connect(self.editor.paste)

        selectAllAction = QAction('Se&lect All', self)
        selectAllAction.setShortcut(QKeySequence.SelectAll)
        selectAllAction.triggered.connect(self.editor.selectAll)

        settingAction = QAction('&Settings', self)
        settingAction.setShortcut('Ctrl+Alt+S')
        settingAction.triggered.connect(self.settingsEdit)

        settingDefaultAction = QAction('&Default Settings', self)
        settingDefaultAction.setShortcut('Ctrl+Alt+D')
        settingDefaultAction.triggered.connect(self.settingsDefault)

        editMenu.addAction(undoAction)
        editMenu.addAction(redoAction)
        editMenu.addSeparator()
        editMenu.addAction(cutAction)
        editMenu.addAction(copyAction)
        editMenu.addAction(pasteAction)
        editMenu.addSeparator()
        editMenu.addAction(selectAllAction)
        editMenu.addSeparator()
        editMenu.addAction(settingAction)
        editMenu.addAction(settingDefaultAction)

        runMenu = mainMenu.addMenu('&Run')

        runAction = QAction('&Run', self)
        runAction.setShortcut('F5')
        runAction.triggered.connect(self.runCode)

        helpMenu = mainMenu.addMenu('&Help')

        helpAction = QAction('&Help', self)
        helpAction.triggered.connect(self.runHelp)

        runMenu.addAction(runAction)
        helpMenu.addAction(helpAction)

    def interpret_text_res(self, filename = None):
        print("==========START : {}==========".format(filename))


    def runHelp(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText('Dev : Hazard@dev\n'
                    'Day : 2020/08/00\n'
                    'Help by python:)\n')
        msg.setWindowTitle('HELP @ Info')
        msg.setStandardButtons(QMessageBox.Yes)
        msg.exec_()

    def setTitle(self):
        self.setWindowTitle('[' + self.filename + '] - PYSP')

    def print_debug_info(self, c, str):
        if c == 'F' and self.DebugFileOpen:
            self.text_res.append('<font color="#6600cc"><b>[F] </b></font>' + str)
        elif c == 'R' and self.DebugRunSource:
            self.text_res.append('<font color="#6600cc"><b>[R] </b></font>' + str)
        elif c == 'S' and self.DebugSettings:
            self.text_res.append('<font color="#6600cc"><b>[S] </b></font>' + str)

    def fileSetSaved(self, stat=False):
        if stat != self.fileSaved:
            self.print_debug_info('F', '<i>saved: ' + str(self.fileSaved) + ' -> ' + str(stat) + '</i>')
            self.fileSaved = stat

    def fileAskSave(self):
        self.print_debug_info('F',
                              '&nbsp;&nbsp;<font color="blue">fileAskSave:</font> fileSaved = ' + str(self.fileSaved))
        if not self.fileSaved:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText('Save changes to "' + self.filename + '"?')
            msg.setWindowTitle('Confirm')
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            i = msg.exec_()

            if i == QMessageBox.Cancel:
                self.fileSavedSucceed = -1
            elif i == QMessageBox.No:
                self.fileSavedSucceed = 0
            elif i == QMessageBox.Yes:
                tmp = self.fileSave()
                self.fileSavedSucceed = tmp
            self.print_debug_info('F', '&nbsp;&nbsp;MsgBoxRes = ' + str(self.fileSavedSucceed))
        else:
            self.fileSavedSucceed = 0

    def fileNew(self):
        self.print_debug_info('F', '<font color="red"><b>FileNew</b></font>')
        self.print_debug_info('F', '&nbsp;&nbsp;FileSavedSucceed = ' + str(self.fileSavedSucceed))
        self.fileAskSave()
        self.print_debug_info('F', '&nbsp;&nbsp;FileSavedSucceed = ' + str(self.fileSavedSucceed))
        if self.fileSavedSucceed == -1:
            self.print_debug_info('F', '&nbsp;&nbsp;FileSavedSucceed = not allowed')
            return
        elif self.fileSavedSucceed == 0:
            self.filename = '*Untitled'
            console = NewCodeEditor(title = '*Untitled', browser = self.text_res)
            console.show()
            self.fileSetSaved(True)
            self.setTitle()

    def fileSave(self):
        self.print_debug_info('F', '<font color="red"><b>FileSave</b></font>')
        if self.windowTitle() == self.settingWindowTitle:
            file = open(self.filename, 'w')
            file.write(self.editor.toPlainText())
            file.close()
            self.fileSetSaved(True)
            return 0

        if self.filename == '*Untitled':
            fd = QFileDialog(self)
            self.filename = fd.getSaveFileName(self, 'Save File', '/Untitled',
                                               'Scheme sourse (*.scp);;Racket source (*.rkt);;lisp source(*.lisp);;text (*.txt)')
            self.print_debug_info('F', '&nbsp;&nbsp;filename = ' + str(self.filename))
            self.filename = self.filename[0]
            if self.filename == '':
                self.filename = '*Untitled'
                return -1

        try:
            file = open(self.filename, 'w')
            file.write(self.editor.toPlainText())
            file.close()
            self.fileSetSaved(True)
            if self.windowTitle() != self.settingWindowTitle:
                self.setTitle()
            return 0
        except OSError:
            self.print_debug_info('R',
                                  '<font color = "pink"><b> RunCode </b></font> <br> <b>RETURN :</b> ' + 'nil')
            traceback_lines = traceback.format_exc().split('\n')
            for i in (3, 2, 1, -1):
                traceback_lines.pop(i)
            self.print_debug_info('R',
                                  '<font color = "pink"><b> RunCode </b></font> <br> <b>INPUT CODE:</b> ' + '#TypeError check this code ' + '\n'.join(
                                      traceback_lines))
            self.debug_stack.clearHelper()

    def fileOpen(self):  # Open File
        self.print_debug_info('F', '<font color="red"><b>FileOpen</b></font>')
        self.fileAskSave()
        if self.fileSavedSucceed == -1:
            return
        elif self.fileSavedSucceed == 0:
            fd = QFileDialog(self)
            self.filename = fd.getOpenFileName(self, 'Open File', '', 'Scheme source (*.scp *.rkt *.txt)')
            self.print_debug_info('F', '&nbsp;&nbsp;filename = ' + str(self.filename))
            self.filename = self.filename[0]
            from os.path import isfile
            if isfile(self.filename):
                text = open(self.filename).read()
                self.print_debug_info('F', '  text = ' + str(text))
                self.editor.setPlainText(text)
                self.fileSetSaved(True)
                self.setTitle()
            else:
                self.filename = '*Untitled'
                self.editor.setPlainText('; Something Wrong in the Document')
                self.setTitle()

    def settingInitialize(self):
        from os.path import isfile
        self.print_debug_info('R', '<b> You must keep the scheme rule </b>')
        filepath = r'\Program Files\PYSP\data\ '
        filename = self.settingFileName  # r'\Program Files\PYSP\data\settings.scp'
        # if not os.path.exists(filepath):
        #     os.makedirs(filepath)
        # print(isfile(filename))
        if isfile(filename):
            text = open(filename).read()
            self.settings = text
            self.setSettings()
        else:
            # print('fuck it')
            return

    def settingsEdit(self):
        if self.windowTitle() == self.settingWindowTitle:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText('You are in setting editor now!')
            msg.setWindowTitle('Error')
            i = msg.exec_()
            return
        self.fileAskSave()
        if self.fileSavedSucceed == -1:
            return
        elif self.fileSavedSucceed == 0:
            import os
            from os.path import isfile
            filepath = r'\Program Files\PYSP\data\ '
            # self.filename = r'\Program Files\PYSP\data\settings.scp'
            self.filename = self.settingFileName
            if not os.path.exists(filepath):
                os.makedirs(filepath)
            self.setWindowTitle(self.settingWindowTitle)
            if isfile(self.filename):
                text = open(self.filename).read()
                self.editor.setPlainText(text)
                self.fileSetSaved(True)
            else:
                self.print_debug_info('S', 'cannot open the settings file')
                self.settingsDefault(1)

    def settingsDefault(self, index=0):
        if self.windowTitle() != self.settingWindowTitle and index == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText('You can only use this in Settings Editor.')
            msg.setWindowTitle('Error')
            i = msg.exec_()
            return
        self.settings = '''; settings
(define df (open debug_file))   
(define dc (open debug_code))   
(define ds (open debug_set))    
(define rc (open run_clear))   
(define fs (lambda (x) (set_font_size x)))
(define ff (lambda (str) (set_font str)))   
        '''
        self.editor.setPlainText(self.settings)
        self.fileSetSaved(False)



    def updateNamespace(self, namespace):
        self.namespace.update(namespace)

    def showMessage(self, message = None):
        self.editor.appendPlainText(message)
        self.newPrompt()

    def newPrompt(self):
        if self.construct:
            prompt = '.' * len(self.editor.prompt)

        else:
            prompt = self.editor.prompt
        self.editor.appendPlainText(prompt)
        self.editor.moveCursor(QtGui.QTextCursor.End)


    def getCommand(self):
        doc = self.editor.document()
        curr_line = doc.findBlockByLineNumber(doc.lineCount() - 1).text()
        curr_line = curr_line.rstrip()
        curr_line = curr_line[len(self.editor.prompt):]
        return curr_line

    def setCommand(self, command):
        if self.editor.getCommand() == command:
            return
        self.editor.moveCursor(QtGui.QTextCursor.End)
        self.editor.moveCursor(QtGui.QTextCursor.StartOfLine, QtGui.QTextCursor.KeepAnchor)
        for i in range(len(self.editor.prompt)):
            self.editor.moveCursor(QtGui.QTextCursor.Right, QtGui.QTextCursor.KeepAnchor)
        self.editor.textCursor().removeSelectedText()
        self.editor.textCursor().insertText(command)
        self.editor.moveCursor(QtGui.QTextCursor.End)

    def getConstruct(self, command):
        if self.construct:
            prev_command = self.construct[-1]
            self.construct.append(command)
            if not prev_command and not command:
                ret_val = '\n'.join(self.construct)
                self.construct = []
                return ret_val
            else:
                return ''
        else:
            if command and command[-1] == (':'):
                self.construct.append(command)
                return ''
            else:
                return command

    def getHistory(self):
        return self.history

    def setHisory(self, history):
        self.history = history

    def addToHistory(self, command):
        if command and (not self.history or self.history[-1] != command):
            self.history.append(command)
        self.history_index = len(self.history)

    def getPrevHistoryEntry(self):
        if self.history:
            self.history_index = max(0, self.history_index - 1)
            return self.history[self.history_index]
        return ''

    def getNextHistoryEntry(self):
        if self.history:
            hist_len = len(self.history)
            self.history_index = min(hist_len, self.history_index + 1)
            if self.history_index < hist_len:
                return self.history[self.history_index]
        return ''

    def getCursorPosition(self):
        return self.editor.textCursor().columnNumber() - len(self.editor.prompt)

    def setCursorPosition(self, position):
        self.editor.moveCursor(QtGui.QTextCursor.StartOfLine)
        for i in range(len(self.editor.prompt) + position):
            self.editor.moveCursor(QtGui.QTextCursor.Right)

    def runCode(self):
        global global_envs
        command = self.getCommand()
        self.addToHistory(command)

        command = self.getConstruct(command)

        if command:
            tmp_stdout = sys.stdout

            class stdoutProxy():
                def __init__(self, write_func):
                    self.write_func = write_func
                    self.skip = False

                def write(self, text):
                    if not self.skip:
                        stripped_text = text.rstrip('\n')
                        self.write_func(stripped_text)
                        QtCore.QCoreApplication.processEvents()
                    self.skip = not self.skip

            sys.stdout = stdoutProxy(self.text_res.append)
            try:
                try:
                    if command[0] is not ('(', '( ') or command[-1] is not (')', ' )'):
                        pass
                    lex = Lexical_Stack(command)
                    lex.tokenize()
                    make = MakeOut(lex.stack)
                    global_envs = []
                    make.out()
                    rea = make.result

                    # OLD VERSION
                    # lex = Lexer(command)
                    # par = Parser(lex)
                    # seman = SemanticAnalyzer(par.expr())
                    # global_envs = []
                    # result = make_stack(interpret(seman.summin_parser()))
                    # val = visit_Atom(result)

                    if rea == 'REPORT':
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Information)
                        msg.setText('BUG_REPORT# hazard@dev.co.kr <-- send')
                        msg.setWindowTitle('Error')
                        exe = msg.exec_()
                        self.print_debug_info('R',
                                              '<font color = "blue"><b> RunCode </b></font> <br> <b>Thanks to report :)</b> ')
                        self.debug_stack.clearHelper()

                    if rea == 'ABORT':
                        time.sleep(1)
                        self.debug_stack.clearHelper()
                        self.text_res.append('EXIT(ABORT FUNCTION) BYE : )')
                        time.sleep(.5)
                        os.abort()

                    if rea is not None:
                        if type(rea) is list:
                            if rea[0] == 'INPUT':
                                num, ok = QInputDialog.getInt(self, 'Input Window', 'Enter a Num')
                                if ok:
                                    self.debug_stack.clearHelper()
                                    standard_env[rea[1]] = visit_Atom(num, standard_env)
                                    self.text_res.append('{val} := {input}'.format(val = rea[1], input = num))

                            else:
                                self.debug_stack.clearHelper()
                                self.text_res.append('RESULT > ' + print_expr(rea))
                        else:
                            self.debug_stack.clearHelper()
                            self.text_res.append('RESULT > ' + rea)

                except SyntaxError:
                    self.print_debug_info('R',
                                          '<font color = "pink"><b> RunCode </b></font> <br> <b>RETURN :</b> ' + 'nil')
                    self.print_debug_info('R','<font color = "pink"><b> RunCode </b></font> <br> <b>INPUT CODE:</b> '+ '#SyntaxError check this code '+self.debug_stack.__repr__())
                    self.debug_stack.clearHelper()
                except AttributeError:
                    self.print_debug_info('R',
                                          '<font color = "pink"><b> RunCode </b></font> <br> <b>RETURN :</b> ' + 'nil')
                    self.print_debug_info('R','<font color = "pink"><b> RunCode </b></font> <br> <b>INPUT CODE:</b> '+ '#AttributeError check this code '+self.debug_stack.__repr__())
                    self.debug_stack.clearHelper()
                except IndexError:
                    self.print_debug_info('R',
                                          '<font color = "pink"><b> RunCode </b></font> <br> <b>RETURN :</b> ' + 'nil')
                    self.print_debug_info('R','<font color = "pink"><b> RunCode </b></font> <br> <b>INPUT CODE:</b> ' + '#IndexError check this code ' + self.debug_stack.__repr__())
                    self.debug_stack.clearHelper()
                except TypeError:
                    self.print_debug_info('R',
                                          '<font color = "pink"><b> RunCode </b></font> <br> <b>RETURN :</b> ' + 'nil')
                    self.print_debug_info('R','<font color = "pink"><b> RunCode </b></font> <br> <b>INPUT CODE:</b> ' + '#TypeError check this code ' + self.debug_stack.__repr__())
                    self.debug_stack.clearHelper()
                except OSError:
                    self.print_debug_info('R',
                                          '<font color = "pink"><b> RunCode </b></font> <br> <b>RETURN :</b> ' + 'nil')
                    traceback_lines = traceback.format_exc().split('\n')
                    for i in (3, 2, 1, -1):
                        traceback_lines.pop(i)
                    self.print_debug_info('R','<font color = "pink"><b> RunCode </b></font> <br> <b>INPUT CODE:</b> ' + '#TypeError check this code ' + '\n'.join(traceback_lines))
                    self.debug_stack.clearHelper()
            except SystemExit:
                self.close()

            sys.stdout = tmp_stdout
        self.newPrompt()

    def keyPressEvent(self, event):
        if event.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return):
            self.runCode()
            return
        if event.key() == QtCore.Qt.Key_Home:
            self.setCursorPosition(0)
            return
        if event.key() == QtCore.Qt.Key_PageUp:
            return
        elif event.key() in (QtCore.Qt.Key_Left, QtCore.Qt.Key_Backspace):
            if self.getCursorPosition() == 0:
                return
        elif event.key() == QtCore.Qt.Key_Up:
            self.setCommand(self.getPrevHistoryEntry())
            return
        elif event.key() == QtCore.Qt.Key_Down:
            self.setCommand(self.getNextHistoryEntry())
            return
        elif event.key() == QtCore.Qt.Key_D and event.modifiers() == QtCore.Qt.ControlModifier:
            self.close()
        super(Console, self).keyPressEvent(event)