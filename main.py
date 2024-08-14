import requests
import pprint
from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk

p = pprint.PrettyPrinter(indent=4)  # indent=4 - значит отступ в 4 пробела

endpoint = {
    # Позволяет запрашивать все поддерживаемые криптовалюты.
    # Возвращает идентификатор монеты, название и символьный код.
    "coins/list": "https://api.coingecko.com/api/v3/coins/list",

    # Позволяет запрашивать цену одной или нескольких криптовалют.
    # ids - идентификатор(ы) криптовалюты, разделенные запятой.
    # vs_currencies - символьный код(ы) поддерживаемых валют.
    "simple/price": "https://api.coingecko.com/api/v3/simple/price"
}


def cut_id_or_code_currency(label_option_str):
    start_pos = label_option_str.index("[") + 1
    return label_option_str[start_pos: -1].lower()


# Получить котировку.
def exchange():
    # Получаем выбранные значения базовой валюты и валюты котировки из выпадающих списков.
    cryptocurrency = cmb_cryptocurrency.get()
    vs_currency = cmb_vs_currency.get()

    # Если обе валюты выбраны, то формируем и выполняем запрос к API.
    if cryptocurrency and vs_currency:
        # Получаем идентификатор валюты из выбранного значения в выпадающем списке.
        cryptocurrency_id = cut_id_or_code_currency(cryptocurrency)
        # Получаем символьный код валюты котировки из выбранного значения в выпадающем списке.
        vs_currency_code = cut_id_or_code_currency(vs_currency)

        try:
            # Выполняем запрос на получения курса обмена на конкретную пару (базовая валюта / валюта котировки).
            url = endpoint["simple/price"]
            params = dict(ids=cryptocurrency_id, vs_currencies=vs_currency_code)
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if data:
                # Получаем курс обмена.
                exchange_rate = data[cryptocurrency_id][vs_currency_code]
                mb.showinfo("Курс обмена", f"За 1 {cryptocurrency}\n{exchange_rate} {vs_currency}")

        except Exception as e:
            mb.showerror("Ошибка", f"Произошла ошибка: {e}")
    else:
        mb.showwarning("Внимание!", "Выберите базовую валюту и валюту котировки!")


# Получить все поддерживаемые криптовалюты.
def get_coins_list():
    global cryptocurrencies
    try:
        # Выполняем запрос на получение всех поддерживаемых криптовалют.
        url = endpoint["coins/list"]
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data:
            for c in data:
                name = c['name']
                cur_id = c['id']
                # Формируем список (list) для выпадающего списка (Combobox).
                cryptocurrencies.append(f"{name} [{cur_id}]")
    except Exception as e:
        mb.showerror("Ошибка", f"Произошла ошибка: {e}")


# Cписок (list) базовых валют для выпадающего списка (Combobox).
cryptocurrencies = []
get_coins_list()

# Cписок (list) валют котировки для выпадающего списка (Combobox).
vs_currencies = sorted([
    'Bitcoin [BTC]',
    'Ethereum [ETH]',
    'Litecoin [LTC]',
    'Доллар США [USD]',
    'Дирхам ОАЭ [AED]',
    'Канадский доллар [CAD]',
    'Швейцарский франк [CHF]',
    'Китайский юань [CNY]',
    'Чешская крона [CZK]',
    'Евро [EUR]',
    'Фунт стерлингов [GBP]',
    'Японская йена [JPY]',
    'Российский рубль [RUB]',
    'Вьетнамский донг [VND]'
])

# Создаём окно приложения.
window = Tk()
window.title("Курсы обмена криптовалют")
window.geometry("500x100")

# Настройка сетки
window.columnconfigure(0, weight=4)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=4)

# Виджеты (элементы управления)
lbl_cryptocurrency = Label(window, text=f"Базовая криптовалюта ({len(cryptocurrencies)} шт.)")
lbl_cryptocurrency.grid(column=0, row=0, padx=8, pady=3, sticky=W)

lbl_vs_currency = Label(window, text=f"Валюта котировки ({len(vs_currencies)} шт.)")
lbl_vs_currency.grid(column=2, row=0, padx=8, pady=3, sticky=W)

cmb_cryptocurrency = ttk.Combobox(window, width=40, values=sorted(cryptocurrencies))
cmb_cryptocurrency.grid(column=0, row=1, padx=10, pady=4)

lbl_arrows = Label(window, width=2, text="⇄", font=("Calibre", 18))
lbl_arrows.grid(column=1, row=1, padx=5)

cmb_vs_currency = ttk.Combobox(window, width=40, values=vs_currencies)
cmb_vs_currency.grid(column=2, row=1, padx=10, pady=4)

btn_get_rate = Button(window, text="Получить курс обмена", command=exchange)
btn_get_rate.grid(column=0, row=2, padx=10, pady=5, columnspan=3, sticky=NSEW)

window.mainloop()
