from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QCompleter, QLineEdit, QGridLayout, QLabel, QPushButton, QDialog, QRadioButton, QHBoxLayout
from web_scrapper import scrap_all_coins_from_market
from coin import Coin


class AddCoinGui(QDialog):
    def __init__(self, parent):
        super(AddCoinGui, self).__init__(parent)
        self.__coins_names = scrap_all_coins_from_market()
        self.__coin_prices = []

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

        radiobuttons_lay = QGridLayout()
        self.__up_radiobutton = QRadioButton("UP")
        self.__up_radiobutton.setChecked(True)
        radiobuttons_lay.addWidget(self.__up_radiobutton, 0, 0, 1, 1)

        self.__down_radiobutton = QRadioButton("DOWN")
        radiobuttons_lay.addWidget(self.__down_radiobutton, 0, 1, 1, 1)

        layout.addLayout(radiobuttons_lay, 1, 1)
        self.__radiobutton_state = 'UP'

        self.__accept_button = QPushButton("Add value")
        self.__accept_button.clicked.connect(self.__accept_button_clicked)
        layout.addWidget(self.__accept_button, 2, 0, 1, 2)

        self.__accept_button = QPushButton("Add coin and exit!")
        self.__accept_button.clicked.connect(self.__save_coin)
        layout.addWidget(self.__accept_button, 3, 0, 1, 2)

        self.setLayout(layout)
        self.setModal(True)
        self.resize(300, 300)

    def get_coin(self):
        if len(self.__coin_prices) > 0:
            return {self.__lineEdit.text(): self.__coin_prices}
        else:
            return {}

    def __save_coin(self):
        self.close()

    def __accept_button_clicked(self):
        radiobutton_state = self.__up_radiobutton.isChecked()
        self.__coin_prices.append((radiobutton_state, self.__value_spin_box.value()))

    def __on_text_changed(self):
        for coin_name in self.__coins_names:
            if self.__lineEdit.text() == coin_name:
                btc = Coin(self.__lineEdit.text())
                self.__value_spin_box.setValue(btc.get_price())
