import requests
"""
A client for making HTTP requests to REST APIs.
This class provides a simple interface for making HTTP requests using the requests library.
It supports common HTTP methods (GET, POST, PUT, DELETE) and handles JSON data.
Attributes:
    base_url (str): The base URL of the API endpoint
    session (requests.Session): A session object to maintain parameters across requests
Usage:
    >>> api = APIClient('https://api.example.com')
    >>> response = api.get('users')
    >>> new_user = api.post('users', {'name': 'John'})
Methods:
    get(endpoint, params=None): Send a GET request to the specified endpoint
    post(endpoint, data): Send a POST request with JSON data
    put(endpoint, data): Send a PUT request with JSON data
    delete(endpoint): Send a DELETE request
Dependencies:
    - requests
    - json
Example:
    new_post = {'title': 'New Post', 'body': 'Content', 'userId': 1}
"""
import json

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def get(self, endpoint, params=None):
        """Send GET request"""
        url = f"{self.base_url}/{endpoint}"
        response = self.session.get(url, params=params)
        return response.json()

    def post(self, endpoint, data):
        """Send POST request"""
        url = f"{self.base_url}/{endpoint}"
        response = self.session.post(url, json=data)
        return response.json()

    def put(self, endpoint, data):
        """Send PUT request"""
        url = f"{self.base_url}/{endpoint}"
        response = self.session.put(url, json=data)
        return response.json()

    def delete(self, endpoint):
        """Send DELETE request"""
        url = f"{self.base_url}/{endpoint}"
        response = self.session.delete(url)
        return response.status_code

def main():
    # Example usage with JSONPlaceholder API
    api = APIClient('https://jsonplaceholder.typicode.com')

    # GET example
    posts = api.get('posts')
    print("GET Posts:", posts[:2])

    # POST example
    new_post = {
        'title': 'New Post',
        'body': 'This is a new post',
        'userId': 1
    }
    created_post = api.post('posts', new_post)
    print("\nPOST Result:", created_post)

    # PUT example
    updated_post = {
        'id': 1,
        'title': 'Updated Post',
        'body': 'This post has been updated',
        'userId': 1
    }
    updated = api.put('posts/1', updated_post)
    print("\nPUT Result:", updated)

    # DELETE example
    delete_status = api.delete('posts/1')
    print("\nDELETE Status:", delete_status)

if __name__ == "__main__":
    main()