# Import required libraries
import requests, json

# Define the base URL for the API
base_url = 'http://example.com/api'

# Function to create a new item
def create_item(data):
	response = requests.post('{}/items'.format(base_url), json=data)
	return response.json()

# Function to get all items
def get_all_items():
	response = requests.get('{}/items'.format(base_url))
	return response.json()

# Function to get an individual item by ID
def get_item(item_id):
	response = requests.get('{}/items/{}'.format(base_url, item_id))
	return response.json()

# Function to update an existing item
def update_item(item_id, data):
	response = requests.put('{}/items/{}'.format(base_url, item_id), json=data)
	return response.json()

# Function to delete an existing item by ID
def delete_item(item_id):
	response = requests.delete('{}/items/{}'.format(base_url, item_id))
	if response.status_code == 204:
		return None
	else:
		return response.json()