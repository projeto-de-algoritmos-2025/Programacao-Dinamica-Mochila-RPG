import flet as ft
import json
from knapsack import knapsack
from dungeon import DungeonManager
from game_utils import prepare_items_for_knapsack 

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

        self.race_dropdown = ft.Dropdown(
            width=220,
            label="Escolha sua Raça",
            value="nord", # Valor padrão
            options=[
                ft.dropdown.Option("nord", "🛡️ Nord (Defesa/Escudos)"),
                ft.dropdown.Option("orc", "🪓 Orc (Ataque/Espadas)"),
                ft.dropdown.Option("wood_elf", "🏹 Wood Elf (Arcos)"),
                ft.dropdown.Option("khajiit", "😼 Khajiit (Ouro/Loot)"),
                ft.dropdown.Option("imperial", "⚖️ Imperial (Equilibrado)"),
            ]
        )

        self.results_column = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)

        self.btn_dungeon = ft.ElevatedButton(
            "Explorar Dungeon", 
            icon=ft.Icons.FORT, 
            on_click=self.open_dungeon_modal,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.GREY_900, 
                color=ft.Colors.GREY_600,
            ),
            disabled=True 
        )

        # Construindo a Interface
        self.build_ui()

    def setup_page(self):
        """Configurações iniciais da janela."""
        self.page.title = "Tamriel Inventory Manager - Knapsack"
        self.page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=ft.Colors.INDIGO,
                on_primary=ft.Colors.WHITE,
                secondary=ft.Colors.BLUE_200,
                on_secondary=ft.Colors.BLACK,
                background=ft.Colors.GREY_50,
                on_background=ft.Colors.BLACK,
                surface=ft.Colors.WHITE,
                on_surface=ft.Colors.BLACK,
            ),
            use_material3=True,
        )
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
            # ### <--- MUDANÇA: Título temático e fonte serifada
            ft.Text("⚔️ Arsenal de Tamriel", size=24, weight=ft.FontWeight.BOLD, font_family="serif"),
            
            ft.Container(
                content=items_table, 
                border=ft.border.all(1, ft.Colors.GREY_400), 
                border_radius=10,
                height=300
            ),
            
            ft.Divider(),
            
            # Linha de Controles
            ft.Row([
                self.weight_input,
                self.race_dropdown, 
                ft.ElevatedButton(
                    "Equipar", # Nome do botão mudou
                    icon=ft.Icons.BACKPACK, 
                    on_click=self.on_calculate_click, 
                    bgcolor=ft.Colors.BLUE_800, 
                    color=ft.Colors.WHITE
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            ft.Divider(),

            ft.Row([
                self.btn_dungeon
            ], alignment=ft.MainAxisAlignment.CENTER)

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
            # ### <--- NOVO: Pegando stats para exibir na tabela
            stats = item.get("stats", {})
            atk = stats.get("attack", 0)
            defe = stats.get("defense", 0)
            
            table_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Image(src=f"/images/{item['image']}", width=30, height=30)),
                        ft.DataCell(ft.Text(item['name'])),
                        ft.DataCell(ft.Text(str(item['weight']))),
                        ft.DataCell(ft.Text(str(item['value']))),
                        # ### <--- NOVO: Coluna extra mostrando ataque e defesa
                        ft.DataCell(ft.Text(f"⚔️{atk}    🛡️{defe}", size=12)),
                    ]
                )
            )

        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Img")),
                ft.DataColumn(ft.Text("Item")),
                ft.DataColumn(ft.Text("Peso"), numeric=True),
                ft.DataColumn(ft.Text("🥮 Septims"), numeric=True), 
                ft.DataColumn(ft.Text("Stats")), 
            ],
            rows=table_rows,
            border=ft.border.all(1, ft.Colors.GREY_300),
            heading_row_color=ft.Colors.BLUE_50,
        )

    def create_result_card(self, item, is_discarded=False):
        """Cria card. Se is_discarded=True, deixa cinza/vermelho."""
        bg_color = ft.Colors.RED_50 if is_discarded else ft.Colors.WHITE
        text_color = ft.Colors.GREY if is_discarded else ft.Colors.BLACK
        
        # ### <--- NOVO: Se o item é "Favorito" da raça (definido no game_utils), fica dourado
        if item.get("is_favorite") and not is_discarded:
            bg_color = ft.Colors.AMBER_50
            
        stats = item.get("stats", {})
        info_text = f"P: {item['weight']} | 💰 {item.get('real_value', item['value'])}"
        
        # Mostra status de batalha se existirem
        if "attack" in stats:
            info_text += f" | ⚔️ {stats.get('attack',0)} | 🛡️ {stats.get('defense',0)}"

        return ft.Card(
            color=bg_color,
            elevation=2 if not is_discarded else 0,
            content=ft.Container(
                content=ft.Row([
                    ft.Image(src=f"/images/{item['image']}", width=50, height=50, fit=ft.ImageFit.CONTAIN, opacity=0.5 if is_discarded else 1.0),
                    ft.Column([
                        ft.Text(item['name'], size=14, weight=ft.FontWeight.BOLD, color=text_color),
                        ft.Text(info_text, size=11, color=ft.Colors.GREY_700)
                    ], alignment=ft.MainAxisAlignment.CENTER, expand=True),
                    
                    ft.Icon(ft.Icons.STAR, color=ft.Colors.AMBER, size=16) if item.get("is_favorite") and not is_discarded else ft.Container()
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

        race = self.race_dropdown.value if self.race_dropdown.value else "empty"
        
        # altera o 'value dos itens baseado na raça
        processed_items = prepare_items_for_knapsack(self.items_data, race)

        # usa os valores alterados por raça
        best_score, chosen, _ = knapsack(processed_items, max_w)
        
        self.current_backpack = chosen 
        self.btn_dungeon.disabled = False
        self.btn_dungeon.color=ft.Colors.WHITE

        # Limpa resultados anteriores
        self.results_column.controls.clear()
        
        self.update_results_panel(best_score, chosen, title=f"Mochila ({race.capitalize()})")
        self.page.update()

    def update_results_panel(self, score, items, title="Resultado"):
        self.results_column.controls.clear()
        
        # Calculando totais para exibir no resumo
        total_gold = sum(i.get('real_value', i['value']) for i in items)
        total_atk = sum(i.get('stats', {}).get('attack', 0) for i in items)
        total_def = sum(i.get('stats', {}).get('defense', 0) for i in items)

        self.results_column.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Text(title, size=20, weight=ft.FontWeight.BOLD),
                    # Mostra "Score de Afinidade" em vez de Valor Total
                    ft.Text(f"✨ Score de Afinidade: {score}", size=16, color=ft.Colors.BLUE_700),
                    
                    # Linha com ícones de Ouro, Ataque e Defesa totais
                    ft.Row([
                        ft.Text(f"💰 {total_gold}", color=ft.Colors.AMBER_800, weight=ft.FontWeight.BOLD),
                        ft.Text(f"⚔️ {total_atk}", color=ft.Colors.RED_700, weight=ft.FontWeight.BOLD),
                        ft.Text(f"🛡️ {total_def}", color=ft.Colors.BLUE_GREY_700, weight=ft.FontWeight.BOLD),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    
                    ft.Text(f"🎒 Peso: {sum(i['weight'] for i in items)}kg", size=14),
                ]),
                padding=10, bgcolor=ft.Colors.BLUE_50, border_radius=10
            )
        )
        
        self.results_column.controls.append(ft.Text(f"Inventário ({len(items)}):", weight=ft.FontWeight.BOLD))
        for item in items:
            self.results_column.controls.append(self.create_result_card(item))

    def open_dungeon_modal(self, e):
        loot = self.dungeon_manager.generate_loot(quantity=3)
        
        # Calcula o descarte ideal 
        raw_value = self.weight_input.value or "0"
        max_w = int(raw_value)
        race = self.race_dropdown.value if self.race_dropdown.value else "empty"
        processed_loot = prepare_items_for_knapsack(loot, race)
        
        kept, discarded, new_score = self.dungeon_manager.discard_overweight(
            self.current_backpack, processed_loot, max_w
        )
        
        # Itens encontrados no loot
        loot_display = ft.Column([ft.Text("🎁 Você encontrou:", weight=ft.FontWeight.BOLD)] + 
                                 [self.create_result_card(i) for i in loot])
        
        # Itens mantidos
        kept_display = ft.Column([ft.Text("✅ Mantidos:", color=ft.Colors.GREEN)] + 
                                 [self.create_result_card(i) for i in kept], scroll=ft.ScrollMode.AUTO, height=400)
        
        # Itens descartados
        discarded_display = ft.Column([ft.Text("🗑️ Descartados:", color=ft.Colors.RED)] + 
                                      [self.create_result_card(i, is_discarded=True) for i in discarded], scroll=ft.ScrollMode.AUTO, height=300)

        # Atualiza a mochila principal com o resultado (caso a gnt feche o modal, já está salvo)
        self.current_backpack = kept
        self.update_results_panel(new_score, kept, title=f"Pós-Dungeon ({race.capitalize()})")

        # Configurar o Modal
        dlg = ft.AlertDialog(
            title=ft.Text("Resultado da Exploração 🏔️⚔️🏔️"),
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