from multiprocessing import Process
import os
import sys
import threading
import unittest
import time
from unittest.mock import MagicMock
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

sys.path.append(os.path.abspath(os.path.join('.' )))
from src import app
from src.logic.Adapters.OpenMeteoAdapter import OpenMeteoAdapter
from flask_cors import CORS

def inserisci_dati_login(driver: webdriver.Chrome, email, password):
        elem = driver.find_element(By.ID, "email")
        elem.send_keys(email)

        elem = driver.find_element(By.ID, "password")
        elem.send_keys(password)

def inserisci_ruolo(driver: webdriver.Chrome, ruolo):
        elem = driver.find_element(By.ID, "ruolo")
        select = Select(elem)
        try:
            select.select_by_visible_text(ruolo)
        except:
            print("ruolo non valido")
            return False
        return True

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
    urlazienda_agricola = "http://127.0.0.1:5000/AziendaAgricola"

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

    def test_genera_codice(self):
        self.tc_4_1_1()
        self.tc_4_1_2()

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

    def tc_4_1_1(self):
        driver = self.driver
        driver.get(self.urllogin)
        time.sleep(1)
        
        assert "Login" in driver.title
        
        inserisci_dati_login(driver, "prova@gmail.com", "password")

        elem = driver.find_element(By.ID, "signin")
        elem.click()

        self.driver.get(self.urlazienda_agricola)
        time.sleep(1)
        elem = driver.find_element(By.ID, "aggiungi")
        elem.click()
        result = inserisci_ruolo(driver, "ruolo1")
        assert result is False
    
    def tc_4_1_2(self):
        driver = self.driver
        driver.get(self.urllogin)
        time.sleep(1)
        
        assert "Login" in driver.title
        
        inserisci_dati_login(driver, "prova@gmail.com", "password")

        elem = driver.find_element(By.ID, "signin")
        elem.click()

        self.driver.get(self.urlazienda_agricola)
        time.sleep(1)
        elem = driver.find_element(By.ID, "aggiungi")
        elem.click()
        result = inserisci_ruolo(driver, "Irrigation Manager")
        assert result is True
        elem = driver.find_element(By.ID, "generacodice")
        elem.click()

        try:
            elem = driver.find_element(By.ID, "gencode")
        except Exception:
            elem = None

        assert elem is not None

    def test_decision_intelligence(self):
        driver = self.driver
        driver.get(self.urllogin)
        time.sleep(1)
        
        assert "Login" in driver.title
        
        inserisci_dati_login(driver, "prova@gmail.com", "password")

        elem = driver.find_element(By.ID, "signin")
        elem.click()
        elem = driver.find_element(By.LINK_TEXT,"Dettagli")
        elem.click()
        time.sleep(10)
        elem = driver.find_element(By.ID, "data-consigliati")
        #find table in elem
        table = elem.find_element(By.CLASS_NAME, "table")
        #find all tr in table
        trs = table.find_elements(By.TAG_NAME, "tr")

        #find all td in trs
        tds = []
        for tr in trs:
            tds.append(tr.find_elements(By.TAG_NAME, "td"))
        
        #assert that td in tds are not empty
        for td in tds:
            assert td is not None
    #non capisco perchè non funziona
    def test_visualizzazione_meteo(self):
        driver = self.driver
        driver.get(self.urllogin)
        time.sleep(1)
        
        #mock open meteo adapter
        result = {'latitude': 45.18, 'longitude': 7.2599998, 'generationtime_ms': 0.4780292510986328, 'utc_offset_seconds': 0, 'timezone': 'GMT', 'timezone_abbreviation': 'GMT', 'elevation': 1820.0, 'hourly_units': {'time': 'iso8601', 'temperature_2m': '°C', 'relativehumidity_2m': '%', 'precipitation': 'mm'}, 'hourly': {'time': ['2023-02-09T00:00', '2023-02-09T01:00', '2023-02-09T02:00', '2023-02-09T03:00', '2023-02-09T04:00', '2023-02-09T05:00', '2023-02-09T06:00', '2023-02-09T07:00', '2023-02-09T08:00', '2023-02-09T09:00', '2023-02-09T10:00', '2023-02-09T11:00', '2023-02-09T12:00', '2023-02-09T13:00', '2023-02-09T14:00', '2023-02-09T15:00', '2023-02-09T16:00', '2023-02-09T17:00', '2023-02-09T18:00', '2023-02-09T19:00', '2023-02-09T20:00', '2023-02-09T21:00', '2023-02-09T22:00', '2023-02-09T23:00', '2023-02-10T00:00', '2023-02-10T01:00', '2023-02-10T02:00', '2023-02-10T03:00', '2023-02-10T04:00', '2023-02-10T05:00', '2023-02-10T06:00', '2023-02-10T07:00', '2023-02-10T08:00', '2023-02-10T09:00', '2023-02-10T10:00', '2023-02-10T11:00', '2023-02-10T12:00', '2023-02-10T13:00', '2023-02-10T14:00', '2023-02-10T15:00', '2023-02-10T16:00', '2023-02-10T17:00', '2023-02-10T18:00', '2023-02-10T19:00', '2023-02-10T20:00', '2023-02-10T21:00', '2023-02-10T22:00', '2023-02-10T23:00', '2023-02-11T00:00', '2023-02-11T01:00', '2023-02-11T02:00', '2023-02-11T03:00', '2023-02-11T04:00', '2023-02-11T05:00', '2023-02-11T06:00', '2023-02-11T07:00', '2023-02-11T08:00', '2023-02-11T09:00', '2023-02-11T10:00', '2023-02-11T11:00', '2023-02-11T12:00', '2023-02-11T13:00', '2023-02-11T14:00', '2023-02-11T15:00', '2023-02-11T16:00', '2023-02-11T17:00', '2023-02-11T18:00', '2023-02-11T19:00', '2023-02-11T20:00', '2023-02-11T21:00', '2023-02-11T22:00', '2023-02-11T23:00', '2023-02-12T00:00', '2023-02-12T01:00', '2023-02-12T02:00', '2023-02-12T03:00', '2023-02-12T04:00', '2023-02-12T05:00', '2023-02-12T06:00', '2023-02-12T07:00', '2023-02-12T08:00', '2023-02-12T09:00', '2023-02-12T10:00', '2023-02-12T11:00', '2023-02-12T12:00', '2023-02-12T13:00', '2023-02-12T14:00', '2023-02-12T15:00', '2023-02-12T16:00', '2023-02-12T17:00', '2023-02-12T18:00', '2023-02-12T19:00', '2023-02-12T20:00', '2023-02-12T21:00', '2023-02-12T22:00', '2023-02-12T23:00', '2023-02-13T00:00', '2023-02-13T01:00', '2023-02-13T02:00', '2023-02-13T03:00', '2023-02-13T04:00', '2023-02-13T05:00', '2023-02-13T06:00', '2023-02-13T07:00', '2023-02-13T08:00', '2023-02-13T09:00', '2023-02-13T10:00', '2023-02-13T11:00', '2023-02-13T12:00', '2023-02-13T13:00', '2023-02-13T14:00', '2023-02-13T15:00', '2023-02-13T16:00', '2023-02-13T17:00', '2023-02-13T18:00', '2023-02-13T19:00', '2023-02-13T20:00', '2023-02-13T21:00', '2023-02-13T22:00', '2023-02-13T23:00', '2023-02-14T00:00', '2023-02-14T01:00', '2023-02-14T02:00', '2023-02-14T03:00', '2023-02-14T04:00', '2023-02-14T05:00', '2023-02-14T06:00', '2023-02-14T07:00', '2023-02-14T08:00', '2023-02-14T09:00', '2023-02-14T10:00', '2023-02-14T11:00', '2023-02-14T12:00', '2023-02-14T13:00', '2023-02-14T14:00', '2023-02-14T15:00', '2023-02-14T16:00', '2023-02-14T17:00', '2023-02-14T18:00', '2023-02-14T19:00', '2023-02-14T20:00', '2023-02-14T21:00', '2023-02-14T22:00', '2023-02-14T23:00', '2023-02-15T00:00', '2023-02-15T01:00', '2023-02-15T02:00', '2023-02-15T03:00', '2023-02-15T04:00', '2023-02-15T05:00', '2023-02-15T06:00', '2023-02-15T07:00', '2023-02-15T08:00', '2023-02-15T09:00', '2023-02-15T10:00', '2023-02-15T11:00', '2023-02-15T12:00', '2023-02-15T13:00', '2023-02-15T14:00', '2023-02-15T15:00', '2023-02-15T16:00', '2023-02-15T17:00', '2023-02-15T18:00', '2023-02-15T19:00', '2023-02-15T20:00', '2023-02-15T21:00', '2023-02-15T22:00', '2023-02-15T23:00'], 'temperature_2m': [-12.1, -11.7, -11.7, -11.8, -12.1, -12.5, -12.5, -12.2, -12.0, -10.1, -8.6, -7.9, -7.8, -7.3, -7.3, -7.6, -7.8, -8.4, -9.0, -9.1, -8.5, -8.1, -8.4, -8.4, -8.1, -7.7, -7.1, -6.6, -6.1, -5.6, -5.1, -4.9, -4.2, -3.2, -1.9, -0.3, 1.5, 1.7, 2.0, 1.4, 0.4, -0.8, -1.8, -2.3, -2.3, -2.4, -2.7, -2.9, -2.8, -2.6, -2.5, -2.6, -2.2, -2.2, -1.7, -1.4, -0.9, 0.3, 2.1, 4.7, 5.3, 5.6, 5.6, 5.5, 2.8, 2.7, 2.1, 2.0, 2.1, 2.2, 2.1, 2.1, 2.1, 2.1, 2.3, 2.2, 2.3, 2.4, 2.2, 2.2, 2.4, 3.1, 4.7, 5.1, 4.8, 4.4, 4.0, 3.2, 2.4, 1.4, 1.1, 0.5, 0.1, -0.4, -0.6, -0.6, -0.7, -0.9, -1.2, -1.4, -1.4, -1.3, -0.9, -0.5, 0.2, 1.0, 1.7, 2.4, 3.1, 3.4, 3.5, 3.5, 3.1, 2.6, 2.0, 1.9, 1.9, 1.9, 1.9, 1.9, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.1, 2.3, 2.6, 3.2, 4.0, 4.9, 5.8, 7.9, 7.6, 6.8, 6.0, 5.1, 4.2, 3.9, 3.9, 3.8, 3.7, 3.5, 3.1, 2.9, 2.6, 2.4, 2.1, 1.8, 1.7, 2.0, 2.5, 3.5, 4.5, 5.9, 7.0, 6.8, 6.1, 5.0, 4.3, 3.5, 2.6, 2.4, 2.5, 2.5, 2.3, 2.1], 'relativehumidity_2m': [87, 89, 84, 85, 82, 82, 81, 78, 76, 74, 68, 66, 70, 71, 72, 69, 70, 69, 65, 63, 56, 48, 45, 45, 40, 39, 37, 34, 32, 30, 29, 28, 26, 25, 27, 26, 18, 20, 20, 26, 41, 37, 31, 29, 24, 24, 25, 27, 28, 28, 28, 29, 27, 28, 26, 26, 23, 24, 27, 15, 14, 17, 17, 14, 25, 24, 25, 29, 27, 26, 24, 24, 24, 24, 25, 27, 28, 28, 29, 27, 26, 26, 22, 18, 28, 35, 45, 58, 64, 65, 58, 57, 56, 54, 52, 49, 46, 45, 43, 42, 40, 38, 37, 38, 39, 41, 40, 38, 38, 42, 49, 55, 54, 51, 47, 45, 43, 40, 38, 37, 35, 35, 35, 35, 34, 34, 33, 34, 35, 35, 34, 32, 30, 28, 34, 42, 46, 49, 50, 46, 40, 33, 31, 30, 30, 30, 30, 31, 32, 33, 34, 33, 32, 30, 27, 23, 23, 32, 45, 60, 65, 68, 67, 60, 50, 38, 34, 32], 'precipitation': [0.1, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}}
        #mock return value of get_data for OpenMeteoAdapter instance
        buffer = OpenMeteoAdapter.get_data
        OpenMeteoAdapter.get_data = lambda self: result
        assert "Login" in driver.title
        
        inserisci_dati_login(driver, "prova@gmail.com", "password")

        elem = driver.find_element(By.ID, "signin")
        elem.click()
        time.sleep(1)
        elem = driver.find_element(By.LINK_TEXT,"Dettagli")
        elem.click()
        time.sleep(4)
        elem = driver.find_element(By.ID, "datiMeteo")

        #find elem with class chartjs-size-monitor
        try:
            elem = elem.find_element(By.CLASS_NAME, "chartjs-size-monitor")
        except Exception:
            elem = None
        assert elem is not None
        
        #clean
        OpenMeteoAdapter.get_data = buffer

    def tearDown(self):
        self.p.terminate()
        self.driver.close()


if __name__ == "__main__":
    t = SystemTest()
    t.setUp()
    t.test_visualizzazione_meteo()
    t.tearDown()        

