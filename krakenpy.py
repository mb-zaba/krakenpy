# -*- coding: utf-8 -*-
# @Author: mb-zaba
# @Date:   2021-02-19 15:54:59
# @Last modified by:   zaba
# @Last modified time: 2021-07-14T13:57:52+02:00
# @Version: 1.0

import pandas as pd
import requests
from dotenv import load_dotenv
import time
import urllib.parse
import hashlib
import hmac
import base64

class Krakenpy:

	def __init__(self, api_key=None, api_sec=None):
		self.api_url = "https://api.kraken.com/0"
		self.api_key = api_key
		self.api_sec = api_sec
		self.public = self.Public(self.api_url)
		self.private = self.Private(self.api_key, self.api_url, self.api_sec)



	class Public:

		def __init__(self, api_url):
			self.api_url = api_url


		# Gets server time from the Kraken API
		def get_server_time(self):
			endpoint = f"{self.api_url}/public/Time"
			r = requests.get(endpoint)
			data = r.json()
			if len(data['error']) < 1:
				server_time = data['result']['rfc1123']
				return server_time
			else:
				print(f"Error: {data['error']}")



		# Gets informations about the specified assets (all if none is specified)
		def get_asset_info(self, assets=None):
			endpoint = f"{self.api_url}/public/Assets"
			if assets == None:
				r = requests.get(endpoint)
			else:
				data = {"":",".join(assets)}
				r = requests.post(endpoint, data=data)
			data = r.json()
			if len(data['error']) < 1:
				#pd.set_option('display.max_rows', None)
				#assets = pd.DataFrame(data['result'])
				assets = data['result']
				return assets
			else:
				print(f"Error: {data['error']}")



		# Gets informations about an asset pair
		def get_asset_pairs(self, pairs=None):
			endpoint = f"{self.api_url}/public/AssetPairs"
			if pairs == None:
				r = requests.get(endpoint)
			else:
				r = requests.post(endpoint, data={'pair':",".join(pairs)})
			data = r.json()
			if len(data['error']) < 1:
				pd.set_option('display.max_rows', None)
				assets = pd.DataFrame(data['result'])
				return assets
			else:
				print(f"Error: {data['error']}")



		# Get Ticker
		def get_ticker(self, pairs):
			endpoint = f"{self.api_url}/public/Ticker"
			r = requests.post(endpoint, data={'pair':",".join(pairs)})
			data = r.json()
			if len(data['error']) < 1:
				#pd.set_option('display.max_rows', None)
				#assets = pd.DataFrame(data['result'])
				assets = data['result']
				return assets
			else:
				print(f"Error: {data['error']}")



		# Get OHLC
		def get_ohlc(self, pair, interval=1, since=None):
			endpoint = f"{self.api_url}/public/OHLC"
			if since == None:
				r = requests.post(endpoint, data={'pair':pair, 'interval':interval})
			else:
				r = requests.post(endpoint, data={'pair':pair, 'interval':interval, 'since':since})
			data = r.json()
			data_struct = {
				"time": [],
				"open": [],
				"high": [],
				"low": [],
				"close": [],
				"vwap": [],
				"volume": [],
				"count": []
			}
			if len(data['error']) < 1:
				for ohlc_data in data['result']:
					if type(data['result'][ohlc_data]) == type([]):
						ohlc_data = data['result'][ohlc_data]
						break

				for row in ohlc_data:
					i = 0
					for entry in data_struct:
						data_struct[entry].append(row[i])
						i += 1
				data_struct['pair'] = pair
				#df = pd.DataFrame(data_struct)
				return data_struct
			else:
				print(f"Error: {data['error']}")



		def get_order_book(self, pair):
			endpoint = f"{self.api_url}/public/Depth"
			r = requests.post(endpoint, data={'pair':pair})
			data = r.json()
			if len(data['error']) < 1:
				return data['result']
			else:
				print(f"Error: {data['error']}")



		def get_recent_trades(self, pair):
			endpoint = f"{self.api_url}/public/Trades"
			r = requests.post(endpoint, data={'pair':pair})
			data = r.json()
			data_struct = {
				"price": [],
				"volume": [],
				"time": [],
				"buy/sell": [],
				"market/limit": [],
				"miscellaneous": []
			}
			if len(data['error']) < 1:
				if len(data['error']) < 1:
					for trade_data in data['result']:
						if type(data['result'][trade_data]) == type([]):
							trade_data = data['result'][trade_data]
							break

					for row in trade_data:
						i = 0
						for entry in data_struct:
							data_struct[entry].append(row[i])
							i += 1

				data_struct['pair'] = pair
				#data_struct = pd.DataFrame(data_struct)
				return data_struct
			else:
				print(f"Error: {data['error']}")


		def get_recent_spread(self, pair):
			endpoint = f"{self.api_url}/public/Spread"
			r = requests.post(endpoint, data={'pair':pair})
			data = r.json()
			data_struct = {
				"time": [],
				"bid": [],
				"ask": []
			}
			if len(data['error']) < 1:
				if len(data['error']) < 1:
					for spread_data in data['result']:
						if type(data['result'][spread_data]) == type([]):
							spread_data = data['result'][spread_data]
							break

					for row in spread_data:
						i = 0
						for entry in data_struct:
							data_struct[entry].append(row[i])
							i += 1

				data_struct['pair'] = pair
				return data_struct
			else:
				print(f"Error: {data['error']}")



	class Private:

		def __init__(self, api_key, api_url, api_sec):
			self.api_key = api_key
			self.api_sec = api_sec
			self.api_url = api_url



		def get_api_sign(self, URI_Path, payload):
			# HMAC-SH512(URI_Path + SHA256(nonce + POST data)) and base64 decoded secret API key
			postdata = urllib.parse.urlencode(payload)
			encoded = (str(payload["nonce"]) + postdata).encode()
			hashed_payload = URI_Path.encode() + hashlib.sha256(encoded).digest()

			api_sign = base64.b64encode(hmac.new(base64.b64decode(self.api_sec), hashed_payload, hashlib.sha512).digest())
			return api_sign


		def get_account_balance(self):
			data = {
			"nonce": str(int(time.time()*1000))
			}
			headers = {}
			headers["API-Sign"] = self.get_api_sign("/0/private/Balance", data)
			headers["API-Key"] = self.api_key
			endpoint = f"{self.api_url}/private/Balance"
			r = requests.post(endpoint, headers=headers, data=data)
			data = r.json()
			if len(data['error']) < 1:
				if len(data['error']) < 1:
					return data["result"]
			else:
				print(f"Error: {data['error']}")
