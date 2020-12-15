import sys
from PyQt5.QtWidgets import QComboBox, QVBoxLayout, QGridLayout, QLabel, QHBoxLayout, QPushButton, QWidget
from web_scrapper import scrap_all_coins_from_market
from coin import Coin
import json
from add_coin_gui import AddCoinGui


class MainGui(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.__coins = {}
        self.__load_coins()
        self.__prices_layout = QVBoxLayout()

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

        self.__add_coin_button = QPushButton("Add another coin")
        self.__add_coin_button.clicked.connect(self.__add_coin)
        self.__layout.addWidget(self.__add_coin_button, 2, 0, 1, 1)

        self.__delete_coin_button = QPushButton("Delete this coin")
        self.__delete_coin_button.clicked.connect(self.__delete_coin)
        self.__layout.addWidget(self.__delete_coin_button, 2, 1, 1, 1)
        self.__coin_changed()
        self.setLayout(self.__layout)

    def __delete_coin(self):
        coin_name = self.__coins_names_box.currentText()
        del self.__coins[coin_name]
        coin_index = self.__coins_names_box.findText(coin_name)
        self.__coins_names_box.removeItem(coin_index)

    def __add_coin(self):
        add_coin_obj = AddCoinGui(self)
        add_coin_obj.exec_()

        new_coin = add_coin_obj.get_coin()
        self.__coins.update(new_coin)
        print(self.__coins)

    def __coin_changed(self):
        for i in reversed(range(self.__prices_layout.count())):
            self.__prices_layout.itemAt(i).widget().setParent(None)

        self.__layout.removeItem(self.__prices_layout)
        for price in self.__coins[self.__coins_names_box.currentText()]:
            l1 = QLabel()
            l1.setText(f"{price}")
            self.__prices_layout.addWidget(l1)

        self.__layout.addLayout(self.__prices_layout, 1, 1, 1, 1)

    def __load_coins(self):
        self.__coins = []
        with open('result.json') as f:
            self.__coins = json.load(f)

    def save_coins(self):
        print(self.__coins)
        with open('result.json', 'w') as fp:
            json.dump(self.__coins, fp)
