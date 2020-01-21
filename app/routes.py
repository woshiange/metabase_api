from pudb import set_trace
from app import app
from app import models
import flask
import json

@app.route('/update/card/<card_id>', methods=['POST'])
def update_card(card_id):
	query = flask.request.args.get("query")
	set_trace()
	models.card(card_id).update_query(query)
	return json.dumps(query) 
