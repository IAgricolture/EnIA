import unittest
import os, sys
from flask import jsonify
from flask_login import current_user
sys.path.append(os.path.abspath(os.path.join('.' )))
from src.logic.model.Terreno import Terreno
from unittest.mock import patch
from src import app
from src.logic.Storage.TerrenoDAO import TerrenoDAO
from src.logic.AmbienteAgricolo.AmbienteAgricoloService import AmbienteAgricoloService


class AmbienteAgricoloControllerTests(unittest.TestCase):
    """
    Classe di test per il controller dell'ambiente agricolo
    """
    def setUp(self):
        self.app = app.test_client()
        #fai il login con ruolo "Farmer"
        self.app.post("/login", data={"email": "prova@gmail.com", "password": "password", "next": "visualizzaTerreni"})
        
    @patch('src.logic.AmbienteAgricolo.AmbienteAgricoloService.AmbienteAgricoloService.aggiungiTerreno')
    def test_aggiungiTerreno_post(self, mock_aggiungiTerreno):
        """
        Test per il metodo AmbienteAgricoloController.aggiungiTerreno
        Args:
            mock_aggiungiTerreno ():   Mock per il metodo AmbienteAgricoloService.aggiungiTerreno
        """
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
    @patch('src.logic.DecisionIntelligence.DecisionIntelligenceService.DecisionIntelligenceService.cercaMeteo')
    def test_dettagli(self, mock_cercaMeteo, mock_cercalon, mock_cercalat, mock_cercaInquinamento, mock_cercaPosizione, mock_trovaTerreno):
        """
        Test per il metodo AmbienteAgricoloController.dettagli
        Args:
            mock_cercaMeteo (mock): Mock per il metodo AmbienteAgricoloService.cercaMeteo
            mock_cercalon (mock): Mock per il metodo AmbienteAgricoloService.cercalon
            mock_cercalat (mock): Mock per il metodo AmbienteAgricoloService.cercalat
            mock_cercaInquinamento (mock): Mock per il metodo AmbienteAgricoloService.cercaInquinamento
            mock_cercaPosizione (mock): Mock per il metodo AmbienteAgricoloService.cercaPosizione
            mock_trovaTerreno (mock): Mock per il metodo AmbienteAgricoloService.trovaTerreno
        """
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
    @patch('src.logic.DecisionIntelligence.DecisionIntelligenceService.DecisionIntelligenceService.cercaMeteo')
    def test_dettagli_key_error(self, mock_cercaMeteo, mock_cercalon, mock_cercalat, mock_cercaInquinamento, mock_cercaPosizione, mock_trovaTerreno):
        """
        Test per il metodo AmbienteAgricoloController.dettagli con KeyError
        Args:
            mock_cercaMeteo (mock): Mock per il metodo AmbienteAgricoloService.cercaMeteo
            mock_cercalon (mock): Mock per il metodo AmbienteAgricoloService.cercalon
            mock_cercalat (mock): Mock per il metodo AmbienteAgricoloService.cercalat
            mock_cercaInquinamento (mock): Mock per il metodo AmbienteAgricoloService.cercaInquinamento
            mock_cercaPosizione (mock): Mock per il metodo AmbienteAgricoloService.cercaPosizione
            mock_trovaTerreno (mock): Mock per il metodo AmbienteAgricoloService.trovaTerreno
        """
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
    @patch('src.logic.DecisionIntelligence.DecisionIntelligenceService.DecisionIntelligenceService.cercaMeteo')
    def test_dettagli_city_in_address(self, mock_cercaMeteo, mock_cercalon, mock_cercalat, mock_cercaInquinamento, mock_cercaPosizione, mock_trovaTerreno):
        """
        Test per il metodo AmbienteAgricoloController.dettagli con city in address
        Args:
            mock_cercaMeteo (mock): Mock per il metodo AmbienteAgricoloService.cercaMeteo
            mock_cercalon (mock): Mock per il metodo AmbienteAgricoloService.cercalon
            mock_cercalat (mock): Mock per il metodo AmbienteAgricoloService.cercalat
            mock_cercaInquinamento (mock): Mock per il metodo AmbienteAgricoloService.cercaInquinamento
            mock_cercaPosizione (mock): Mock per il metodo AmbienteAgricoloService.cercaPosizione
            mock_trovaTerreno (mock): Mock per il metodo AmbienteAgricoloService.trovaTerreno
        """
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
    @patch('src.logic.DecisionIntelligence.DecisionIntelligenceService.DecisionIntelligenceService.cercaMeteo')
    def test_dettagli_village_in_address(self, mock_cercaMeteo, mock_cercalon, mock_cercalat, mock_cercaInquinamento, mock_cercaPosizione, mock_trovaTerreno):
        """
        Test per il metodo AmbienteAgricoloController.dettagli con village in address
        Args:
            mock_cercaMeteo (mock): Mock per il metodo AmbienteAgricoloService.cercaMeteo
            mock_cercalon (mock): Mock per il metodo AmbienteAgricoloService.cercalon
            mock_cercalat (mock): Mock per il metodo AmbienteAgricoloService.cercalat
            mock_cercaInquinamento (mock): Mock per il metodo AmbienteAgricoloService.cercaInquinamento
            mock_cercaPosizione (mock): Mock per il metodo AmbienteAgricoloService.cercaPosizione
            mock_trovaTerreno (mock): Mock per il metodo AmbienteAgricoloService.trovaTerreno
        """
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
            
    @patch('src.logic.AmbienteAgricolo.AmbienteAgricoloService.AmbienteAgricoloService.trovaTerreno')
    @patch('src.logic.AmbienteAgricolo.AmbienteAgricoloService.AmbienteAgricoloService.cercalat')
    @patch('src.logic.AmbienteAgricolo.AmbienteAgricoloService.AmbienteAgricoloService.cercalon')
    @patch('src.logic.AmbienteAgricolo.AmbienteAgricoloService.AmbienteAgricoloService.restituisciPredizioneLivelliIrrigazione')
    def test_visualizzaPredizioneIrrigazione(self, mock_restituisciPredizioneLivelliIrrigazione, mock_cercalon, mock_cercalat, mock_trovaTerreno):
        """
        Test per il metodo AmbienteAgricoloController.visualizzaPredizioneIrrigazione
        Args:
            mock_restituisciPredizioneLivelliIrrigazione (mock): Mock per il metodo AmbienteAgricoloService.restituisciPredizioneLivelliIrrigazione
            mock_cercalon (mock): Mock per il metodo AmbienteAgricoloService.cercalon
            mock_cercalat (mock): Mock per il metodo AmbienteAgricoloService.cercalat
            mock_trovaTerreno (mock): Mock per il metodo AmbienteAgricoloService.trovaTerreno
        """
        mock_terreno = Terreno(1, 'Terreno 1', 'Pomodori', 'Semina', 'Latitudine: 40.730610, Longitudine: -73.935242', False, 1, 1)
        mock_lat = '40.730610'
        mock_lon = '-73.935242'
        mock_predizione = {'data': '2021-05-01', 'livello': '1'}
        mock_trovaTerreno.return_value = mock_terreno
        mock_cercalat.return_value = mock_lat
        mock_cercalon.return_value = mock_lon
        mock_restituisciPredizioneLivelliIrrigazione.return_value = mock_predizione
       
        response = self.app.post('/visualizzaPredizioneIrrigazione', json={'id_terreno': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), mock_predizione)
            
if  __name__ == '__main__':
    unittest.main()