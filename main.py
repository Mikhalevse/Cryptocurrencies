import requests
import pprint
from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk


p = pprint.PrettyPrinter(indent=4)  # indent=4 - значит отступ в 4 пробела

endpoint = {
    # Позволяет запрашивать все поддерживаемые монеты.
    # Возвращает идентификатор монеты, название и символьный код.
    "coins/list": "https://api.coingecko.com/api/v3/coins/list",
    # Позволяет запрашивать все поддерживаемые монеты с указанием цены.
    # vs_currency - код поддерживаемой валюты
    # locale - локализация данных (по умолчанию: en)
    "coins/markets": "https://api.coingecko.com/api/v3/coins/markets",
    # Позволяет запрашивать все поддерживаемые валюты
    "simple/supported_vs_currencies": "https://api.coingecko.com/api/v3/simple/supported_vs_currencies",
    # Позволяет запрашивать цену одной или нескольких монет, используя их уникальные идентификаторы
    # ids - идентификатор(ы) криптовалюты, разделенные запятой.
    # vs_currencies - символьный код(ы) поддерживаемых валют
    "simple/price": "https://api.coingecko.com/api/v3/simple/price"
}


# Получить идентификаторы, локализованные названия и коды (крипто)валют.
def get_coins_markets():
    global cryptocurrencies
    try:
        url = endpoint["coins/list"]
        # params = dict(vs_currency="usd", locale="ru")
        # response = requests.get(url, params=params)
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        p.pprint(len(data))

        if data:
            for c in data:
                cryptocurrencies[c["id"]] = dict(name=c["name"], symbol=c["symbol"])

    except Exception as e:
        mb.showerror("Ошибка", f"Произошла ошибка: {e}")
    pass


def set_cryptocurrencies_names_for_cmb():
    global cryptocurrencies_for_cmb

    for v in cryptocurrencies.values():
        cryptocurrencies_for_cmb.append(f'{v['name']} [{v['symbol']}]')

    sorted(cryptocurrencies_for_cmb)

    p.pprint(cryptocurrencies_for_cmb)
    pass


# id:name
cryptocurrencies = {}
#     'solana':   dict(name='Солана',     symbol="sln"),
#     'bitcoin':  dict(name='Биткоин',    symbol="btc"),
#     'ethereum': dict(name='Эфириум',    symbol="eth"),
# }



cryptocurrencies_for_cmb = []


get_coins_markets()
set_cryptocurrencies_names_for_cmb()


window = Tk()
window.title("Курсы криптовалют")
window.geometry("400x100")

# configure the grid
window.columnconfigure(0, weight=4)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=4)


lbl_cryptocurrency = Label(window, text="Криптовалюта")
lbl_cryptocurrency.grid(column=0, row=0, pady=3)

lbl_vs_currency = Label(window, text="Валюта")
lbl_vs_currency.grid(column=2, row=0, pady=3)

cmb_cryptocurrency = ttk.Combobox(window, width=40, values=cryptocurrencies_for_cmb)
cmb_cryptocurrency.grid(column=0, row=1, padx=10, pady=4)

lbl_arrows = Label(window, width=2, text="⇄", font=("Calibre", 18))
lbl_arrows.grid(column=1, row=1, padx=5)

cmb_vs_currency = ttk.Combobox(window, width=40, values=cryptocurrencies_for_cmb)
cmb_vs_currency.grid(column=2, row=1, padx=10, pady=4)

btn_get_rate = Button(window, text="Получить курс обмена")
btn_get_rate.grid(column=0, row=2, padx=10, pady=5, columnspan=3, sticky=NSEW)







window.mainloop()
