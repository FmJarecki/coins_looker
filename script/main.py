from coin import Coin
from main_gui import MainGui
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = MainGui()
    gui.resize(600, 600)
    gui.show()
    app.exec_()
    gui.save_coins()




