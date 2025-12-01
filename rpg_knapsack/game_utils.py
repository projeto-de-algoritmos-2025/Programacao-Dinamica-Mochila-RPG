def calculate_item_score(item, race_key):
    """
    Calcula o valor de utilidade baseado na raça.
    """
    stats = item.get("stats", {"attack": 0, "defense": 0})
    base_value = item.get("value", 0)
    name = item.get("name", "").lower()
    item_type = item.get("type", "")
    
    score = 0
    
    if race_key == "orc":
        # Orcs => dano bruto e armas corpo a corpo 
        score = (stats.get("attack", 0) * 4) + (stats.get("defense", 0) * 1)
        if "espada" in name: 
            score += 30  
        if "escudo" in name:
            score += 20  
            
    elif race_key == "nord":
        # Nords => +resistentes e usam escudos
        score = (stats.get("defense", 0) * 4) + (stats.get("attack", 0) * 1)
        if "escudo" in name or "nordico" in name or "nórdico" in name:
            score += 25  # Grande preferência cultural
        if "espada" in name:
            score += 20
            
    elif race_key == "wood_elf":
        # Bosmer são os melhores arqueiros
        if "arco" in name:
            score = base_value + 50 + (stats.get("attack", 0) * 3)
        else:
            # Desvalorizam itens pesados que não sejam arcos
            score = base_value * 0.5 
            
    elif race_key == "khajiit":
        # Khajiit tem mercadorias se você tem moedas. Só importa o ouro.
        score = base_value * 2 
        
    elif race_key == "imperial":
        # Imperiais são equilibrados => meh
        score = base_value + stats.get("attack", 0) + stats.get("defense", 0)

    # Poções sempre são úteis, independentemente da raça
    if item_type == "consumable" or "poção" in name:
        score += 15

    # int pro Knapsack não quebrar
    return int(score)

def prepare_items_for_knapsack(items, race_key):
    """
    Processa os itens aplicando a 'visão' da raça sobre o valor deles.
    """
    processed_items = []
    for item in items:
        new_item = item.copy()
        # Salva o valor original e define o 'value' como o Score calculado
        new_item["real_value"] = item["value"] 
        new_item["value"] = calculate_item_score(item, race_key)
        
        # Adiciona uma tag pra mostrar que o item é "favorito" da raça
        if new_item["value"] > item["value"] * 2: # Se o score for muito alto
            new_item["is_favorite"] = True
            
        processed_items.append(new_item)
    return processed_items