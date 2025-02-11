"""Get the Ticker's holdings"""

from yahooquery import Ticker


class ETFHoldings:
    def __init__(self, symbol):
        """Initialize with the ETF symbol."""
        self.symbol = symbol.upper().strip()

    def get_holdings(self):
        """Fetch and return ETF holdings."""
        ticker = Ticker(self.symbol)
        data = ticker.fund_holding_info
        # Check if data exists
        if self.symbol in data and "holdings" in data[self.symbol]:
            return {"symbol": self.symbol, "holdings": data[self.symbol]["holdings"]}
        return {"error": f"No holdings data found for {self.symbol}"}
