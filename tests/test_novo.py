from views_filme import *

import os
import tempfile
import unittest
from flask import Flask
from flask_testing import TestCase
from filmesvideo import app, db
from models import Filmes

class TestFilmes(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_criar_filme(self):
        response = self.client.get('/novo')
        self.assertEqual(response.status_code, 302)  # Redirecionamento para a página de login

        # Supondo que você tenha uma rota '/login', você precisará adicionar mais lógica para fazer login no teste.

        # Mock data
        data = {
            'nome': 'Filme Teste',
            'categoria': 'Ação',
            'streaming': 'Netflix',
            # Adicione outros campos conforme necessário
        }

        # Suponha que você tenha uma rota '/login' para fazer login antes de criar o filme
        self.client.post('/login', data={'username': 'seu_usuario', 'password': 'sua_senha'})

        # Enviar dados do filme
        response = self.client.post('/criar', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)  # Verificar se o filme foi criado com sucesso

        # Verificar se o filme está na lista
        filmes = Filmes.query.all()
        self.assertEqual(len(filmes), 1)
        self.assertEqual(filmes[0].nome, 'Filme Teste')

if __name__ == '__main__':
    unittest.main()
