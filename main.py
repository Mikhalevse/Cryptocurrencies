import requests
import pprint
from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk


p = pprint.PrettyPrinter(indent=4)  # indent=4 - значит отступ в 4 пробела

endpoint = {
    # Позволяет запрашивать все поддерживаемые монеты с указанием цены.
    # vs_currency - код поддерживаемой валюты
    "coins/markets": "https://api.coingecko.com/api/v3/coins/markets",
    # Позволяет запрашивать все поддерживаемые валюты
    "simple/supported_vs_currencies": "https://api.coingecko.com/api/v3/simple/supported_vs_currencies",
    # Позволяет запрашивать цену одной или нескольких монет, используя их уникальные идентификаторы
    # ids - идентификатор(ы) криптовалюты, разделенные запятой.
    # vs_currencies - код(ы) поддерживаемых валют
    "simple/price": "https://api.coingecko.com/api/v3/simple/price",
}


# id:name
currency = {
    'solana':   dict(name='Солана',     symbol="sln"),
    'bitcoin':  dict(name='Биткоин',    symbol="btc"),
    'ethereum': dict(name='Эфириум',    symbol="eth"),
}


cryptocurrency = []
for v in currency.values():
    cryptocurrency.append(f'{v['name']} [{v['symbol']}]')

p.pprint(cryptocurrency)


window = Tk()
window.title("Курсы криптовалют")
window.geometry("365x100")


lbl_cryptocurrency = Label(window, text="Криптовалюта")
lbl_cryptocurrency.grid(column=0, row=0, pady=3)

lbl_vs_currency = Label(window, text="Валюта")
lbl_vs_currency.grid(column=2, row=0, pady=3)

cmb_cryptocurrency = ttk.Combobox(window, values=cryptocurrency)
cmb_cryptocurrency.grid(column=0, row=1, padx=10, pady=4)

lbl_arrows = Label(window, text="⇄", font=("Calibre", 18))
lbl_arrows.grid(column=1, row=1, padx=5)

cmb_vs_currency = ttk.Combobox(window, values=cryptocurrency)
cmb_vs_currency.grid(column=2, row=1, padx=10, pady=4)

btn_get_rate = Button(window, text="Получить курс обмена")
btn_get_rate.grid(column=0, row=2, padx=10, pady=5, columnspan=3, sticky=NSEW)

window.mainloop()
