import sys
from PyQt5 import QtWidgets
from multiprocessing import Process
from src.front.console import Console

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    console = Console()
    P = Process(target=console.show())
    P.start()
    P.join()
    sys.exit(app.exec_())