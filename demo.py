import sys
from PyQt5.QtWidgets import QApplication
import dataAnalysis

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = dataAnalysis.dataAnalysis()
    w.setWindowTitle('dataAnalysis')
    w.show()

    sys.exit(app.exec())