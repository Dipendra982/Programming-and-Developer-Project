def maxProfit(max_trades, daily_prices):
    n = len(daily_prices)
    if n == 0 or max_trades == 0:
        return 0

    if max_trades >= n // 2:
        profit = 0
        for i in range(1, n):
            if daily_prices[i] > daily_prices[i - 1]:
                profit += daily_prices[i] - daily_prices[i - 1]
        return profit

    dp = [[0] * n for _ in range(max_trades + 1)]

    for t in range(1, max_trades + 1):
        max_diff = -daily_prices[0]
        for i in range(1, n):
            dp[t][i] = max(dp[t][i - 1], daily_prices[i] + max_diff)
            max_diff = max(max_diff, dp[t - 1][i] - daily_prices[i])

    return dp[max_trades][n - 1]


if __name__ == "__main__":
    prices = [3, 2, 6, 5, 0, 3]
    k = 2

    print("Maximum Profit:", maxProfit(k, prices))