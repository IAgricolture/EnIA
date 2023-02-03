from multiprocessing import Process
import os
import sys
import threading
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
sys.path.append(os.path.abspath(os.path.join('.' )))
from src import app
from flask_cors import CORS

def inserisci_dati_login(driver: webdriver.Chrome, email, password):
        elem = driver.find_element(By.ID, "email")
        elem.send_keys(email)

        elem = driver.find_element(By.ID, "password")
        elem.send_keys(password)

def inserisci_dati_aggiunta_terreno(driver: webdriver.Chrome, nome, coltura,stadio_sviluppo, preferito, priorita):
        elem = driver.find_element(By.ID, "nome")
        elem.send_keys(nome)

        elem = driver.find_element(By.ID, "coltura")
        #elem è un oggetto di tipo select
        try:
            select = Select(elem)
            select.select_by_visible_text(coltura)
        except:
            print("coltura non valida")
            return False
     
        elem = driver.find_element(By.ID, "stadio")
        select = Select(elem)
        print(stadio_sviluppo)
        #catch exception
        try:
            
            select.select_by_visible_text(stadio_sviluppo)
        except:
            print("stadio di sviluppo non valido")
            return False
        
        elem = driver.find_element(By.ID, "preferito")
        if preferito:
            elem.click()
        elem = driver.find_element(By.ID, "priorita")
        elem.send_keys(priorita)

        elem = driver.find_element(By.ID, "map")
        elem.click()
        elem.click()
        elem.click()
        return True

def inserisci_dati_aggiunta_terreno_click_sbagliati(driver: webdriver.Chrome, nome, coltura,stadio_sviluppo, preferito, priorita):
        elem = driver.find_element(By.ID, "nome")
        elem.send_keys(nome)

        elem = driver.find_element(By.ID, "coltura")
        #elem è un oggetto di tipo select
        try:
            select = Select(elem)
            select.select_by_visible_text(coltura)
        except:
            print("coltura non valida")
            return
     
        elem = driver.find_element(By.ID, "stadio")
        select = Select(elem)
        #catch exception
        try:
            select.select_by_visible_text(stadio_sviluppo)
        except:
            print("stadio di sviluppo non valido")
            return
        
        elem = driver.find_element(By.ID, "preferito")
        if preferito:
            elem.click()
        elem = driver.find_element(By.ID, "priorita")
        elem.send_keys(priorita)

        elem = driver.find_element(By.ID, "map")

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
def run_flask_app():
    #start the flask app in a second thread
    app.run(port=5000)

class SystemTest (unittest.TestCase):
    url = "http://127.0.0.1:5000/login"
    urllogin= "http://127.0.0.1:5000/login"
    urlinserisciterreno = "http://127.0.0.1:5000/aggiuntaTerreno"

    def setUp(self):
        self.p = Process(target=run_flask_app)
        #start the flask app in a thread
        self.p.start()
        print("starting server...")
        self.driver = webdriver.Chrome()

    def test_login(self):
        self.tc_1_1_1()
        self.tc_1_1_2()
        self.tc_1_1_3()
        self.tc_1_1_4()
        self.tc_1_1_5()
        self.tc_1_1_6()
        self.tc_1_1_7()
        self.tc_1_1_8()
    
    def test_aggiunta_terreno(self):
        self.tc_2_1_1()
        self.tc_2_1_2()
        self.tc_2_1_3()
        self.tc_2_1_4()
        self.tc_2_1_5()
        self.tc_2_1_8()
        self.tc_2_1_9()
        self.tc_2_1_11()


    def tc_1_1_1(self):
        driver = self.driver
        driver.get(self.url)
        print(self.url)
        time.sleep(1)
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
        time.sleep(1)
        elem = driver.find_element(By.ID, "emailerr")
        assert "Formato non valido" in elem.text

    def tc_1_1_2(self):
        driver = self.driver
        driver.get(self.url)
        time.sleep(1)

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

    def tc_1_1_3(self):
        driver = self.driver
        driver.get(self.url)
        time.sleep(1)

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

    def tc_1_1_4(self):
        driver = self.driver
        driver.get(self.url)
        time.sleep(1)

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
    
    def tc_1_1_5(self):
        driver = self.driver
        driver.get(self.url)
        time.sleep(1)

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
    def tc_1_1_6(self):
        driver = self.driver
        driver.get(self.url)
        time.sleep(1)

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

        elem = driver.find_element(By.ID, "cod")
        #correggere
        #assert "codice non valido o gia' usato" in elem.text

    def tc_1_1_7(self):
        driver = self.driver
        driver.get(self.url)
        time.sleep(1)

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
    def tc_1_1_8(self):
        driver = self.driver
        driver.get(self.url)
        time.sleep(1)

        assert "Login" in driver.title

        elem = driver.find_element(By.LINK_TEXT, "Registrati qui")
        elem.click()

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
        
        assert "Registrazione" in driver.title

    def tc_2_1_1(self):
        driver = self.driver
        driver.get(self.urllogin)
        time.sleep(1)
        
        assert "Login" in driver.title
        
        inserisci_dati_login(driver, "prova@gmail.com", "password")

        elem = driver.find_element(By.ID, "signin")
        elem.click()

        self.driver.get(self.urlinserisciterreno)
        time.sleep(1)
        result = inserisci_dati_aggiunta_terreno(driver, "Ç?(&%U", "Orzo", "Fine Stagione", True, 12)
        elem = driver.find_element(By.ID, "add")
        elem.click()

        #find one class alert alert-danger
        time.sleep(1)
        elem = driver.find_element(By.CLASS_NAME, "alert-danger")
        #assert che elem esiste
        assert elem is not None
    
    def tc_2_1_2(self):
        driver = self.driver
        driver.get(self.urllogin)
        time.sleep(1)
        
        assert "Login" in driver.title
        
        inserisci_dati_login(driver, "prova@gmail.com", "password")

        elem = driver.find_element(By.ID, "signin")
        elem.click()

        self.driver.get(self.urlinserisciterreno)
        time.sleep(1)
        result = inserisci_dati_aggiunta_terreno(driver, "", "Orzo", "Fine Stagione", True, 12)
        elem = driver.find_element(By.ID, "add")
        elem.click()

        #find one class alert alert-danger
        elem = driver.find_element(By.CLASS_NAME, "alert-danger")
        #assert che elem esiste
        assert elem is not None
    
    def tc_2_1_3(self):
        driver = self.driver
        driver.get(self.urllogin)
        time.sleep(1)
        
        assert "Login" in driver.title
        
        inserisci_dati_login(driver, "prova@gmail.com", "password")

        elem = driver.find_element(By.ID, "signin")
        elem.click()

        self.driver.get(self.urlinserisciterreno)
        time.sleep(1)
        result = inserisci_dati_aggiunta_terreno(driver, "terreno1", "", "Fine Stagione", True, 12)
        elem = driver.find_element(By.ID, "add")
        elem.click()

        #find one class alert alert-danger
        elem = driver.find_element(By.CLASS_NAME, "alert-danger")
        #assert che elem esiste
        assert elem is not None

    #ORACOLO: Inserimento fallisce per formato invalido di coltura
    def tc_2_1_4(self):
        driver = self.driver
        driver.get(self.urllogin)
        time.sleep(1)
        
        assert "Login" in driver.title
        
        inserisci_dati_login(driver, "prova@gmail.com", "password")

        elem = driver.find_element(By.ID, "signin")
        elem.click()

        self.driver.get(self.urlinserisciterreno)
        time.sleep(1)
        result = inserisci_dati_aggiunta_terreno(driver, "terreno1", "*çéçé=(", "Fine Stagione", True, 12)
        
        elem = driver.find_element(By.ID, "add")
        elem.click()

        #find one class alert alert-danger
        elem = driver.find_element(By.CLASS_NAME, "alert-danger")
        #assert che elem esiste
        assert elem is not None

    #ORACOLO: Inserimento fallisce per formato invalido di coltura
    def tc_2_1_5(self):
        driver = self.driver
        driver.get(self.urllogin)
        time.sleep(1)
        
        assert "Login" in driver.title
        
        inserisci_dati_login(driver, "prova@gmail.com", "password")

        elem = driver.find_element(By.ID, "signin")
        elem.click()

        self.driver.get(self.urlinserisciterreno)
        time.sleep(1)
        result = inserisci_dati_aggiunta_terreno(driver, "terreno1", "Orzaiolinoo", "Fine Stagione", True, 12)
        assert result is False
        elem = driver.find_element(By.ID, "add")
        elem.click()

        #find one class alert alert-danger
        elem = driver.find_element(By.CLASS_NAME, "alert-danger")
        #assert che elem esiste
        assert elem is not None

    #ORACOLO: Fallisce in quanto manca la posizione
    def tc_2_1_8(self):
        pass

    #ORACOLO: Fallito per non aver inserito posizione
    def tc_2_1_9(self):
        driver = self.driver
        driver.get(self.urllogin)
        time.sleep(1)
        
        assert "Login" in driver.title
        
        inserisci_dati_login(driver, "prova@gmail.com", "password")

        elem = driver.find_element(By.ID, "signin")
        elem.click()

        self.driver.get(self.urlinserisciterreno)
        time.sleep(1)
        result = inserisci_dati_aggiunta_terreno_click_sbagliati(driver, "terreno1", "Orzo", "Fine Stagione", True, 12)
        elem = driver.find_element(By.ID, "add")
        elem.click()

        #find one class alert alert-danger
        elem = driver.find_element(By.CLASS_NAME, "alert-danger")
        #assert che elem esiste
        assert elem is not None

    #test_case_2_1_10 non si può fare dato che il preferito o è checked o non è checked

    #ORACOLO: Inserimento va a buon fine in quanto tutti i campi sono corretti.
    def tc_2_1_11(self):
        driver = self.driver
        driver.get(self.urllogin)
        time.sleep(1)
        
        assert "Login" in driver.title
        
        inserisci_dati_login(driver, "prova@gmail.com", "password")

        elem = driver.find_element(By.ID, "signin")
        elem.click()

        self.driver.get(self.urlinserisciterreno)
        time.sleep(1)
        result = inserisci_dati_aggiunta_terreno(driver, "terreno1", "Orzo", "Fine Stagione", True, 12)
        elem = driver.find_element(By.ID, "add")
        elem.click()

        #find one class alert alert-danger
        try:
            elem = driver.find_element(By.CLASS_NAME, "alert-danger")
        except Exception:
            elem = None
        #assert che elem esiste
        assert elem is None

    def tearDown(self):
        self.p.terminate()
        self.driver.close()


if __name__ == "__main__":
    unittest.main()

        

