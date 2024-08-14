import asyncio
import aiohttp
import tkinter as tk
from tkinter import messagebox as mb
from tkinter import ttk

endpoint = {
    "coins/list": "https://api.coingecko.com/api/v3/coins/list",
    "simple/price": "https://api.coingecko.com/api/v3/simple/price"
}

def cut_id_or_code_currency(label_option_str):
    start_pos = label_option_str.index("[") + 1
    return label_option_str[start_pos: -1].lower()

async def fetch(url, params=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            response.raise_for_status()
            return await response.json()

async def exchange():
    cryptocurrency = cmb_cryptocurrency.get()
    vs_currency = cmb_vs_currency.get()

    if cryptocurrency and vs_currency:
        cryptocurrency_id = cut_id_or_code_currency(cryptocurrency)
        vs_currency_code = cut_id_or_code_currency(vs_currency)

        try:
            url = endpoint["simple/price"]
            params = dict(ids=cryptocurrency_id, vs_currencies=vs_currency_code)
            data = await fetch(url, params=params)

            if data:
                exchange_rate = data[cryptocurrency_id][vs_currency_code]
                mb.showinfo("Курс обмена", f"За 1 {cryptocurrency}\n{exchange_rate} {vs_currency}")
        except aiohttp.ClientError as e:
            mb.showerror("Ошибка", f"Ошибка соединения: {e}")
        except Exception as e:
            mb.showerror("Ошибка", f"Произошла ошибка: {e}")
    else:
        mb.showwarning("Внимание!", "Выберите базовую валюту и валюту котировки!")

async def get_coins_list():
    global cryptocurrencies
    try:
        url = endpoint["coins/list"]
        data = await fetch(url)
        if data:
            popular_cryptos = {'bitcoin', 'ethereum', 'litecoin', 'ripple', 'dogecoin', 'binancecoin', 'cardano'}
            for c in data:
                name = c['name']
                cur_id = c['id']
                if cur_id in popular_cryptos:
                    cryptocurrencies.append(f"{name} [{cur_id}]")
            cmb_cryptocurrency['values'] = sorted(cryptocurrencies)
    except aiohttp.ClientError as e:
        mb.showerror("Ошибка", f"Ошибка соединения: {e}")
    except Exception as e:
        mb.showerror("Ошибка", f"Произошла ошибка: {e}")

def run_get_coins_list():
    asyncio.run(get_coins_list())

cryptocurrencies = []

vs_currencies = sorted([
    'Доллар США [USD]',
    'Евро [EUR]',
    'Фунт стерлингов [GBP]',
    'Японская йена [JPY]',
    'Российский рубль [RUB]'
])

window = tk.Tk()
window.title("Курсы обмена криптовалют")
window.geometry("500x150")

window.columnconfigure(0, weight=4)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=4)

lbl_cryptocurrency = tk.Label(window, text="Криптовалюта (базовая валюта)")
lbl_cryptocurrency.grid(column=0, row=0, padx=8, pady=3, sticky=tk.W)

lbl_vs_currency = tk.Label(window, text="Валюта котировки")
lbl_vs_currency.grid(column=2, row=0, padx=8, pady=3, sticky=tk.W)

cmb_cryptocurrency = ttk.Combobox(window, width=40)
cmb_cryptocurrency.grid(column=0, row=1, padx=10, pady=4)

lbl_arrows = tk.Label(window, width=2, text="⇄", font=("Calibre", 18))
lbl_arrows.grid(column=1, row=1, padx=5)

cmb_vs_currency = ttk.Combobox(window, width=40, values=vs_currencies)
cmb_vs_currency.grid(column=2, row=1, padx=10, pady=4)

btn_get_rate = tk.Button(window, text="Получить курс обмена", command=lambda: asyncio.run(exchange()))
btn_get_rate.grid(column=0, row=2, padx=10, pady=5, columnspan=3, sticky=tk.NSEW)

window.after(100, run_get_coins_list)

window.mainloop()
