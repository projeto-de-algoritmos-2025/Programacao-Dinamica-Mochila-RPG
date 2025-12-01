def calculate_item_score(item, race_key):
    """
    Calcula o valor de utilidade baseado na raça.
    Acrescenta influência do value original para evitar escolhas estranhas.
    """
    stats = item.get("stats", {"attack": 0, "defense": 0})
    base_value = item.get("value", 0)
    name = item.get("name", "").lower()
    item_type = item.get("type", "")
    
    score = 0
    
    if race_key == "orc":
        # Orcs => preferência forte por dano corpo-a-corpo (espadas)
        # base ponderada por ataque 
        score = (stats.get("attack", 0) * 6) + (stats.get("defense", 0) * 1)
        # dar um bônus maior para espadas (preferência clara por melee)
        if "espada" in name or "sword" in name:
            score += 90
        # penaliza arcos para orcs
        if "arco" in name or "bow" in name:
            score -= 90
        # incluir parte do valor base, mas com peso menor para não sobrepor os stats
        score += base_value * 0.1
            
    elif race_key == "nord":
        score = (stats.get("defense", 0) * 4) + (stats.get("attack", 0) * 1)
        if "escudo" in name or "nordico" in name or "nórdico" in name:
            score += 25
        if "espada" in name:
            score += 20
        score += base_value * 0.15
            
    elif race_key == "wood_elf":
        if "arco" in name:
            score = base_value + 60 + (stats.get("attack", 0) * 3)
        else:
            score = base_value * 0.4 
            
    elif race_key == "khajiit":
        score = base_value * 2 
        
    elif race_key == "imperial":
        score = base_value + stats.get("attack", 0) + stats.get("defense", 0)

    # Poções sempre são úteis independentemente da raça
    if item_type == "consumable" or "poção" in name:
        score += 15

    # Garantir não-negatividade e inteiro para o knapsack
    final = max(int(score), 0)
    return final

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