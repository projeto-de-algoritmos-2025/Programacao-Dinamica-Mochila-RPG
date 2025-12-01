import random
from knapsack import knapsack
import json

mock_inventory = [
    {'name': 'Escudo de Carvalho',  'weight': 5, 'value': 10,   'image': 'shield.jpg'}, 
    {'name': 'Poção de Cura',       'weight': 2, 'value': 4,    'image': 'potion.jpg'}, 
    {'name': 'Arco Élfico',         'weight': 4, 'value': 9,    'image': 'bow.png'}, 
    {'name': 'Arco de Auriel',      'weight': 4, 'value': 9,    'image': "auriel'sBow.png"}
]

all_items = [
  { "name": "Espada Longa", "weight": 7, "value": 13, "image": "sword.jpg" },
  { "name": "Escudo de Carvalho", "weight": 5, "value": 10, "image": "shield.jpg" },
  { "name": "Poção de Cura", "weight": 2, "value": 4, "image": "potion.jpg" },
  { "name": "Arco Élfico", "weight": 4, "value": 9, "image": "bow.png" },
  { "name": "Arco de Auriel", "weight": 4, "value": 9, "image": "auriel'sBow.png" },
  { "name": "Arco de Vidro", "weight": 4, "value": 9, "image": "GlassBow_SK.webp" },
  { "name": "Escudo de Vidro", "weight": 4, "value": 9, "image": "glassShield.png" },
  { "name": "Espada de Vidro", "weight": 4, "value": 9, "image": "glassSword.png" },
  { "name": "Escudo Nórdico", "weight": 4, "value": 9, "image": "nordicShield.png" }
]

class DungeonManager:
    def __init__(self, all_possible_items: list):
        self.possible_items = all_items

    def generate_loot(self, quantity: int = 3) -> list:
        loot = []
        for _ in range(quantity):
            item = random.choice(self.possible_items)
            loot.append(item)
        return loot

    def discard_overweight(self, current_backpack: list, loot: list, max_capacity: int) -> tuple[list, list, int]:
        """
        Recebe:
        - current_backpack: Lista de itens que já estavam na mochila.
        - loot: Lista de itens novos encontrados.
        - max_capacity: Peso máximo da mochila.
        
        Retorna:
        - kept_items: Itens que ficaram na mochila (Otimizados).
        - discarded_items: Itens que foram jogados fora.
        - total_value: Valor da nova mochila.
        """
        
        overcarry = current_backpack + loot
        
        # roda o knapsack novamente para ver a mochila com o maior valor entre os itens atuais + loot
        best_value, kept_items, _ = knapsack(overcarry, max_capacity)
        
        discarded_items = []
        kept_set = {json.dumps(item, sort_keys=True) for item in kept_items}
        
        # se ele tava na mochila e não está mais no kept_items, ele foi descartado
        for item in overcarry:
            item_key = json.dumps(item, sort_keys=True)
            if item_key not in kept_set:
                discarded_items.append(item)
                
        return kept_items, discarded_items, best_value
    
def parse_formatted_items(items: list):
    formatted = []
    for item in items:
        formatted.append(f"- {item['name']} (Peso: {item['weight']}, Valor: {item['value']})")
    return "\n".join(formatted)

if __name__ == "__main__":
    a = []
    dungeon = DungeonManager(a)
    loot = dungeon.generate_loot()
    mock_inventory, discarded_items, total_value = dungeon.discard_overweight(mock_inventory, loot, 15)
    
    loot_weight = 0
    
    for item in loot:
        loot_weight += item['weight']
    
    inventory_weight = 0
    for item in mock_inventory:
        inventory_weight += item['weight']
    
    print(f"\nMochila inicial 15/15:\n {parse_formatted_items(mock_inventory)}")
    print(f"\nLoot obtido:\n {parse_formatted_items(loot)}")
    print(f"\nMochila pós loot {inventory_weight + loot_weight}/15:\n {parse_formatted_items(mock_inventory + loot)}")
    print(f"\nLoot descartado:\n {parse_formatted_items(discarded_items)}")
    print(f"\nMochila final {inventory_weight}/15 (Valor total: {total_value}):\n {parse_formatted_items(mock_inventory)}\n")

