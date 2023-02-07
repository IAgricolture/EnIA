    
import hashlib
import os
import sys
import unittest

from unittest.mock import MagicMock, patch
sys.path.append(os.path.abspath(os.path.join('.' )))

from src import app
from src.logic.Registrazione.RegistrazioneService import RegistrazioneService

class RegistrazioneControllerTests(unittest.TestCase):
    """
    Testa la logica del controller per la registrazione
    """
    def setUp(self):
        """
        Setup il test client per l'applicazione
        """
        self.app = app.test_client()
        self.app.testing = True

    def test_registrazione_con_codice_di_accesso_get(self):
        """
        Testa la GET request per la /register route
        """
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)

    def test_registrazione_con_codice_di_accesso_post(self):
        """
        Testa la POST request per la /register route
        """
        # Set up the mock object for RegistrazioneService.modificaUtente
        buffer = RegistrazioneService.modificaUtente
        RegistrazioneService.modificaUtente = MagicMock(return_value={'success': True})

        # Set up the form data for the POST request
        form_data = {
            'email': 'example@email.com',
            'nome': 'John',
            'cognome': 'Doe',
            'password': 'secret',
            'dataNascita': '2000-01-01',
            'codice': 'ABCD1234',
            'indirizzo': '123 Main St'
        }

        # Make the POST request
        response = self.app.post('/register', data=form_data)

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Check the response content
        expected_content = {'success': True}
        #turn expceted content into a json object
        
        
        self.assertEqual(response.get_json(), expected_content)

        # Check that the RegistrazioneService.modificaUtente method was called with the correct arguments
        RegistrazioneService.modificaUtente.assert_called_with('John', 'Doe', 'example@email.com', 'secret', '2000-01-01', 'ABCD1234', '123 Main St')

        # Restore the original method
        RegistrazioneService.modificaUtente = buffer

    @patch('src.logic.Registrazione.RegistrazioneService.RegistrazioneService.trovaUtenteByEmail')
    @patch('src.logic.Registrazione.RegistrazioneService.RegistrazioneService.creaFarmer')
    @patch('src.logic.Registrazione.RegistrazioneService.RegistrazioneService.creaLicenza')
    @patch('src.logic.GestionePagamento.GestionePagamentoService.GestionePagamentoService.creaMetodoDiPagamento')
    def test_registrazioneFarmer_post(self, mock_creaMetodoDiPagamento, mock_creaLicenza, mock_creaFarmer, mock_trovaUtenteByEmail):
        """
        Testa la registrazione di un farmer con una chiamata POST al controller
        """
        mock_trovaUtenteByEmail.return_value = None
        mock_creaFarmer.return_value = 1
        mock_creaLicenza.return_value = True
        mock_creaMetodoDiPagamento.return_value = True

        # Add code to simulate a POST request to the registrazioneFarmer endpoint
        # Setup the data for the request
        data = {
            "email": "test@example.com",
            "nome": "Test",
            "cognome": "User",
            "password": "password",
            "dataDiNascita": "01-01-1970",
            "partitaiva": "12345678901",
            "licenza": "1",
            "numerocarta": "1234567890123456",
            "titolare": "Test User",
            "scadenza": "01-2023",
            "cvv": "123",
            "indirizzo": "1 Main St"
        }
        # Send the request
        response = self.app.post("/registerf", data=data)
        # Check the response status code
        self.assertEqual(response.status_code, 302) # expect redirect
        self.assertEqual(response.location, "/login")

        data["password"] = hashlib.sha512(data.get("password").encode()).hexdigest()
        # Assert that the mock methods were called with the correct arguments
        mock_trovaUtenteByEmail.assert_called_with('test@example.com')
        mock_creaFarmer.assert_called_with('Test', 'User', 'test@example.com',data["password"] , None, '12345678901', '1 Main St')
        mock_creaLicenza.assert_called_with(1, '1')
        mock_creaMetodoDiPagamento.assert_called_with(data['numerocarta'], data["titolare"], data['scadenza'], data['cvv'], 1)

    def test_registrazioneFarmer_get(self):
        """
        Testa la registrazione di un farmer con una chiamata GET al controller
        """
        response = self.app.get("/registerf")
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()