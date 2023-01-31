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
        
if __name__ == '__main__':
    print("Partenza test di TerrenoDAO")
    test = TerrenoDAOTests()
    test.setUp()
    test.run()