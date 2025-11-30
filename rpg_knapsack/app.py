import flet as ft
import json
from knapsack import knapsack

class RPGKnapsackApp:
    def __init__(self, page: ft.Page):
        self.page = page
        
        self.setup_page()
        
        # Carregando os dados dos itens
        self.items_data = self.load_data()
        
        # Inicializar Componentes de UI 
        self.weight_input = ft.TextField(
            label="Peso Máximo", 
            value="15", 
            text_align=ft.TextAlign.RIGHT, 
            width=150
        )
        self.results_column = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)

        # Construindo a Interface
        self.build_ui()

    def setup_page(self):
        """Configurações iniciais da janela."""
        self.page.title = "Mochila de RPG - Knapsack (OO Version)"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 20
        self.page.window.width = 1000
        self.page.window.height = 700

    def load_data(self):
        """Lê o arquivo JSON de itens."""
        try:
            with open("data/items.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            self.page.add(ft.Text(f"Erro ao ler data/items.json: {e}", color=ft.Colors.RED))
            return []

    def build_ui(self):
        """Monta o layout principal da aplicação."""
        
        # Cria a tabela usando os dados carregados
        items_table = self.create_items_table()

        # Painel Esquerdo (Inputs e Tabela)
        left_panel = ft.Column([
            ft.Text("🛡️ Itens Disponíveis", size=24, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=items_table, 
                border=ft.border.all(1, ft.Colors.GREY_200), 
                border_radius=10
            ),
            ft.Divider(),
            ft.Row([
                ft.Text("Capacidade da Mochila:"),
                self.weight_input,
                ft.ElevatedButton(
                    "Calcular", 
                    icon=ft.Icons.CALCULATE, 
                    on_click=self.on_calculate_click, 
                    bgcolor=ft.Colors.BLUE_600, 
                    color=ft.Colors.WHITE
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ], scroll=ft.ScrollMode.AUTO, expand=True)

        # Painel Direito (Resultados)
        right_panel = ft.Container(
            content=self.results_column,
            padding=10,
            border=ft.Border(left=ft.BorderSide(1, ft.Colors.GREY_300)),
            expand=True
        )

        # Layout Principal (Divisão da tela)
        layout = ft.Row([
            ft.Container(left_panel, expand=6, padding=10),
            ft.Container(right_panel, expand=4, padding=10)
        ], expand=True)

        self.page.add(layout)

    def create_items_table(self):
        """Gera a DataTable com base nos itens."""
        table_rows = []
        for item in self.items_data:
            table_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Image(src=f"/images/{item['image']}", width=30, height=30)),
                        ft.DataCell(ft.Text(item['name'])),
                        ft.DataCell(ft.Text(str(item['weight']))),
                        ft.DataCell(ft.Text(str(item['value']))),
                    ]
                )
            )

        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Img")),
                ft.DataColumn(ft.Text("Nome")),
                ft.DataColumn(ft.Text("Peso"), numeric=True),
                ft.DataColumn(ft.Text("Valor"), numeric=True),
            ],
            rows=table_rows,
            border=ft.border.all(1, ft.Colors.GREY_300),
            vertical_lines=ft.border.BorderSide(1, ft.Colors.GREY_200),
            heading_row_color=ft.Colors.BLUE_50,
        )

    def create_result_card(self, item):
        """Cria um Card visual para um item escolhido."""
        return ft.Card(
            content=ft.Container(
                content=ft.Row([
                    ft.Image(src=f"/images/{item['image']}", width=60, height=60, fit=ft.ImageFit.CONTAIN, border_radius=5),
                    ft.Column([
                        ft.Text(item['name'], size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Peso: {item['weight']}kg | Valor: {item['value']}", size=12, color=ft.Colors.GREY_700)
                    ], alignment=ft.MainAxisAlignment.CENTER),
                ]),
                padding=10,
            )
        )

    def on_calculate_click(self, e):
        """Evento de clique do botão Calcular."""
        try:
            if not self.weight_input.value:
                raise ValueError("empty")
            max_w = int(self.weight_input.value)
        except ValueError:
            self.weight_input.error_text = "Digite um número inteiro"
            self.weight_input.update()
            return

        # Limpar erro se houver sucesso na conversão
        self.weight_input.error_text = None
        self.weight_input.update()

        # Executa o algoritmo (lógica importada)
        best_value, chosen, _ = knapsack(self.items_data, max_w)
        
        # Limpa resultados anteriores
        self.results_column.controls.clear()
        
        # Adiciona Cabeçalho do Resultado
        self.results_column.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Text("Resultado do Algoritmo", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text(f"💰 Melhor Valor Total: {best_value}", size=18, color=ft.Colors.GREEN_700),
                ]),
                padding=10,
                bgcolor=ft.Colors.GREEN_50,
                border_radius=10
            )
        )

        # Adiciona Lista de Itens
        self.results_column.controls.append(ft.Text(f"Itens Escolhidos ({len(chosen)}):", weight=ft.FontWeight.BOLD))

        for item in chosen:
            card = self.create_result_card(item)
            self.results_column.controls.append(card)
        
        # Atualiza a página para mostrar as mudanças
        self.page.update()

def main(page: ft.Page):
    RPGKnapsackApp(page)

if __name__ == "__main__":
    ft.app(target=main, assets_dir="data")