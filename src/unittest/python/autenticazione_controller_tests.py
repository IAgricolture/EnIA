import os
import sys
from unittest import mock
import unittest

import jinja2
sys.path.append(os.path.abspath(os.path.join('.' )))
from flask import request, redirect, render_template
from src.logic.Autenticazione.AutenticazioneService import AutenticazioneService
from src import app
    
class TestLogin(unittest.TestCase):
            
    def setUp(self):
        self.app = app.test_client()
 
    def test_login_success(self):
        with mock.patch('src.logic.Autenticazione.AutenticazioneService.AutenticazioneService.login') as mock_login:
            # Configurare il mock per restituire True quando viene chiamato login()
            mock_login.return_value = True

            # Inviare una richiesta POST al metodo login() con i dati di login necessari
            response = self.app.post("/login", data={"email": "prova@gmail.com", "password": "password", "next": "visualizzaTerreni"})

            # Verificare che la risposta sia un redirect alla pagina visualizzaTerreni
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, "visualizzaTerreni")
    
    def test_logout_success(self):
        with mock.patch('src.logic.Autenticazione.AutenticazioneService.AutenticazioneService.logout') as mock_logout:
            # Configurare il mock per non restituire alcun valore quando viene chiamato logout()
            mock_logout.return_value = None
                
            # Inviare una richiesta GET al metodo logout()
            response = self.app.get("/logout")
                
            # Verificare che la risposta sia un redirect alla pagina di login
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, "/login")
    
    def test_login_failure(self):
        with mock.patch('src.logic.Autenticazione.AutenticazioneService.AutenticazioneService.login') as mock_login:
            # Configurare il mock per restituire False quando viene chiamato login()
            mock_login.return_value = False

            # Inviare una richiesta POST al metodo login() con i dati di login necessari
            response = self.app.post("/login", data={"email": "prova@gmail.com", "password": "password", "next": "visualizzaTerreni"})
            self.assertEqual(response.status_code, 200)
            

if __name__ == '__main__':
        test = TestLogin()
        test.setUp()
        test.test_login_success()