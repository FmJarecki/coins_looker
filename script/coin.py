from plyer import notification
from web_scrapper import download_phrase_from_marker


class Coin:
    def __init__(self, name):
        self.__name = name.lower()
        self.__name = self.__name.replace(" ", "-")
        self.__short_name = download_phrase_from_marker(self.__name, 'script', 'symbol', 9, '\"')
        self.__price = 0.0
        self.update_price()

    def update_price(self):
        new_price = download_phrase_from_marker(self.__name, 'span', 'price__price', 15, '<')
        new_price = new_price.replace(",", "")
        self.__price = float(new_price)

    def get_price(self):
        return self.__price

    def call_notification(self):
        notification.notify(
            title=f'{self.__name} price!',
            message=f'{self.__short_name} price: {self.__price} USD',
            app_icon="icon/Paomedia-Small-N-Flat-Bell.ico",
            timeout=5
        )
