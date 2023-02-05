import unittest
import os, sys
from flask import jsonify
from flask_login import current_user

import requests







sys.path.append(os.path.abspath(os.path.join('.' )))
from unittest.mock import patch
from src import app
from src.logic.Storage.TerrenoDAO import TerrenoDAO
from src.logic.AmbienteAgricolo.AmbienteAgricoloService import AmbienteAgricoloService


class AmbienteAgricoloControllerTests(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        #fai il login con ruolo "Farmer"
        self.app.post("/login", data={"email": "prova@gmail.com", "password": "password", "next": "visualizzaTerreni"})
        
    @patch('src.logic.AmbienteAgricolo.AmbienteAgricoloService.AmbienteAgricoloService.aggiungiTerreno')
    def test_aggiungiTerreno_post(self, mock_aggiungiTerreno):
        with self.app:
            self.app.post("/login", data={"email": "prova@gmail.com", "password": "password", "next": "visualizzaTerreni"})
            # Impostare il valore di ritorno di mock_aggiungiTerreno
            mock_aggiungiTerreno.return_value = {'esitoOperazione': True}
            
            # Inviare una richiesta POST con i dati di esempio
            url = 'http://localhost:5000/aggiuntaTerreno'
            data = {
                "nome": "Example Name",
                "coltura": "Example Crop",
                "posizione": "Example Position",
                "preferito": True,
                "priorita": 1,
                "stadio_crescita": "Example Stage"
            }

            response = self.app.post("/aggiuntaTerreno", json=data)
            # Verificare che AmbienteAgricoloService.aggiungiTerreno sia stato chiamato con i parametri corretti
            mock_aggiungiTerreno.assert_called_with(
                'Example Name', 'Example Crop', 'Example Stage',
                'Example Position', True, 1, current_user.id
            )
            # Verificare che la risposta sia corretta
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'TerrenoAggiunto': True})

    @patch('src.logic.AmbienteAgricolo.AmbienteAgricoloService.AmbienteAgricoloService.trovaTerreno')
    @patch('src.logic.AmbienteAgricolo.AmbienteAgricoloService.AmbienteAgricoloService.cercaPosizione')
    @patch('src.logic.AmbienteAgricolo.AmbienteAgricoloService.AmbienteAgricoloService.cercaInquinamento')
    @patch('src.logic.AmbienteAgricolo.AmbienteAgricoloService.AmbienteAgricoloService.cercalat')
    @patch('src.logic.AmbienteAgricolo.AmbienteAgricoloService.AmbienteAgricoloService.cercalon')
    @patch('src.logic.AmbienteAgricolo.AmbienteAgricoloService.AmbienteAgricoloService.cercaMeteo')
    def test_dettagli(self, mock_cercaMeteo, mock_cercalon, mock_cercalat, mock_cercaInquinamento, mock_cercaPosizione, mock_trovaTerreno):
        with self.app:
            self.app.post("/login", data={"email": "prova@gmail.com", "password": "password", "next": "visualizzaTerreni"})
            # Definire i dati di test per i mock
            terreno = {'id': 1, 'nome': 'Terreno 1', 'coltura': 'Pomodori', 'stadio_crescita': 'Semina', 'posizione': 'Latitudine: 40.730610, Longitudine: -73.935242', 'preferito': False, 'priorita': 1, 'proprietario': 1}
            posizione = {'lat': '40.730610', 'lon': '-73.935242', 'address': {'town': 'New York', 'county': 'New York County', 'state': 'New York', 'country': 'United States of America'}}
            inquinamento = {'value': 10.0, 'unit': 'µg/m³'}
            lat = '40.730610'
            lon = '-73.935242'
            meteo = {'temperature': '20.0', 'humidity': '50.0', 'wind_speed': '5.0', 'wind_direction': 'N'}
            
            # Configurare i mock per restituire i dati di test
            mock_trovaTerreno.return_value = terreno
            mock_cercaPosizione.return_value = posizione
            mock_cercaInquinamento.return_value = inquinamento
            mock_cercalat.return_value = lat
            mock_cercalon.return_value = lon
            mock_cercaMeteo.return_value = meteo
            print(AmbienteAgricoloService.trovaTerreno(1))
            # Invocare la funzione dettagli con una richiesta GET
            response = self.app.get('/dettagliterreno?idTerreno=1')

            # Verificare che la risposta sia corretta
            #verificare che la risposta sia corretta
            self.assertEqual(response.status_code, 200)
            
    @patch('src.logic.AmbienteAgricolo.AmbienteAgricoloService.AmbienteAgricoloService.trovaTerreno')
    @patch('src.logic.AmbienteAgricolo.AmbienteAgricoloService.AmbienteAgricoloService.cercaPosizione')
    @patch('src.logic.AmbienteAgricolo.AmbienteAgricoloService.AmbienteAgricoloService.cercaInquinamento')
    @patch('src.logic.AmbienteAgricolo.AmbienteAgricoloService.AmbienteAgricoloService.cercalat')
    @patch('src.logic.AmbienteAgricolo.AmbienteAgricoloService.AmbienteAgricoloService.cercalon')
    @patch('src.logic.AmbienteAgricolo.AmbienteAgricoloService.AmbienteAgricoloService.cercaMeteo')
    def test_dettagli_key_error(self, mock_cercaMeteo, mock_cercalon, mock_cercalat, mock_cercaInquinamento, mock_cercaPosizione, mock_trovaTerreno):
        with self.app:
            self.app.post("/login", data={"email": "prova@gmail.com", "password": "password", "next": "visualizzaTerreni"})
            # Definire i dati di test per i mock
            terreno = {'id': 1, 'nome': 'Terreno 1', 'coltura': 'Pomodori', 'stadio_crescita': 'Semina', 'posizione': 'Latitudine: 40.730610, Longitudine: -73.935242', 'preferito': False, 'priorita': 1, 'proprietario': 1}
            posizione = {'lat': '40.730610', 'lon': '-73.935242', 'address': {'town': 'New York', 'county': 'New York County', 'state': 'New York', 'country': 'United States of America'}}
            inquinamento = {'value': 10.0, 'unit': 'µg/m³'}
            lat = '40.730610'
            lon = '-73.935242'
            meteo = {'temperature': '20.0', 'humidity': '50.0', 'wind_speed': '5.0', 'wind_direction': 'N'}
            
            # Configurare i mock per restituire i dati di test
            mock_trovaTerreno.return_value = terreno
            mock_cercaPosizione.return_value = posizione
            mock_cercaInquinamento.return_value = inquinamento
            mock_cercalat.return_value = lat
            mock_cercalon.return_value = lon
            mock_cercaMeteo.return_value = meteo
            print(AmbienteAgricoloService.trovaTerreno(1))
            # Invocare la funzione dettagli con una richiesta GET
            response = self.app.get('/dettagliterreno?idTerreno=1')

            # Verificare che la risposta sia corretta
            #verificare che la risposta sia corretta
            self.assertEqual(response.status_code, 200)
            #controlla che sia stata lanciata l'eccezione KeyError
            self.assertRaises(KeyError)
            
    @patch('src.logic.AmbienteAgricolo.AmbienteAgricoloService.AmbienteAgricoloService.trovaTerreno')
    @patch('src.logic.AmbienteAgricolo.AmbienteAgricoloService.AmbienteAgricoloService.cercaPosizione')
    @patch('src.logic.AmbienteAgricolo.AmbienteAgricoloService.AmbienteAgricoloService.cercaInquinamento')
    @patch('src.logic.AmbienteAgricolo.AmbienteAgricoloService.AmbienteAgricoloService.cercalat')
    @patch('src.logic.AmbienteAgricolo.AmbienteAgricoloService.AmbienteAgricoloService.cercalon')
    @patch('src.logic.AmbienteAgricolo.AmbienteAgricoloService.AmbienteAgricoloService.cercaMeteo')
    def test_dettagli_city_in_address(self, mock_cercaMeteo, mock_cercalon, mock_cercalat, mock_cercaInquinamento, mock_cercaPosizione, mock_trovaTerreno):
        with self.app:
            self.app.post("/login", data={"email": "prova@gmail.com", "password": "password", "next": "visualizzaTerreni"})
            # Definire i dati di test per i mock
            terreno = {'id': 1, 'nome': 'Terreno 1', 'coltura': 'Pomodori', 'stadio_crescita': 'Semina', 'posizione': 'Latitudine: 40.730610, Longitudine: -73.935242', 'preferito': False, 'priorita': 1, 'proprietario': 1}
            posizione = {'lat': '40.730610', 'lon': '-73.935242', 'address': {'city': 'New York', 'county': 'New York County', 'state': 'New York', 'country': 'United States of America'}}
            inquinamento = {'value': 10.0, 'unit': 'µg/m³'}
            lat = '40.730610'
            lon = '-73.935242'
            meteo = {'temperature': '20.0', 'humidity': '50.0', 'wind_speed': '5.0', 'wind_direction': 'N'}
            
            # Configurare i mock per restituire i dati di test
            mock_trovaTerreno.return_value = terreno
            mock_cercaPosizione.return_value = posizione
            mock_cercaInquinamento.return_value = inquinamento
            mock_cercalat.return_value = lat
            mock_cercalon.return_value = lon
            mock_cercaMeteo.return_value = meteo
            print(AmbienteAgricoloService.trovaTerreno(1))
            # Invocare la funzione dettagli con una richiesta GET
            response = self.app.get('/dettagliterreno?idTerreno=1')

            # Verificare che la risposta sia corretta
            #verificare che la risposta sia corretta
            self.assertEqual(response.status_code, 200)
            
    @patch('src.logic.AmbienteAgricolo.AmbienteAgricoloService.AmbienteAgricoloService.trovaTerreno')
    @patch('src.logic.AmbienteAgricolo.AmbienteAgricoloService.AmbienteAgricoloService.cercaPosizione')
    @patch('src.logic.AmbienteAgricolo.AmbienteAgricoloService.AmbienteAgricoloService.cercaInquinamento')
    @patch('src.logic.AmbienteAgricolo.AmbienteAgricoloService.AmbienteAgricoloService.cercalat')
    @patch('src.logic.AmbienteAgricolo.AmbienteAgricoloService.AmbienteAgricoloService.cercalon')
    @patch('src.logic.AmbienteAgricolo.AmbienteAgricoloService.AmbienteAgricoloService.cercaMeteo')
    def test_dettagli_village_in_address(self, mock_cercaMeteo, mock_cercalon, mock_cercalat, mock_cercaInquinamento, mock_cercaPosizione, mock_trovaTerreno):
        with self.app:
            self.app.post("/login", data={"email": "prova@gmail.com", "password": "password", "next": "visualizzaTerreni"})
            # Definire i dati di test per i mock
            terreno = {'id': 1, 'nome': 'Terreno 1', 'coltura': 'Pomodori', 'stadio_crescita': 'Semina', 'posizione': 'Latitudine: 40.730610, Longitudine: -73.935242', 'preferito': False, 'priorita': 1, 'proprietario': 1}
            posizione = {'lat': '40.730610', 'lon': '-73.935242', 'address': {'village': 'New York', 'county': 'New York County', 'state': 'New York', 'country': 'United States of America'}}
            inquinamento = {'value': 10.0, 'unit': 'µg/m³'}
            lat = '40.730610'
            lon = '-73.935242'
            meteo = {'temperature': '20.0', 'humidity': '50.0', 'wind_speed': '5.0', 'wind_direction': 'N'}
            
            # Configurare i mock per restituire i dati di test
            mock_trovaTerreno.return_value = terreno
            mock_cercaPosizione.return_value = posizione
            mock_cercaInquinamento.return_value = inquinamento
            mock_cercalat.return_value = lat
            mock_cercalon.return_value = lon
            mock_cercaMeteo.return_value = meteo
            print(AmbienteAgricoloService.trovaTerreno(1))
            # Invocare la funzione dettagli con una richiesta GET
            response = self.app.get('/dettagliterreno?idTerreno=1')

            # Verificare che la risposta sia corretta
            #verificare che la risposta sia corretta
            self.assertEqual(response.status_code, 200)
            
if  __name__ == '__main__':
    unittest.main()