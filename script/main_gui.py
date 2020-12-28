from PyQt5.QtWidgets import QComboBox, QVBoxLayout, QGridLayout, QLabel, QHBoxLayout, QPushButton, QWidget
from coin import Coin
import json
from add_coin_gui import AddCoinGui
from threading import Thread, Event


class MyThread(Thread):
    def __init__(self, event, coins):
        Thread.__init__(self)
        self.__frequency = 0.5
        self.stopped = event
        self.__coins = coins

    def run(self):
        while not self.stopped.wait(self.__frequency):
            for key, val in self.__coins.items():
                coin_obj = Coin(key)
                coin_price = coin_obj.get_price()
                for values in val:
                    if values[0]:
                        if values[1] >= coin_price:
                            coin_obj.call_notification()
                    else:
                        if values[1] <= coin_price:
                            coin_obj.call_notification()


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

        stopFlag = Event()
        thread = MyThread(stopFlag, self.__coins)
        thread.start()

        # this will stop the timer
        #stopFlag.set()

    def __delete_coin(self):
        coin_name = self.__coins_names_box.currentText()
        del self.__coins[coin_name]
        coin_index = self.__coins_names_box.findText(coin_name)
        self.__coins_names_box.removeItem(coin_index)
        self.__update_gui()

    def __add_coin(self):
        add_coin_obj = AddCoinGui(self)
        add_coin_obj.exec_()

        new_coin = add_coin_obj.get_coin()
        self.__coins.update(new_coin)
        self.__update_gui()
        print(self.__coins)

    def __update_gui(self):
        self.__coins_names_box.clear()
        self.__coins_names_box.addItems(self.__coins.keys())
        self.__coin_changed()

    def __coin_changed(self):
        for i in reversed(range(self.__prices_layout.count())):
            self.__prices_layout.itemAt(i).widget().setParent(None)

        self.__layout.removeItem(self.__prices_layout)
        for price in self.__coins[self.__coins_names_box.currentText()]:
            l1 = QLabel()
            if price[0]:
                l1.setText(f"UP: {price[1]}")
            else:
                l1.setText(f"DOWN: {price[1]}")
            self.__prices_layout.addWidget(l1)

        self.__layout.addLayout(self.__prices_layout, 1, 1, 1, 1)

    def __load_coins(self):
        self.__coins.clear()
        with open('result.json') as f:
            self.__coins = json.load(f)

    def save_coins(self):
        print(self.__coins)
        with open('result.json', 'w') as fp:
            json.dump(self.__coins, fp)
