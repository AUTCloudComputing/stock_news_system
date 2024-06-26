import re
import sys
import argparse
from flask import Flask, render_template
from api.financial_data import EODHDAPIsDataFetcher
from config import API_TOKEN


parser = argparse.ArgumentParser(description="EODHD APIs")
parser.add_argument(
    "--host",
    type=str,
    help="Web service IP (default: 127.0.0.1)",
)
parser.add_argument(
    "--port",
    type=int,
    help="Web service port (default: 5000)",
)
parser.add_argument("--debug", action="store_true", help="Enable debugging")
args = parser.parse_args()


# Listen on local host
http_host = "0.0.0.0"
if args.host is not None:
    p = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    if p.match(args.host):
        http_host = args.host
    else:
        parser.print_help(sys.stderr)

# Listen on local port
http_port = 5000
if args.port is not None:
    if args.port >= 0 and args.port <= 65535:
        http_port = args.port
    else:
        parser.print_help(sys.stderr)


app = Flask(__name__)

data_fetcher = EODHDAPIsDataFetcher(API_TOKEN)


# @app.route("/")
# def exchanges():
#     exchanges = data_fetcher.fetch_exchanges()
#     return render_template("exchanges.html", exchanges=exchanges)


@app.route("/")
def exchanges():
    exchanges = data_fetcher.fetch_news()
    return render_template("news.html", exchanges=exchanges)


@app.route("/exchange/<code>")
def exchange_markets(code):
    markets = data_fetcher.fetch_exchange_markets(code)
    return render_template("markets.html", code=code, markets=markets)


@app.route("/exchange/<code>/<market>/<granularity>")
def exchange_market_data(code, market, granularity):
    candles = data_fetcher.fetch_exchange_market_data(code, market, granularity)
    return render_template("data.html", code=code, market=market, granularity=granularity, candles=candles)


if __name__ == "__main__":
    app.run(host=http_host, port=http_port, debug=args.debug)
    # app.run(debug=True)
