"""Aggreagte holdings by inputs"""

from collections import OrderedDict


class ETFAggregation:
    def __init__(self, holdings_data):
        """
        Initialize the ETFAggregation class with the ETF holdings data.

        :param holdings_data: Dictionary containing ETF data with holdings informations
        """
        self.holdings_data = holdings_data
        self.aggregated_holdings = {}

    def aggregate_holdings(self):
        """
        Aggregates the holdings data by company symbol and sums their holding percentages.
        """
        for etf, data in self.holdings_data.items():
            if isinstance(data, dict) and "holdings" in data:
                for holding in data["holdings"]:
                    company_symbol = holding["symbol"]
                    company_name = holding["holdingName"]
                    holding_percent = holding["holdingPercent"]

                    if company_symbol in self.aggregated_holdings:
                        self.aggregated_holdings[company_symbol]["totalPercent"] += (
                            holding_percent
                        )
                    else:
                        self.aggregated_holdings[company_symbol] = {
                            "companyName": company_name,
                            "totalPercent": holding_percent,
                        }

    def normalize_percentages(self):
        """
        Normalizes the total percentage to 100% and calculates the relative percentages for each company.

        :return: A dictionary with company names as keys and their normalized percentages as values
        """
        total_percentage = sum(
            [item["totalPercent"] for item in self.aggregated_holdings.values()]
        )

        normalized_result = {}
        for company in self.aggregated_holdings.values():
            company["normalizedPercent"] = (
                company["totalPercent"] / total_percentage * 100
            )
            normalized_result[company["companyName"]] = company["normalizedPercent"]

        # Sort the result in descending order by normalized percentage
        sorted_result = OrderedDict(
            sorted(normalized_result.items(), key=lambda x: x[1], reverse=True)
        )

        return sorted_result

    def process(self):
        """
        Aggregates the holdings and normalizes the percentages, then returns the sorted results.

        :return: Sorted dictionary of companies with their normalized holding percentages
        """
        self.aggregate_holdings()
        return self.normalize_percentages()
