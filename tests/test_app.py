import os
import pytest
from flask import Flask, session
from flask_testing import TestCase
from app import app, socketio

class TestApp(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SECRET_KEY'] = 'test_secret_key'
        app.config['DEBUG'] = False  # Set to True if you want more verbose output during testing
        return app

    def test_index_route_requires_login(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/google/login')

    def test_login_route_loads(self):
        response = self.client.get('/login')
        self.assert200(response)

    def test_register_route_loads(self):
        response = self.client.get('/register')
        self.assert200(response)

    def test_google_login_redirects_to_google(self):
        response = self.client.get('/google/login')
        self.assertRedirects(response, '/google/login')

    # Add more test cases as needed

if __name__ == '__main__':
    socketio.run(app, debug=True)
