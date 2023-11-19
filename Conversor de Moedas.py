import tkinter as tk
from tkinter import ttk
import requests

class ConversorMoedas:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor de Moedas")

        self.base_label = ttk.Label(root, text="Moeda Base:")
        self.base_label.grid(row=0, column=0, padx=10, pady=10)

        self.base_combobox = ttk.Combobox(root, values=self.obter_lista_moedas())
        self.base_combobox.grid(row=0, column=1, padx=10, pady=10)
        self.base_combobox.set("BRL")

        self.quantidade_label = ttk.Label(root, text="Valor que será convertido:")
        self.quantidade_label.grid(row=1, column=0, padx=10, pady=10)

        self.quantidade_entry = ttk.Entry(root)
        self.quantidade_entry.grid(row=1, column=1, padx=10, pady=10)

        self.destino_label = ttk.Label(root, text="Moeda de Destino:")
        self.destino_label.grid(row=2, column=0, padx=10, pady=10)

        self.destino_combobox = ttk.Combobox(root, values=self.obter_lista_moedas())
        self.destino_combobox.grid(row=2, column=1, padx=10, pady=10)
        self.destino_combobox.set("USD")

        self.converter_button = ttk.Button(root, text="Converter", command=self.converter)
        self.converter_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.resultado_label = ttk.Label(root, text="")
        self.resultado_label.grid(row=4, column=0, columnspan=2, pady=10)

    def obter_lista_moedas(self):
        moedas = ['BRL', 'USD', 'EUR', 'KRW', 'CNY', 'AOA', 'JPY']
        return moedas

    def obter_taxas(self, base):
        url = f'https://open.er-api.com/v6/latest/{base}'
        try:
            resposta = requests.get(url)
            resposta.raise_for_status()
            dados = resposta.json()
            return dados['rates']
        except requests.exceptions.RequestException as e:
            print(f"Erro na obtenção das taxas: {e}")
            return {}

    def converter_moeda(self, valor, para, taxas):
        taxa_para = taxas[para]
        valor_convertido = valor * taxa_para
        return valor_convertido

    def converter(self):
        base = self.base_combobox.get()
        quantidade = float(self.quantidade_entry.get())
        destino = self.destino_combobox.get()

        try:
            taxas = self.obter_taxas(base)
            resultado = self.converter_moeda(quantidade, destino, taxas)
            self.resultado_label.config(text=f"{quantidade} {base} é equivalente a {resultado:.2f} {destino}")
        except KeyError:
            self.resultado_label.config(text="Moeda não encontrada. Verifique os códigos de moeda e tente novamente.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConversorMoedas(root)
    root.mainloop()
