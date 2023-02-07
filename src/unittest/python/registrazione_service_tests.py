import unittest
import os, sys

from mockito import mock, when
sys.path.append(os.path.abspath(os.path.join('.' )))
from src.logic.Registrazione.RegistrazioneService import RegistrazioneService
from src.logic.Storage.TerrenoDAO import TerrenoDAO
from src.logic.AmbienteAgricolo.AmbienteAgricoloService import AmbienteAgricoloService
from src.dbConnection import terreni


class RegistrazioneServiceTest(unittest.TestCase):
    
    def test_case_1_1_1(self):
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
        #TODO conferma password non esiste
        pass
    
    def test_case_1_1_4(self):
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
        
    def test_case_1_1_5(self):
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
        
    def test_case_1_1_6(self):
        pass #TODO numero di telefono non esiste modificare tcs
    
    def test_case_1_1_7(self):
        pass #TODO il codice di accesso è una stringa di 6 caratteri numerici randomici si evita quindi questo caso di test
    
        """
        _summary_: Test case 1.1.8 : La registrazione non va a buon fine dato che il codice di accesso non è presente nel database
        """
    def test_case_1_1_8(self):
        # Arrange
        nome="Kratos"
        cognome="Zeus"
        email=" BoyComeHere@libero.it"
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
    def test_case_1_1_9(self):
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
    
        """_summary_: Test case 1.1.10 : La registrazione non va a buon fine dato che l'indirizzo non è valido
       
    def test_case_1_1_10(self):
        # Arrange
        nome="Giuseppe"
        cognome="Della Zappa"
        email="peepino@gmail.com"
        password = "Papera43@"
        codice = "123456"
        indirizzo = "Via Di 2329392, Lor@##"
        data_nascita = "01/01/2000"
        
        #act
        risultato = RegistrazioneService.creaUtente(nome, cognome, email,data_nascita, password, codice, indirizzo)
        
        #assert
        self.assertEqual(risultato["indirizzoNonValido"], True)
        self.assertEqual(risultato["utenteRegistrato"], False)
         """
    
    """_summary_: Test case 1.1.11 : La registrazione non va a buon fine dato che l'indirizzo non esiste
    """
    def test_case_1_1_11(self):
        #arrange
        # Arrange
        nome="Giuseppe"
        cognome="Della Zappa"
        email="peepino@gmail.com"
        password = "Papera43@"
        codice = "123456"
        indirizzo = "Via GIANMARIA DELLE DUE  MARIE 13, isolanonesiste, peterpan"
        data_nascita = "01/01/2000"
        
        #act
        risultato = RegistrazioneService.creaUtente(nome, cognome, email,data_nascita, password, codice, indirizzo)

        #assert
        self.assertEqual(risultato["indirizzoNonValido"], True)
        self.assertEqual(risultato["utenteRegistrato"], False)
    """_summary_: Test case 1.1.12 : La registrazione va a buon fine
    """
    def test_case_1_1_12(self):
        #TODO 
        pass
        