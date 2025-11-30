def knapsack(items, max_weight):
    n = len(items)

    # DP[i][w] = melhor valor usando itens até i com peso máximo w
    dp = [[0] * (max_weight + 1) for _ in range(n + 1)]

    # Computando a tabela
    for i in range(1, n + 1):
        item_weight = items[i-1]["weight"]
        item_value = items[i-1]["value"]

        for w in range(max_weight + 1):
            if item_weight <= w:
                dp[i][w] = max(
                    dp[i-1][w],                     # não usar item
                    dp[i-1][w - item_weight] + item_value  # usar item
                )
            else:
                dp[i][w] = dp[i-1][w]

    # Reconstrução dos itens usados
    chosen = []
    w = max_weight

    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            chosen.append(items[i-1])
            w -= items[i-1]["weight"]

    return dp[n][max_weight], chosen[::-1], dp
