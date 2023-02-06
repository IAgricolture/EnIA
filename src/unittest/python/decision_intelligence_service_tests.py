import unittest
import os, sys

from mockito import mock, verify
sys.path.append(os.path.abspath(os.path.join('.' )))
from src.logic.DecisionIntelligence.DecisionIntelligenceService import DecisionIntelligenceService
from src.logic.Storage.AutenticazioneDAO import AutenticazioneDAO
from src.logic.Utente.GestioneUtenteService import GestioneUtenteService

farmer = "63b9e6a27862c31f1f7b221f"
ruoli = ["irrigation manager", "pollution analyst"]

class DecisionIntelligenceServiceTest(unittest.TestCase):

    #Oracolo: test fallisce dato che Sviluppatissima non è uno stadio di crescita valido
    def test_case_5_1_1(self):
        #arrange
        stadio_crescita = "Sviluppatissima"
        latitudine = 12.5
        longitudine = 13.5
        coltura = "Orzo"
        
        try:
            
            result = DecisionIntelligenceService.getPredizioneLivelliIrrigazione(latitudine, longitudine, coltura, stadio_crescita)
        except Exception as e:
            self.assertEqual("Stadio di crescita non valido", str(e))
            return
    
        self.fail("Exception not raised")
    
    #Oracolo: test fallisce dato che 250 va oltre il limite massimo di latitudine
    def test_case_5_1_2(self):
        #arrange
        stadio_crescita = "Iniziale"
        latitudine = 250
        longitudine = 13.5
        coltura = "Orzo"
        
        try: 
            result = DecisionIntelligenceService.getPredizioneLivelliIrrigazione(latitudine, longitudine, coltura, stadio_crescita)
        except Exception as e:
            self.assertEqual("Latitudine o longitudine non valide", str(e))
            return
    
        self.fail("Exception not raised")
      
    #Oracolo: test fallisce dato che -190.32 va oltre il limite minimo di longitudine
    def test_case_5_1_3(self):
        #arrange
        stadio_crescita = "Iniziale"
        latitudine = 12
        longitudine = -190.32
        coltura = "Orzo"
        
        try: 
            result = DecisionIntelligenceService.getPredizioneLivelliIrrigazione(latitudine, longitudine, coltura, stadio_crescita)
        except Exception as e:
            self.assertEqual("Latitudine o longitudine non valide", str(e))
            return
    
        self.fail("Exception not raised")
    
    #Oracolo: test fallisce dato che "Pasta al forno" non è una coltura valida
    def test_case_5_1_4(self):
        #arrange
        stadio_crescita = "Iniziale"
        latitudine = 12
        longitudine = 13.5
        coltura = "Pasta al forno"
        
        try: 
            result = DecisionIntelligenceService.getPredizioneLivelliIrrigazione(latitudine, longitudine, coltura, stadio_crescita)
        except Exception as e:
            self.assertEqual("Coltura non valida", str(e))
            return
    
        self.fail("Exception not raised")
    
    def test_case_5_1_5(self):
        #arrange
        stadio_crescita = "Iniziale"
        latitudine = 12
        longitudine = 13.5
        coltura = "Orzo"
        
        result = DecisionIntelligenceService.getPredizioneLivelliIrrigazione(latitudine, longitudine, coltura, stadio_crescita)
        #assert that the result is a dictionary with 7 keys and that the values are not null
        self.assertEqual(7, len(result))
        for key in result:
            self.assertIsNotNone(result[key])
        
if __name__ == '__main__':
    unittest.main()