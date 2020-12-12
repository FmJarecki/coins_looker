import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QComboBox, QVBoxLayout, QGridLayout, QLabel, QHBoxLayout
from web_scrapper import scrap_all_coins_from_market
from coin import Coin
import json


class MainGui:
    def __init__(self):
        self.__coins = {}
        self.__load_coins()
        self.__prices_layout = QVBoxLayout()
        app = QtWidgets.QApplication(sys.argv)
        widget = QtWidgets.QWidget()
        widget.resize(400, 200)
        widget.setWindowTitle("This is PyQt Widget example")

        self.__layout = QGridLayout()

        combo_layout = QHBoxLayout()

        l1 = QLabel()
        l1.setText("Available coins: ")
        combo_layout.addWidget(l1)

        self.__coins_names_box = QComboBox()
        self.__coins_names_box.addItems(self.__coins.keys())
        self.__coins_names_box.activated.connect(self.__coin_changed)
        combo_layout.addWidget(self.__coins_names_box)
        self.__layout.addLayout(combo_layout, 0, 0, 1, 2)
        l1 = QLabel()
        l1.setText("Setted prices: ")
        self.__layout.addWidget(l1, 1, 0, 1, 1)

        widget.setLayout(self.__layout)
        widget.show()
        exit(app.exec_())

    def __coin_changed(self):
        for i in reversed(range(self.__prices_layout.count())):
            self.__prices_layout.itemAt(i).widget().setParent(None)
        for price in self.__coins[self.__coins_names_box.currentText()]:
            l1 = QLabel()
            l1.setText(f"{price}")
            self.__prices_layout.addWidget(l1)
        self.__layout.addLayout(self.__prices_layout, 1, 1, 1, 1)

    def __load_coins(self):
        with open('result.json') as f:
            self.__coins = json.load(f)
