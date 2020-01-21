from pudb import set_trace
import requests
import json
from app import config

metabase_host = config.metabase_host
metabase_session = None

def refresh_metabase_session(f):
	def refresh():
		global metabase_session
		end_point = '/api/session/'
		result = requests.post(
				url = metabase_host + end_point,
				headers = {
					'Content-Type': 'application/json'
				},
				data = json.dumps({
					'username': config.metabase_username,
					'password': config.metabase_password
				})
			)
		metabase_session =  result.json()['id']
	def wrapper(*args, **kwargs):
		result = f(*args, **kwargs)
		if type(result) is requests.models.Response:
			if result.status_code == 401:
				refresh()
				result = f(*args, **kwargs)
		return result.json()
	return wrapper

class card():
	def __init__(self, card_id):
		self.end_point = '/api/card/' + str(card_id)
		self.id = card_id
		self.query = None

	@refresh_metabase_session
	def update_query(self, query):
		result = requests.put(
			url = metabase_host + self.end_point,
			headers = {
				'Content-Type': 'application/json',
				'X-Metabase-Session': metabase_session
			},
			data = json.dumps(
				{
					"name":"stupid_card",
					"dataset_query":{
						"type":"native",
						"native":{
							"query": query
						},
						"database":2
					}
				}
			)
		)
		return result
