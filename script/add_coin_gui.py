import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QCompleter, QLineEdit, QGridLayout, QLabel, QPushButton
from web_scrapper import scrap_all_coins_from_market
from coin import Coin
import json

class AddCoinGui:
    def __init__(self):
        self.__coins_names = scrap_all_coins_from_market()
        self.__choosen_values = {}

        app = QtWidgets.QApplication(sys.argv)
        widget = QtWidgets.QWidget()
        widget.resize(400, 200)
        widget.setWindowTitle("This is PyQt Widget example")

        layout = QGridLayout()

        l1 = QLabel()
        l1.setText("Choose coin: ")
        layout.addWidget(l1, 0, 0, 1, 1)

        completer = QCompleter(self.__coins_names)
        self.__lineEdit = QLineEdit()
        self.__lineEdit.setCompleter(completer)
        layout.addWidget(self.__lineEdit, 0, 1, 1, 1)

        self.__lineEdit.textChanged.connect(self.__on_text_changed)

        self.__value_spin_box = QtWidgets.QDoubleSpinBox()
        self.__value_spin_box.setPrefix("Value: ")
        self.__value_spin_box.setSuffix(" USD")
        self.__value_spin_box.setRange(0, 100000)
        self.__value_spin_box.setSingleStep(0.1)
        self.__value_spin_box.setValue(0)
        layout.addWidget(self.__value_spin_box, 1, 0, 1, 1)

        self.__accept_button = QPushButton("Add value")
        self.__accept_button.clicked.connect(self.__accept_button_clicked)
        layout.addWidget(self.__accept_button, 1, 1, 1, 1)

        self.__accept_button = QPushButton("Add coin and exit!")
        self.__accept_button.clicked.connect(self.__save_coin)
        layout.addWidget(self.__accept_button, 2, 0, 1, 2)

        widget.setLayout(layout)
        widget.show()
        exit(app.exec_())

    def __save_coin(self):
        with open('result.json', 'w') as fp:
            json.dump(self.__choosen_values, fp)

    def __accept_button_clicked(self):
        key = self.__lineEdit.text()
        if key in self.__choosen_values:
            self.__choosen_values[key].append(self.__value_spin_box.value())
        else:
            self.__choosen_values[key] = [self.__value_spin_box.value()]

    def __on_text_changed(self):
        for coin_name in self.__coins_names:
            if self.__lineEdit.text() == coin_name:
                btc = Coin(self.__lineEdit.text(), 5)
                self.__value_spin_box.setValue(btc.get_price())
