import requests
import time
import random

class CryptoTradingSimulator:
    def __init__(self, starting_balance=1_000_000):
        self.balance = starting_balance  # Fake USD balance
        self.portfolio = {}  # Dictionary to store token holdings
        self.trade_history = []  # Record of all trades
        self.base_url = "https://api.coingecko.com/api/v3/simple/price"

    def get_token_price(self, token="ethereum"):
        """Fetch real-time token price from a testnet-compatible API."""
        try:
            response = requests.get(f"{self.base_url}?ids={token}&vs_currencies=usd")
            data = response.json()
            return data[token]["usd"]
        except Exception as e:
            print(f"Error fetching token price: {e}")
            return None

    def execute_trade(self, model_output, token="ethereum"):
        """Executes Buy/Sell based on ML model's prediction (-1 = Sell, 1 = Buy, 0 = Hold)."""
        price = self.get_token_price(token)
        if not price:
            print("Skipping trade due to price fetch error.")
            return
        
        action = "Hold"
        if model_output == 1:  # Buy
            amount = self.balance * 0.1 / price  # Buy 10% of balance
            self.balance -= amount * price
            self.portfolio[token] = self.portfolio.get(token, 0) + amount
            action = "Buy"
        elif model_output == -1 and token in self.portfolio:  # Sell
            amount = self.portfolio[token] * 0.1  # Sell 50% of holdings
            self.balance += amount * price
            self.portfolio[token] -= amount
            action = "Sell"
        
        self.trade_history.append({"token": token, "action": action, "price": price, "balance": self.balance})
        print(f"{action} {token} at ${price:.2f}. New balance: ${self.balance:.2f}")

    def run_simulation(self, model_predictions):
        """Runs a simulated trading loop based on ML predictions."""
        for prediction in model_predictions:
            self.execute_trade(prediction)
            time.sleep(2)  # Simulate trade delay

    def print_portfolio(self):
        """Prints the current portfolio and balance."""
        print("\n--- Portfolio Summary ---")
        print(f"Balance: ${self.balance:.2f}")
        for token, amount in self.portfolio.items():
            print(f"{token}: {amount:.4f}")
        print("-------------------------")

# Example Usage
if __name__ == "__main__":
    simulator = CryptoTradingSimulator()
    model_predictions = [1, 0, -1, 1, 1, -1, 0]  # Replace with your real ML model outputs
    simulator.run_simulation(model_predictions)
    simulator.print_portfolio()
