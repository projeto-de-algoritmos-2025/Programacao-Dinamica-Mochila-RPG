import flet as ft
import json
from knapsack import knapsack
from dungeon import DungeonManager

class RPGKnapsackApp:
    def __init__(self, page: ft.Page):
        self.page = page
        
        self.setup_page()
        
        # Carregando os dados dos itens
        self.items_data = self.load_data()
        self.dungeon_manager = DungeonManager(self.items_data) 
        self.current_backpack = [] 
        
        # Inicializar Componentes de UI 
        self.weight_input = ft.TextField(
            label="Peso Máximo", 
            value="15", 
            text_align=ft.TextAlign.RIGHT, 
            width=150
        )
        self.results_column = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)

        self.btn_dungeon = ft.ElevatedButton(
            "Explorar Dungeon (+ Loot)", 
            icon=ft.Icons.FORT, # Ícone de castelo/forte
            on_click=self.open_dungeon_modal,
            bgcolor=ft.Colors.PURPLE_700,
            color=ft.Colors.WHITE,
            disabled=True # Só habilita depois de calcular a primeira mochila
        )

        # Construindo a Interface
        self.build_ui()

    def setup_page(self):
        """Configurações iniciais da janela."""
        self.page.title = "Mochila de RPG - Knapsack"
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
                    color=ft.Colors.WHITE,
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([
                self.btn_dungeon 
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ], scroll=ft.ScrollMode.AUTO, expand=True,
        )

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

    def create_result_card(self, item, is_discarded=False):
        """Cria card. Se is_discarded=True, deixa cinza/vermelho."""
        bg_color = ft.Colors.RED_50 if is_discarded else ft.Colors.WHITE
        text_color = ft.Colors.GREY if is_discarded else ft.Colors.BLACK
        icon = ft.Icons.DELETE_OUTLINE if is_discarded else None

        return ft.Card(
            color=bg_color,
            content=ft.Container(
                content=ft.Row([
                    ft.Image(src=f"/images/{item['image']}", width=50, height=50, fit=ft.ImageFit.CONTAIN, opacity=0.5 if is_discarded else 1.0),
                    ft.Column([
                        ft.Text(item['name'], size=14, weight=ft.FontWeight.BOLD, color=text_color),
                        ft.Text(f"P: {item['weight']} | V: {item['value']}", size=12, color=ft.Colors.GREY_700)
                    ], alignment=ft.MainAxisAlignment.CENTER, expand=True),
                    ft.Icon(icon, color=ft.Colors.RED_400) if icon else ft.Container()
                ]),
                padding=5,
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
        
        self.current_backpack = chosen 
        
        self.btn_dungeon.disabled = False

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

    def update_results_panel(self, value, items, title="Resultado"):
        self.results_column.controls.clear()
        
        # Card de Resumo
        self.results_column.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Text(title, size=20, weight=ft.FontWeight.BOLD),
                    ft.Text(f"💰 Valor Total: {value}", size=18, color=ft.Colors.GREEN_700),
                    ft.Text(f"🎒 Peso Atual: {sum(i['weight'] for i in items)}kg", size=14),
                ]),
                padding=10, bgcolor=ft.Colors.GREEN_50, border_radius=10
            )
        )
        
        self.results_column.controls.append(ft.Text(f"Itens ({len(items)}):", weight=ft.FontWeight.BOLD))
        for item in items:
            self.results_column.controls.append(self.create_result_card(item))

    def open_dungeon_modal(self, e):
        # 1. Gerar Loot
        loot = self.dungeon_manager.generate_loot(quantity=3)
        
        # 2. Calcular o Descarte Ideal (Lógica que você fez)
        raw_value = self.weight_input.value or "0"
        max_w = int(raw_value)
        kept, discarded, new_value = self.dungeon_manager.discard_overweight(
            self.current_backpack, loot, max_w
        )
        
        # Itens Encontrados no loot
        loot_display = ft.Column([ft.Text("🎁 Você encontrou:", weight=ft.FontWeight.BOLD)] + 
                                 [self.create_result_card(i) for i in loot])
        
        # Itens Mantidos
        kept_display = ft.Column([ft.Text("✅ Mantidos:", color=ft.Colors.GREEN)] + 
                                 [self.create_result_card(i) for i in kept], scroll=ft.ScrollMode.AUTO, height=400)
        
        # Itens Descartados
        discarded_display = ft.Column([ft.Text("🗑️ Descartados:", color=ft.Colors.RED)] + 
                                      [self.create_result_card(i, is_discarded=True) for i in discarded], scroll=ft.ScrollMode.AUTO, height=300)

        # Atualiza a mochila principal com o resultado (caso a gnt feche o modal, já está salvo)
        self.current_backpack = kept
        self.update_results_panel(new_value, kept, title="Mochila Pós-Dungeon")

        # Configurar o Modal
        dlg = ft.AlertDialog(
            title=ft.Text("Resultado da Exploração 🏰"),
            content=ft.Container(
                width=900,
                content=ft.Row([
                    ft.Container(loot_display, expand=1, padding=5, bgcolor=ft.Colors.AMBER_50, border_radius=5),
                    ft.VerticalDivider(),
                    ft.Container(kept_display, expand=1),
                    ft.VerticalDivider(),
                    ft.Container(discarded_display, expand=1),
                ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.START)
            ),
            actions=[
                ft.TextButton("Continuar", on_click=lambda e: self.close_modal(e.control.parent))
            ],
        )
        
        self.page.open(dlg)

    def close_modal(self, dlg):
        self.page.close(dlg)

def main(page: ft.Page):
    RPGKnapsackApp(page)

if __name__ == "__main__":
    ft.app(target=main, assets_dir="data")