import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def Inserisci_dati_registrazione_codice_accesso(driver: webdriver.Chrome, nome, cognome, email, password, conferma, codice, indirizzo, data_nascita):
        elem = driver.find_element(By.ID, "nome")
        elem.send_keys(nome)

        elem = driver.find_element(By.ID, "cognome")
        elem.send_keys(cognome)

        elem = driver.find_element(By.ID, "email")
        elem.send_keys(email)

        elem = driver.find_element(By.ID, "password")
        elem.send_keys(password)

        elem = driver.find_element(By.ID, "confermaPassword")
        elem.send_keys(conferma)

        elem = driver.find_element(By.ID, "codiceDiAccesso")
        elem.send_keys(codice)

        elem = driver.find_element(By.ID, "indirizzo")
        elem.send_keys(indirizzo)

        elem = driver.find_element(By.ID, "dataNascita")
        elem.send_keys(data_nascita)

class SystemTest (unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_case_1_1_1(self):
        driver = self.driver
        driver.get("http://localhost:5000/login")

        assert "Login" in driver.title

        elem = driver.find_element(By.LINK_TEXT, "Registrati qui")
        elem.click()

        assert "Registrazione" in driver.title

        nome="Mario"
        cognome="Rossi"
        email="CropHater@"
        password = "CropIsLove18@"
        conferma = "CropIsLove18@"
        codice = "123456"
        indirizzo = "Via Roma 1, Saviano"
        data_nascita = "01/01/2000"

        Inserisci_dati_registrazione_codice_accesso(driver, nome, cognome, password, conferma, email, codice, indirizzo, data_nascita)

        elem = driver.find_element(By.LINK_TEXT, "SIGN UP")
        elem.click()

        elem = driver.find_element(By.ID, "emailerr")
        assert "Formato non valido" in elem.text

    def test_case_1_1_2(self):
        driver = self.driver
        driver.get("http://localhost:5000/login")

        assert "Login" in driver.title

        elem = driver.find_element(By.LINK_TEXT, "Registrati qui")
        elem.click()

        assert "Registrazione" in driver.title

        nome="Patata"
        cognome="Tubero"
        email="LoveTuberi@gmail.it"
        password = "Potato Potato Potato"
        conferma = "Potato Potato Potato"
        codice = "AC48D20F20SC73L"
        indirizzo = "Corso Italia, Saviano, Napoli, Campania, 80039, 1"
        data_nascita = "01/01/2000"

        Inserisci_dati_registrazione_codice_accesso(driver, nome, cognome, password, conferma, email, codice, indirizzo, data_nascita)

        elem = driver.find_element(By.LINK_TEXT, "SIGN UP")
        elem.click()

        elem = driver.find_element(By.ID, "passerr")
        assert "Formato non valido" in elem.text

    def test_case_1_1_3(self):
        driver = self.driver
        driver.get("http://localhost:5000/login")

        assert "Login" in driver.title

        elem = driver.find_element(By.LINK_TEXT, "Registrati qui")
        elem.click();

        assert "Registrazione" in driver.title

        nome="Pierluigi"
        cognome="Macchia"
        email="PierluigiIlChad@libero.it"
        password = "LoveProtein56!"
        conferma = "Lveprotein55@"
        codice = "AC48D20F20SC73L"
        indirizzo = "Via Canal Bernardo, Catene, Marghera, Venezia, Veneto, 30175, Italia, 25"
        data_nascita = "01/01/2000"

        Inserisci_dati_registrazione_codice_accesso(driver, nome, cognome, password, conferma, email, codice, indirizzo, data_nascita)

        elem = driver.find_element(By.LINK_TEXT, "SIGN UP")
        elem.click()

        elem = driver.find_element(By.ID, "conferr")
        assert "Le due password non corrispondono" in elem.text

    def test_case_1_1_4(self):
        driver = self.driver
        driver.get("http://localhost:5000/login")

        assert "Login" in driver.title

        elem = driver.find_element(By.LINK_TEXT, "Registrati qui")
        elem.click();

        assert "Registrazione" in driver.title

        nome="Willie13"
        cognome="The Duck"
        email="LeFocheSonoCarine@libero.it"
        password = "Papera43@"
        conferma = "Papera43@"
        codice = "AC48D20F20SC73L"
        indirizzo = "Località Pian d'Asdrubale, 17, Ca' L'Agostina, Fermignano, Pesaro e Urbino, Marche, Italia"
        data_nascita = "01/01/2000"

        Inserisci_dati_registrazione_codice_accesso(driver, nome, cognome, password, conferma, email, codice, indirizzo, data_nascita)

        elem = driver.find_element(By.LINK_TEXT, "SIGN UP")
        elem.click()

        elem = driver.find_element(By.ID, "nomeerr")
        assert "Formato non valido" in elem.text
    
    def test_case_1_1_5(self):
        driver = self.driver
        driver.get("http://localhost:5000/login")

        assert "Login" in driver.title

        elem = driver.find_element(By.LINK_TEXT, "Registrati qui")
        elem.click();

        assert "Registrazione" in driver.title

        nome="Willie13"
        cognome="The Duck13"
        email="LeFocheSonoCarine@libero.it"
        password = "Papera43@"
        conferma = "Papera43@"
        codice = "AC48D20F20SC73L"
        indirizzo = "Via Di Fabio 1, La Briglia, Vaiano, Prato, Toscana, 59021, Italia"
        data_nascita = "01/01/2000"

        Inserisci_dati_registrazione_codice_accesso(driver, nome, cognome, password, conferma, email, codice, indirizzo, data_nascita)

        elem = driver.find_element(By.LINK_TEXT, "SIGN UP")
        elem.click()

        elem = driver.find_element(By.ID, "cognomeerr")
        assert "Formato non valido" in elem.text
    
    #TODO: Farlo funzionare con le chiamate asincrone 
    def test_case_1_1_6(self):
        driver = self.driver
        driver.get("http://localhost:5000/login")

        assert "Login" in driver.title

        elem = driver.find_element(By.LINK_TEXT, "Registrati qui")
        elem.click();

        assert "Registrazione" in driver.title

        nome="Kratos"
        cognome="Spartan"
        email="BoyComeHere@libero.it"
        password = "IHateZeus01!"
        conferma = "IHateZeus01!"
        codice = "AC4820F73L"
        indirizzo = "Via dello Zappatore 43, Veronetta, Centro Storico, Verona, Veneto, 37122, Italia"
        data_nascita = "01/01/2000"

        Inserisci_dati_registrazione_codice_accesso(driver, nome, cognome, password, conferma, email, codice, indirizzo, data_nascita)

        elem = driver.find_element(By.LINK_TEXT, "SIGN UP")
        elem.click()

        driver.execute_async_script()
        time.sleep(10)
        elem = driver.find_element(By.ID, "cod")
        assert "codice non valido o gia' usato" in elem.text

    def test_case_1_1_7(self):
        driver = self.driver
        driver.get("http://localhost:5000/login")

        assert "Login" in driver.title

        elem = driver.find_element(By.LINK_TEXT, "Registrati qui")
        elem.click();

        assert "Registrazione" in driver.title

        nome="Giuseppe"
        cognome="Della Zappa"
        email="PeppinoELoZappino@gmail.com"
        password = "ZappaForever#56"
        conferma = "ZappaForever#56"
        codice = "AC48D20F20SC73L"
        indirizzo = "Via Di 293299 Lor@##"
        data_nascita = "01/01/2000"

        Inserisci_dati_registrazione_codice_accesso(driver, nome, cognome, password, conferma, email, codice, indirizzo, data_nascita)

        elem = driver.find_element(By.LINK_TEXT, "SIGN UP")
        elem.click()

        elem = driver.find_element(By.ID, "indirizzoerr")
        assert "Formato non valido" in elem.text    

    #TODO: Farlo funzionare con le chiamate asincrone 
    def test_case_1_1_8(self):
        driver = self.driver
        driver.get("http://localhost:5000/login")

        assert "Login" in driver.title

        elem = driver.find_element(By.LINK_TEXT, "Registrati qui")
        elem.click();

        assert "Registrazione" in driver.title

        nome="Giuseppe"
        cognome="Della Zappa"
        email="PeppinoELoZappino@gmail.com"
        password = "ZappaForever#56"
        conferma = "ZappaForever#56"
        codice = "AC48D20F20SC73L"
        indirizzo = "Via Molino 12, Saviano, Napoli, Italia, 80039"
        data_nascita = "01/01/2000"

        Inserisci_dati_registrazione_codice_accesso(driver, nome, cognome, password, conferma, email, codice, indirizzo, data_nascita)

        elem = driver.find_element(By.LINK_TEXT, "SIGN UP")
        elem.click()
        
        time.sleep(10)
        assert "Login" in driver.title

    def tearDown(self):
        self.driver.close()
        

