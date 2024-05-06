# api/financial_data.py
import json
from eodhd import APIClient
import openai
from openai import OpenAI
from flask import Flask, redirect, render_template, request, url_for
from config import OPENAI_KEY

client = OpenAI(api_key=OPENAI_KEY)


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
            news_list = api.financial_news(from_date="2022-12-10", to_date="2023-04-10", t="financial results",
                                           offset="200", limit="1")

            df_with_summary = []
            for news in news_list:
                news_with_summary = self.fetch_summary_news(news)
                df_with_summary.append(news_with_summary)

            return df_with_summary

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

    def generate_news_prompt(self, news):
        prompt = f"Summarize the following news article titled '{news['title']}' with content limited to 100 words, \
                   in approximately four to five points. Also, give credits to {news['link']}\n\
                   The detailed article: {news['content']}"
        return prompt

    def fetch_summary_news(self, news):
        try:
            # Call to the OpenAI API
            prompt = self.generate_news_prompt(news)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6
            )
            summary = response.choices[0].message.content
            news['summary'] = summary  # Add the summary to the news dictionary
            return news

        except Exception as e:
            print(f"An error occurred: {e}")
            news['summary'] = "Failed to fetch summary."
            return news


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
