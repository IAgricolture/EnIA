import os
import sys
from unittest import mock
import unittest
import datetime

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
        TerrenoDAO.RimuoviTerreno(resultTerreno)
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
        
class MetodoDiPagamentoDAOTests(unittest.TestCase):
    
    def setUp(self):
        self.metodo = MetodoDiPagamento("", "5220629405479725", "Marco Rossi", "12/24", "874", "63b9e6a27862c31f1f7p40p")
        self.metodoID = MetodoDiPagamentoDAO.creaMetodo(self.metodo)
        self.metodoExpected = MetodoDiPagamentoDAO.findMetodo(self.metodoID)
        
    def tearDown(self):
        MetodoDiPagamentoDAO.eliminaMetodo(self.metodoID)
            
    def test_findMetodo_pass(self):
        print("findMetodo")
        metodoResult = MetodoDiPagamentoDAO.findMetodo(self.metodoID)
        self.assertEqual(metodoResult, self.metodoExpected)

    def test_creaMetodo_pass(self):
        print("creaMetodo")
        self.assertEqual(self.metodo, self.metodoExpected)
    
    def test_findMetodoByProprietario_pass(self):
        print("findMetodoByProprietario")
        metodoResult = MetodoDiPagamentoDAO.findMetodoByProprietario(self.metodo.proprietario)
        self.assertEqual(metodoResult, self.metodoExpected)
    
    def test_modificaMetodo_pass(self):
        print("modificaMetodo")
        scadenzaPrecedenteMetodo = self.metodoExpected.scadenza
        self.metodoExpected.scadenza = "11/25"
        MetodoDiPagamentoDAO.modificaMetodo(self.metodoExpected)
        resultMetodo = MetodoDiPagamentoDAO.findMetodo(self.metodoExpected.id)
        self.assertNotEqual(scadenzaPrecedenteMetodo, resultMetodo.scadenza)
    
    def test_eliminaMetodo_pass(self):
        print("eliminaMetodo")
        result = MetodoDiPagamentoDAO.eliminaMetodo(self.metodoID)
        self.assertEqual(result, True)
        
class LicenzaDAOTests(unittest.TestCase):
    
    def setUp(self):
        self.licenza = Licenza("", "licenza standard", 29.99, "2022-01-31", "2023-01-31", False, "63bd21ceb7dba69993e45sms")
        self.licenzaID = LicenzaDAO.creaLicenza(self.licenza)
        self.licenzaExpected = LicenzaDAO.findLicenza(self.licenzaID)
        
    def tearDown(self):
        LicenzaDAO.eliminaLicenza(self.licenzaID)
            
    def test_findLicenza_pass(self):
        print("findLicenza")
        licenzaResult = LicenzaDAO.findLicenza(self.licenzaID)
        self.assertEqual(licenzaResult, self.licenzaExpected)

    def test_creaLicenza_pass(self):
        print("creaLicenza")
        self.assertEqual(self.licenza, self.licenzaExpected)
    
    def test_findLicenzaByProprietario_pass(self):
        print("findLicenzaByProprietario")
        licenzaResult = LicenzaDAO.findLicenzaByProprietario(self.licenza.proprietario)
        self.assertEqual(licenzaResult, self.licenzaExpected)
    
    def test_eliminaLicenza_pass(self):
        print("eliminaLicenza")
        result = LicenzaDAO.eliminaLicenza(self.licenzaID)
        self.assertEqual(result, True)     
 
class EventoDAOTests(unittest.TestCase):
    
    def setUp(self):
        self.evento = Evento("", "Scheduling", "Scheduling consigliato applicato", datetime.datetime.now().isoformat(' ', 'seconds'), "Scheduling", False, True, "63d1a61ecf0e0efd3dee3asw")
        self.eventoID = EventoDAO.creaEvento(self.evento)
        self.eventoExpected = EventoDAO.findEvento(self.eventoID)
        
    def tearDown(self):
        EventoDAO.cancellaEvento(self.eventoID)
            
    def test_findEvento_pass(self):
        print("findEvento")
        eventoResult = EventoDAO.findEvento(self.eventoID)
        self.assertEqual(eventoResult, self.eventoExpected)

    def test_creaEvento_pass(self):
        print("creaEvento")
        self.assertEqual(self.evento, self.eventoExpected)
    
    def test_findEventiByTerreno_pass(self):
        print("findEventiByTerreno")
        evento2 = Evento("", "Scheduling", "Scheduling consigliato applicato", datetime.datetime.now().isoformat(' ', 'seconds'), "Scheduling", False, False, "63d1a61ecf0e0efd3dee3asw")
        evento2ID = EventoDAO.creaEvento(evento2)
        results = list(EventoDAO.findEventiByTerreno(evento2.terreno))
        EventoDAO.cancellaEvento(evento2ID)
        self.assertGreaterEqual(len(results), 2)
    
    def test_cancellaTuttiEventiByTerreno_pass(self):
        print("cancellaEvento")
        evento2 = Evento("", "Scheduling", "Scheduling consigliato applicato", datetime.datetime.now().isoformat(' ', 'seconds'), "Scheduling", False, False, "63d1a61ecf0e0efd3dee3asw")
        evento2ID = EventoDAO.creaEvento(evento2)
        result = EventoDAO.cancellaTuttiEventiByTerreno(evento2.terreno)
        self.assertEqual(result, 2)     
    
    def test_cancellaEvento_pass(self):
        print("cancellaEvento")
        result = EventoDAO.cancellaEvento(self.eventoID)
        self.assertEqual(result, True)     
        
class ImpiantoDiIrrigazioneDAOTests(unittest.TestCase):
    
    def setUp(self):
        terrenoperimpianto = Terreno(None, "Terreno-A", "Orzo", "Sviluppo", {"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[14.783607,40.772225],[14.783735,40.772745],[14.784594,40.771965],[14.783607,40.772225]]]}}, True, 15, "63b9e6a27862c31f1f7b221p")
        self.terrenoperimpiantoID = TerrenoDAO.InserisciTerreno(terrenoperimpianto)
        self.impianto = ImpiantoDiIrrigazione("", "IrrigatoreTest", "irrigatore", "", "{'type': 'Feature', 'properties': {}, 'geometry': {'type': 'Point', 'coordinates': [14.789861, 40.774736]}}", False) 
        self.impiantoID = ImpiantoDiIrrigazioneDAO.creaImpianto(self.impianto, self.terrenoperimpiantoID)
        self.impiantoExpected = ImpiantoDiIrrigazioneDAO.findImpiantoById(self.impiantoID)
        
    def tearDown(self):
        TerrenoDAO.RimuoviTerreno(TerrenoDAO.TrovaTerreno(self.terrenoperimpiantoID))
        ImpiantoDiIrrigazioneDAO.eliminaImpianto(self.impiantoID)      
              
    def test_findImpiantiByTerreno_pass(self):
        print("findImpiantiByTerreno")
        impianto2 = ImpiantoDiIrrigazione("", "NuovoIrrigatore", "irrigatore", "", "{'type': 'Feature', 'properties': {}, 'geometry': {'type': 'Point', 'coordinates': [7.306682, 45.172598]}}", True)
        impianto2ID = ImpiantoDiIrrigazioneDAO.creaImpianto(impianto2, self.terrenoperimpiantoID)
        results = ImpiantoDiIrrigazioneDAO.findImpiantiByTerreno(self.terrenoperimpiantoID)
        ImpiantoDiIrrigazioneDAO.eliminaImpianto(impianto2ID)
        self.assertGreaterEqual(len(results), 2)
              
    def test_findImpiantoById_pass(self):
        print("findImpiantoById")
        impiantoResult = ImpiantoDiIrrigazioneDAO.findImpiantoById(self.impiantoID)
        self.assertEqual(impiantoResult, self.impiantoExpected)

    def test_creaImpianto_pass(self):
        print("creaImpianto")
        self.assertEqual(self.impianto, self.impiantoExpected)
    
    def test_modificaImpianto_pass(self):
        print("modificaImpianto")
        nomePrecedenteImpianto = self.impiantoExpected.nome
        self.impiantoExpected.nome = "NomeCambiato"
        ImpiantoDiIrrigazioneDAO.modificaImpianto(self.impiantoExpected)
        resultImpianto = ImpiantoDiIrrigazioneDAO.findImpiantoById(self.impiantoExpected.id)
        self.assertNotEqual(nomePrecedenteImpianto, resultImpianto.nome)          
    
    def test_attivaImpianto_pass(self):
        print("attivaImpianto")
        result = ImpiantoDiIrrigazioneDAO.attivaImpianto(self.impiantoID)
        self.assertEqual(result, True)
        attivo = ImpiantoDiIrrigazioneDAO.findImpiantoById(self.impiantoID).attivo
        self.assertEqual(attivo, True)

    def test_disattivaImpianto_pass(self):
        print("disattivaImpianto")
        ImpiantoDiIrrigazioneDAO.attivaImpianto(self.impiantoID) #Necessario perchè input non è attivo
        result = ImpiantoDiIrrigazioneDAO.disattivaImpianto(self.impiantoID)
        self.assertEqual(result, True)
        attivo = ImpiantoDiIrrigazioneDAO.findImpiantoById(self.impiantoID).attivo
        self.assertEqual(attivo, False)
        
    def test_eliminaImpianto_pass(self):
        print("eliminaImpianto")
        result = ImpiantoDiIrrigazioneDAO.eliminaImpianto(self.impiantoID)
        self.assertEqual(result, True)     
                
class ScheduleDAOTests(unittest.TestCase):
    
    def setUp(self):
        terrenoperschedule = Terreno(None, "Terreno-C", "Orzo", "Sviluppo", {"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[14.783607,40.772225],[14.783735,40.772745],[14.784594,40.771965],[14.783607,40.772225]]]}}, False, 15, "63b9e6a27862c31f1f7b221p")
        self.terrenoperscheduleID = TerrenoDAO.InserisciTerreno(terrenoperschedule)
        print(self.terrenoperscheduleID)
        self.schedule = Schedule("", datetime.datetime.now(), datetime.datetime.now(), "basso", self.terrenoperscheduleID)
        print(self.schedule.terreno)
        self.scheduleID = ScheduleDAO.creaSchedule(self.schedule)
        self.scheduleExpected = ScheduleDAO.findSchedule(self.scheduleID)
        print(self.scheduleExpected.terreno)
        
    def tearDown(self):
        TerrenoDAO.RimuoviTerreno(TerrenoDAO.TrovaTerreno(self.terrenoperscheduleID))
        ScheduleDAO.eliminaSchedule(self.scheduleID)      
              
    def test_findSchedule_pass(self):
        print("findSchedule")
        scheduleResult = ScheduleDAO.findSchedule(self.scheduleID)
        self.assertEqual(scheduleResult, self.scheduleExpected)
             
    def test_creaSettimanaScheduleNullo_pass(self):
        print("creaSettimanaScheduleNullo")
        result = ScheduleDAO.creaSettimanaScheduleNullo(self.schedule.terreno)
        self.assertEqual(result.acknowledged, True)
        for id in result.inserted_ids:
            resultSchedule = ScheduleDAO.findSchedule(id)
            self.assertEqual(resultSchedule.modalita, "Nessuno")
            self.assertEqual(resultSchedule.terreno, self.schedule.terreno)
        

    def test_creaSchedule_pass(self):
        print("creaSchedule")
        self.assertEqual(self.schedule.inizio.replace(microsecond=0).time(), self.scheduleExpected.inizio.replace(microsecond=0))
    
    def test_getWeeklySchedule_pass(self):
        print("getWeeklySchedule")
        weekly = list(ScheduleDAO.getWeeklySchedule(self.schedule.terreno))
        self.assertEqual(len(weekly), 7)
        for schedule in weekly:
            self.assertEqual(str(schedule["terreno"]), str(self.schedule.terreno))
            
    def test_modificaLivelloSchedule_pass(self):
        print("modificaLivelloSchedule")
        try:
            result = ScheduleDAO.modificaLivelloSchedule(self.schedule.terreno, datetime.datetime.now().date().strftime("%d-%m-%Y"), "Alto")
            self.assertEqual(result, True)
        except Exception as e:
            print(e)
        
    def test_eliminaSchedule_pass(self):
        print("eliminaSchedule")
        result = ScheduleDAO.eliminaSchedule(self.scheduleID)
        self.assertEqual(result, True)
        
if __name__ == '__main__':
    print("Partenza test di TerrenoDAO")
    test = TerrenoDAOTests()
    test.setUp()
    test.run()
    print("Partenza test di AutenticazioneDAO")
    test = AutenticazioneDAOTests()
    test.setUp()
    test.run()
    print("Partenza test di MetodoDiPagamentoDAO")
    test = MetodoDiPagamentoDAOTests()
    test.setUp()
    test.run()
    print("Partenza test di LicenzaPagamentoDAO")
    test = LicenzaDAOTests()
    test.setUp()
    test.run()
    print("Partenza test di EventoDAO")
    test = EventoDAOTests()
    test.setUp()
    test.run()
    print("Partenza test di ImpiantoDiIrrigazioneDAO")
    test = ImpiantoDiIrrigazioneDAOTests()
    test.setUp()
    test.run()
    print("Partenza test di ScheduleDAO")
    test = ScheduleDAOTests()
    test.setUp()
    test.run()