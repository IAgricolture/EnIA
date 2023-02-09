import unittest
import os, sys
from unittest.mock import MagicMock

from mockito import mock, when

sys.path.append(os.path.abspath(os.path.join('.' )))
from src.logic.Storage.AutenticazioneDAO import AutenticazioneDAO
from src.logic.Registrazione.RegistrazioneService import RegistrazioneService
from src.logic.Storage.TerrenoDAO import TerrenoDAO
from src.logic.AmbienteAgricolo.AmbienteAgricoloService import AmbienteAgricoloService
from src.dbConnection import terreni

from src.logic.model.Utente import Utente




class RegistrazioneServiceTest(unittest.TestCase):
    
    def test_case_1_1_1(self):
        print  ("test_case_1_1_1")
        # Arrange
        nome="Mario"
        cognome="Rossi"
        email="CropHater@"
        password = "CropIsLove18@"
        codice = "123456"
        indirizzo = "Via Roma 1, Saviano"
        data_nascita = "01/01/2000"
        
        #act
        risultato = RegistrazioneService.creaUtente(nome, cognome, email, password,data_nascita, codice, indirizzo)
        
        #assert
        self.assertEqual(risultato["emailNonValida"], True)
        self.assertEqual(risultato["utenteRegistrato"], False)
        
    def test_case_1_1_2(self):
        print   ("test_case_1_1_2")
        # Arrange
        nome="Mario"
        cognome="Rossi"
        email="LoveTuberi@gmail.it"
        password = "Potato Potato Potato"
        codice = "123456"
        indirizzo = "Via Roma 1, Saviano"
        data_nascita = "01/01/2000"
        
        #act
        risultato = RegistrazioneService.creaUtente(nome, cognome, email, password,data_nascita, codice, indirizzo)
        
        #assert
        self.assertEqual(risultato["passwordNonValida"], True)
        self.assertEqual(risultato["utenteRegistrato"], False)
        
    def test_case_1_1_3(self):
        print("test_case_1_1_3")
        # Arrange
        nome="Willie13"
        cognome="The Duck"
        email="LoveTuberi@gmail.it"
        password = "Papera43@"
        codice = "123456"
        indirizzo = "Via Roma 1, Saviano"
        data_nascita = "01/01/2000"
        
        #act
        risultato = RegistrazioneService.creaUtente(nome, cognome, email, password,data_nascita, codice, indirizzo)
        
        #assert
        self.assertEqual(risultato["nomeNonValido"], True)
        self.assertEqual(risultato["utenteRegistrato"], False)
        
    def test_case_1_1_4(self):
        print("test_case_1_1_4")
        # Arrange
        nome="Willie"
        cognome="The Duck13"
        email="LoveTuberi@gmail.it"
        password = "Papera43@"
        codice = "123456"
        indirizzo = "Via Roma 1, Saviano"
        data_nascita = "01/01/2000"
        
        #act
        risultato = RegistrazioneService.creaUtente(nome, cognome, email, password,data_nascita, codice, indirizzo)
        
        #assert
        self.assertEqual(risultato["cognomeNonValido"], True)
        self.assertEqual(risultato["utenteRegistrato"], False)
        
        """
        _summary_: Test case 1.1.8 : La registrazione non va a buon fine dato che il codice di accesso non è presente nel database
        """
    def test_case_1_1_5(self):
        print("test_case_1_1_5")
        # Arrange
        nome="Kratos"
        cognome="Zeus"
        email=" Boycome@libero.it"
        password = "IHateGods18@"
        codice = "123456"
        indirizzo = "Via Roma 5, Fisciano"
        data_nascita = "01/01/2000"
        
        #act
        risultato = RegistrazioneService.creaUtente(nome, cognome, email, password, data_nascita, codice, indirizzo)
        #assert
        self.assertEqual(risultato["codiceNonValido"], True)
        self.assertEqual(risultato["utenteRegistrato"], False)
        
        """_summary_: Test case 1.1.9 : La registrazione non va a buon fine dato che il codice è già stato utilizzato
        """
    def test_case_1_1_6(self):
        # Arrange
        nome="Kratos"
        cognome="Zeus"
        email=" BoyComeHere@libero.it"
        password = "IHateGods18@"
        codice = "5507d0" #codice già utilizzato
        indirizzo = "Via Roma 5, Fisciano"
        data_nascita = "01/01/2000"
        
        #act
        risultato = RegistrazioneService.creaUtente(nome, cognome, email, password, data_nascita, codice, indirizzo)
        #assert
        self.assertEqual(risultato["codiceNonValido"], True)
        self.assertEqual(risultato["utenteRegistrato"], False)
    
        """_summary_: Test case 1.1.7 : La registrazione non va a buon fine dato che l'indirizzo non è valido
       """
    def test_case_1_1_7(self):
        print("test_case_1_1_7")
        # Arrange
        nome="Giuseppe"
        cognome="Della Zappa"
        email="peepino@gmail.com"
        password = "Papera43@"
        codice = "123456"
        indirizzo = "Via Di 2329392, Lor@##"
        data_nascita = "01/01/2000"
        
        #act
        risultato = RegistrazioneService.creaUtente(nome, cognome, email,password, data_nascita, codice, indirizzo)
        
        #assert
        self.assertEqual(risultato["indirizzoNonValido"], True)
        self.assertEqual(risultato["utenteRegistrato"], False)
    
    """_summary_: Test case 1.1.8 : La registrazione non va a buon fine dato che l'indirizzo non esiste
    """
    def test_case_1_1_8(self):
        print("test-case_1_1_8")
        # Arrange
        nome="Giuseppe"
        cognome="Della Zappa"
        email="peepino@gmail.com"
        password = "Papera43@"
        codice = "123456"
        indirizzo = "Via GIANMARIA DELLE DUE  MARIE 13, isolanonesiste, peterpan"
        data_nascita = "01/01/2000"
        
        #act
        risultato = RegistrazioneService.creaUtente(nome, cognome, email,password, data_nascita, codice, indirizzo)

        #assert
        self.assertEqual(risultato["indirizzoNonValido"], True)
        self.assertEqual(risultato["utenteRegistrato"], False)
    """_summary_: Test case 1.1.9 : La registrazione va a buon fine
    """
    def test_case_1_1_9(self):
        print("test-case_1_1_9")
        nome="Giuseppe"
        cognome="Della Zappa"
        email="PeppinoELoZappino@gmail.com"
        password = "ZappaForever@56"
        codice = "AC48D20F20SC73L"
        indirizzo = "Via Molino 12, Saviano"
        data_nascita = "01/01/2000"
    
        #mock AutenticazioneDAO.trovaUtenteByCodiceDiAccesso
        utente_mock = Utente("", "", "", "" ,"","", "", "", "AC48D20F20SC73L", "","")
        buffer_1 = AutenticazioneDAO.trovaUtenteByCodiceDiAccesso
        buffer_2 = AutenticazioneDAO.modificaUtente
        AutenticazioneDAO.trovaUtenteByCodiceDiAccesso = MagicMock(return_value = utente_mock)
        AutenticazioneDAO.modificaUtente = MagicMock(return_value = True)
        risultato = RegistrazioneService.creaUtente(nome, cognome, email, password, data_nascita, codice, indirizzo)
        
        self.assertEqual(risultato["utenteRegistrato"], True)

        #clean
        AutenticazioneDAO.trovaUtenteByCodiceDiAccesso = buffer_1
        AutenticazioneDAO.modificaUtente = buffer_2
        
if __name__ == '__main__':
    unittest.main()