# api/financial_data.py

import json
from eodhd import APIClient


class EODHDAPIsDataFetcher:
    def __init__(self, api_token):
        self._api_token = api_token

    def fetch_exchanges(self):
        try:
            api = APIClient(self._api_token)
            df = api.get_exchanges()
            return json.loads(df.to_json(orient="records"))

        except Exception as e:
            print(f"Error fetching data: {e}")
            return None

    def fetch_news(self):
        try:
            api = APIClient(self._api_token)
            df = api.financial_news(from_date="2022-12-10", to_date="2023-04-10", t="financial results",
                                               offset="200", limit="100")
            return df

        except Exception as e:
            print(f"Error fetching data: {e}")
            return None

    def fetch_exchange_markets(self, code: str = ""):
        try:
            api = APIClient(self._api_token)
            df = api.get_exchange_symbols(code)
            return json.loads(df.to_json(orient="records"))

        except Exception as e:
            print(f"Error fetching data: {e}")
            return None

    def fetch_exchange_market_data(self, code: str = "", market: str = "", granularity: str = ""):
        try:
            api = APIClient(self._api_token)
            df = api.get_historical_data(f"{market}.{code}", granularity)
            df["datetime"] = df.index.astype(str)
            print(df)
            return json.loads(df.to_json(orient="records"))

        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
