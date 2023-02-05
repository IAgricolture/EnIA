import unittest
import os, sys
from flask import jsonify
from flask_login import current_user

import requests



sys.path.append(os.path.abspath(os.path.join('.' )))
from unittest.mock import patch
from src import app


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

                         
if  __name__ == '__main__':
    unittest.main()