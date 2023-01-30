import os
import sys
from unittest import mock
import unittest

sys.path.append(os.path.abspath(os.path.join('.' )))
from src import app
from src.logic.Storage.AutenticazioneDAO import AutenticazioneDAO
from src.logic.Storage.EventoDAO import EventoDAO
from src.logic.Storage.ImpiantoDiIrrigazioneDAO import ImpiantoDiIrrigazioneDAO
from src.logic.Storage.LicenzaDAO import LicenzaDAO
from src.logic.Storage.MetodoDiPagamentoDAO import MetodoDiPagamentoDAO
from src.logic.Storage.ScheduleDAO import ScheduleDAO
from src.logic.Storage.TerrenoDAO import TerrenoDAO
from src.logic.model.Terreno import Terreno
from src.logic.model.Schedule import Schedule
from src.logic.model.MetodoDiPagamento import MetodoDiPagamento
from src.logic.model.Licenza import Licenza
from src.logic.model.ImpiantoDiIrrigazione import ImpiantoDiIrrigazione
from src.logic.model.Evento import Evento
from src.logic.model.Utente import Utente

class TerrenoDAOTests(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.terrenoTest = Terreno(None, "Terreno-A", "Orzo", "Sviluppo", {"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[14.783607,40.772225],[14.783735,40.772745],[14.784594,40.771965],[14.783607,40.772225]]]}}, True, 15, "63b9e6a27862c31f1f7b221p")
        self.IDTerreno = TerrenoDAO.InserisciTerreno(self.terrenoTest)
        self.resultTerreno = TerrenoDAO.TrovaTerreno(self.IDTerreno)    
        
    def tearDown(self):
        self.removalTerreno = TerrenoDAO.RimuoviTerreno(self.resultTerreno)
    
    def test_TrovaTerreno_pass(self):
        print("TrovaTerreno")
        self.assertEqual(self.terrenoTest, self.resultTerreno)
    
    def test_InserisciTerreno_pass(self):
        print("InserisciTerreno")
        self.assertEqual(self.terrenoTest, self.resultTerreno) #Controlla che siano uguali
    
    def test_RimuoviTerreno_pass(self):
        print("RimuoviTerreno")
        result = TerrenoDAO.RimuoviTerreno(self.resultTerreno) #Deve rimanere anche se ci prova il teardown dopo, altrimenti non funzia.
        self.assertEqual(result, True) #Controlla che siano uguali   
    
    def test_ModificaTerreno_pass(self):
        print("ModificaTerreno")
        colturaPrecedente = self.resultTerreno.coltura
        self.resultTerreno.coltura = "Cavolo"
        TerrenoDAO.modificaTerreno(self.resultTerreno)
        nuovoTerreno = TerrenoDAO.TrovaTerreno(self.IDTerreno)
        self.assertNotEqual(colturaPrecedente, nuovoTerreno.coltura) #Controlla che siano uguali
    
    def test_restituisciTerreniByFarmer(self):
        print("restituisciTerreniByFarmer")
        IDTerreno = TerrenoDAO.InserisciTerreno(self.terrenoTest)
        resultTerreno = TerrenoDAO.TrovaTerreno(IDTerreno)
        terreno2 = self.terrenoTest
        terreno2.nome = "ProvaTerreno2"
        IDTerreno2 = TerrenoDAO.InserisciTerreno(terreno2)
        terreno2 = TerrenoDAO.TrovaTerreno(IDTerreno2)
        result = TerrenoDAO.restituisciTerreniByFarmer(resultTerreno.proprietario)
        TerrenoDAO.RimuoviTerreno(terreno2)
        self.assertEqual(resultTerreno, result[0])
        self.assertEqual(terreno2, result[1])        

class AutenticazioneDAOTests(unittest.TestCase):
    
    def setUp(self):
        self.farmer = Utente("", "Francesco Maria", "Puca", "provaemail8@gmail.com", "8c0863379f06c27f7883d36101d0372a105527be64314f9501ad2d37e1b1c9dcc6658e196af067176b24bae8f3b2d4e29ad39dd54e613cc7dfa6550948606a66", "farmer", "2002-06-10", "31682670364", None, "Via Europa 25, Pontecagnano Faiano", None)
        self.farmerID = AutenticazioneDAO.creaUtente(self.farmer)
        self.farmerExpected = AutenticazioneDAO.trovaUtente(self.farmerID)
        self.dipendente = Utente("", "Pietro", "Galli", "ilpietro@outlook.it", "020576c9c472443ba5f596fc7df95fa3cc48cd08fbfd90aa3440794bd6a7ba3821e315460c8e56cf7a24e86fc71f0894a9adbf9684e10888a3f7a285b4629609", "pollution analyst", "1998-07-08", "3fta15", None, "Via Antonio Vivaldi 2, Pagliarone", self.farmerID)
        self.dipendenteID = AutenticazioneDAO.creaUtente(self.dipendente)
        self.dipendenteExpected = AutenticazioneDAO.trovaUtente(self.dipendenteID)
        
    def tearDown(self):
        AutenticazioneDAO.eliminaUtente(self.farmerID)
        AutenticazioneDAO.eliminaUtente(self.dipendenteID)
    
    def test_trovaUtenteByEmail_pass(self):
        print("trovaUtenteByEmail")
        farmerResult = AutenticazioneDAO.trovaUtenteByEmail(self.farmer.email)
        self.assertEqual(farmerResult, self.farmerExpected)
        dipendenteResult = AutenticazioneDAO.trovaUtenteByEmail(self.dipendente.email)
        self.assertEqual(dipendenteResult, self.dipendenteExpected)
    
    def test_trovaUtente_pass(self):
        print("trovaUtente")
        farmerResult = AutenticazioneDAO.trovaUtente(self.farmerID)
        self.assertEqual(farmerResult, self.farmerExpected)
        dipendenteResult = AutenticazioneDAO.trovaUtente(self.dipendenteID)
        self.assertEqual(dipendenteResult, self.dipendenteExpected)

    
    def test_trovaUtenteByCodiceDiAccesso_pass(self):
        print("trovaUtenteByCodiceDiAccesso")
        dipendenteResult = AutenticazioneDAO.trovaUtenteByCodiceDiAccesso(self.dipendente.codice)
        self.assertEqual(dipendenteResult, self.dipendenteExpected)
    
    def test_creaUtente_pass(self):
        print("creaUtente")
        self.assertEqual(self.farmer, self.farmerExpected)
        self.assertEqual(self.dipendente, self.dipendenteExpected)
    
    def test_eliminaUtente_pass(self):
        print("eliminaUtente")
        resultFarmer = AutenticazioneDAO.eliminaUtente(self.farmerID)
        resultDipendente = AutenticazioneDAO.eliminaUtente(self.dipendenteID)
        self.assertEqual(resultFarmer, True)
        self.assertEqual(resultDipendente, True)
    
    def test_modificaUtente_pass(self):
        print("modificaUtente")
        emailPrecedenteFarmer = self.farmerExpected.email
        self.farmerExpected.email = "cambioemail1@gmail.com"
        AutenticazioneDAO.modificaUtente(self.farmerExpected)
        resultFarmer = AutenticazioneDAO.trovaUtente(self.farmerExpected.id)
        self.assertNotEqual(emailPrecedenteFarmer, resultFarmer.email)
        
        emailPrecedenteDipendente = self.dipendenteExpected.email
        self.dipendenteExpected.email = "email2nuova@libero.it"
        AutenticazioneDAO.modificaUtente(self.dipendenteExpected)
        resultDipendente = AutenticazioneDAO.trovaUtente(self.dipendenteExpected.id)
        self.assertNotEqual(emailPrecedenteDipendente, resultDipendente.email)
        
        
    def test_listaUtentiTutti_pass(self):
        print("listaUtentiTutti")
        results = list(AutenticazioneDAO.listaUtentiTutti())
        self.assertGreaterEqual(len(results), 2)
        
    def test_listaDipendenti_pass(self):
        print("listaDipendenti")
        dipendente2 = Utente("", "Gaia", "Pietri", "PostaPietri@virgilio.it", "4be410db8d26899ecea8259d3ca4692c1033fa94ec1db5a31a018ff7729fc337d86358ec4dfd102eac7c5070e505ab8dd305bc1318e281d8f9a0498598fd3206", "irrigation manager", "2001-11-03", "4bcddg", None, "Via F.Sco Spirito 11, Mercato", self.farmerID)
        dipendente2ID = AutenticazioneDAO.creaUtente(dipendente2)
        results = list(AutenticazioneDAO.listaDipendenti(self.farmerID))
        AutenticazioneDAO.eliminaUtente(dipendente2ID)
        self.assertGreaterEqual(len(results), 2)

    def test_insertSlot_pass(self):
        print("insertSlot")
        resultDipendenteID = str(AutenticazioneDAO.insertSlot("pollution analyst", "trr12e", self.farmerID).inserted_id)
        resultDipendente = AutenticazioneDAO.trovaUtenteByCodiceDiAccesso("trr12e")
        expectedDipendente = Utente(resultDipendenteID, "", "", "", "", "pollution analyst", "", None, "trr12e", "", self.farmerID)
        AutenticazioneDAO.eliminaUtente(resultDipendenteID)
        self.assertEqual(resultDipendente, expectedDipendente)  
    
    def test_getDatore(self):
        result = AutenticazioneDAO.getDatore(self.dipendenteExpected.id)
        self.assertEqual(result, self.dipendenteExpected.datore) 
        
        
if __name__ == '__main__':
    print("Partenza test di TerrenoDAO")
    test = TerrenoDAOTests()
    test.setUp()
    test.run()
    print("Partenza test di AutenticazioneDAO")
    test = AutenticazioneDAOTests()
    test.setUp()
    test.run()