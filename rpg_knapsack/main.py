import json
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from knapsack import knapsack

class RPGKnapsackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mochila de RPG - Knapsack")

        # Carregar itens
        with open("data/items.json", "r") as f:
            self.items = json.load(f)

        # Interface esquerda
        left_frame = tk.Frame(root)
        left_frame.pack(side="left", padx=10, pady=10)

        tk.Label(left_frame, text="Itens Disponíveis", font=("Arial", 14)).pack()

        self.tree = ttk.Treeview(left_frame, columns=("peso", "valor"), show="headings", height=10)
        self.tree.heading("peso", text="Peso")
        self.tree.heading("valor", text="Valor")
        self.tree.pack()

        for item in self.items:
            self.tree.insert("", "end", values=(item["name"], item["weight"], item["value"]))

        tk.Label(left_frame, text="Peso máximo da mochila:").pack(pady=10)
        self.entry_weight = tk.Entry(left_frame)
        self.entry_weight.pack()

        tk.Button(left_frame, text="Calcular Mochila Ideal", command=self.calculate).pack(pady=20)

        self.result_text = tk.Text(root, width=40, height=20)
        self.result_text.pack(side="right", padx=10)

    def calculate(self):
        try:
            max_w = int(self.entry_weight.get())
        except ValueError:
            self.result_text.insert("end", "Peso inválido!\n")
            return

        best_value, chosen, dp_table = knapsack(self.items, max_w)

        self.result_text.delete("1.0", "end")
        self.result_text.insert("end", f"Melhor valor: {best_value}\n")
        self.result_text.insert("end", "Itens escolhidos:\n")

        for item in chosen:
            self.result_text.insert("end",
                                    f"- {item['name']} (Peso {item['weight']}, Valor {item['value']})\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = RPGKnapsackApp(root)
    root.mainloop()
