import unittest
import os, sys
from unittest.mock import MagicMock

from mockito import mock, verify
sys.path.append(os.path.abspath(os.path.join('.' )))
from src.logic.Adapters.OpenMeteoAdapter import OpenMeteoAdapter
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

       #TEST VISUALIZZAZIONE METEO
    
    def test_visualizza_meteo_tc_3_1_1(self):
        print("TC_3_1_1")
        
        #arrange
        long = 190
        lat = 12.2
        
        try:
            #act
            DecisionIntelligenceService.cercaMeteo(lat, long)
        except Exception as e:
            #assert
            self.assertEqual(e.args[0], "Longitudine non valida")
            return 
        #assert
        self.fail("Eccezione non lanciata")
        
    def test_visualizza_meteo_tc_3_1_2(self):
        print("TC_3_1_2")
        
        #arrange
        long = 12.2
        lat = -25555
        
        try:
            #act
            DecisionIntelligenceService.cercaMeteo(lat, long)
        except Exception as e:
            #assert
            self.assertEqual(e.args[0], "Latitudine non valida")
            return 
        #assert
        self.fail("Eccezione non lanciata")
        
    def test_visualizza_meteo_tc_3_1_3(self):
        print("TC_3_1_3")
        
        #arrange
        long = 12.2
        lat = 14.3
        
        #mock return value of AmbienteAgricoloService.cercaMeteo
        dizionario = {'latitude': 14.25, 'longitude': 12.25, 'generationtime_ms': 0.36895275115966797, 'utc_offset_seconds': 0, 'timezone': 'GMT', 'timezone_abbreviation': 'GMT', 'elevation': 337.0, 'hourly_units': {'time': 'iso8601', 'temperature_2m': '°C', 'relativehumidity_2m': '%', 'precipitation': 'mm'}, 'hourly': {'time': ['2023-02-04T00:00', '2023-02-04T01:00', '2023-02-04T02:00', '2023-02-04T03:00', '2023-02-04T04:00', '2023-02-04T05:00', '2023-02-04T06:00', '2023-02-04T07:00', '2023-02-04T08:00', '2023-02-04T09:00', '2023-02-04T10:00', '2023-02-04T11:00', '2023-02-04T12:00', '2023-02-04T13:00', '2023-02-04T14:00', '2023-02-04T15:00', '2023-02-04T16:00', '2023-02-04T17:00', '2023-02-04T18:00', '2023-02-04T19:00', '2023-02-04T20:00', '2023-02-04T21:00', '2023-02-04T22:00', '2023-02-04T23:00', '2023-02-05T00:00', '2023-02-05T01:00', '2023-02-05T02:00', '2023-02-05T03:00', '2023-02-05T04:00', '2023-02-05T05:00', '2023-02-05T06:00', '2023-02-05T07:00', '2023-02-05T08:00', '2023-02-05T09:00', '2023-02-05T10:00', '2023-02-05T11:00', '2023-02-05T12:00', '2023-02-05T13:00', '2023-02-05T14:00', '2023-02-05T15:00', '2023-02-05T16:00', '2023-02-05T17:00', '2023-02-05T18:00', '2023-02-05T19:00', '2023-02-05T20:00', '2023-02-05T21:00', '2023-02-05T22:00', '2023-02-05T23:00', '2023-02-06T00:00', '2023-02-06T01:00', '2023-02-06T02:00', '2023-02-06T03:00', '2023-02-06T04:00', '2023-02-06T05:00', '2023-02-06T06:00', '2023-02-06T07:00', '2023-02-06T08:00', '2023-02-06T09:00', '2023-02-06T10:00', '2023-02-06T11:00', '2023-02-06T12:00', '2023-02-06T13:00', '2023-02-06T14:00', '2023-02-06T15:00', '2023-02-06T16:00', '2023-02-06T17:00', '2023-02-06T18:00', '2023-02-06T19:00', '2023-02-06T20:00', '2023-02-06T21:00', '2023-02-06T22:00', '2023-02-06T23:00', '2023-02-07T00:00', '2023-02-07T01:00', '2023-02-07T02:00', '2023-02-07T03:00', '2023-02-07T04:00', '2023-02-07T05:00', '2023-02-07T06:00', '2023-02-07T07:00', '2023-02-07T08:00', '2023-02-07T09:00', '2023-02-07T10:00', '2023-02-07T11:00', '2023-02-07T12:00', '2023-02-07T13:00', '2023-02-07T14:00', '2023-02-07T15:00', '2023-02-07T16:00', '2023-02-07T17:00', '2023-02-07T18:00', '2023-02-07T19:00', '2023-02-07T20:00', '2023-02-07T21:00', '2023-02-07T22:00', '2023-02-07T23:00', '2023-02-08T00:00', '2023-02-08T01:00', '2023-02-08T02:00', '2023-02-08T03:00', '2023-02-08T04:00', '2023-02-08T05:00', '2023-02-08T06:00', '2023-02-08T07:00', '2023-02-08T08:00', '2023-02-08T09:00', '2023-02-08T10:00', '2023-02-08T11:00', '2023-02-08T12:00', '2023-02-08T13:00', '2023-02-08T14:00', '2023-02-08T15:00', '2023-02-08T16:00', '2023-02-08T17:00', '2023-02-08T18:00', '2023-02-08T19:00', '2023-02-08T20:00', '2023-02-08T21:00', '2023-02-08T22:00', '2023-02-08T23:00', '2023-02-09T00:00', '2023-02-09T01:00', '2023-02-09T02:00', '2023-02-09T03:00', '2023-02-09T04:00', '2023-02-09T05:00', '2023-02-09T06:00', '2023-02-09T07:00', '2023-02-09T08:00', '2023-02-09T09:00', '2023-02-09T10:00', '2023-02-09T11:00', '2023-02-09T12:00', '2023-02-09T13:00', '2023-02-09T14:00', '2023-02-09T15:00', '2023-02-09T16:00', '2023-02-09T17:00', '2023-02-09T18:00', '2023-02-09T19:00', '2023-02-09T20:00', '2023-02-09T21:00', '2023-02-09T22:00', '2023-02-09T23:00', '2023-02-10T00:00', '2023-02-10T01:00', '2023-02-10T02:00', '2023-02-10T03:00', '2023-02-10T04:00', '2023-02-10T05:00', '2023-02-10T06:00', '2023-02-10T07:00', '2023-02-10T08:00', '2023-02-10T09:00', '2023-02-10T10:00', '2023-02-10T11:00', '2023-02-10T12:00', '2023-02-10T13:00', '2023-02-10T14:00', '2023-02-10T15:00', '2023-02-10T16:00', '2023-02-10T17:00', '2023-02-10T18:00', '2023-02-10T19:00', '2023-02-10T20:00', '2023-02-10T21:00', '2023-02-10T22:00', '2023-02-10T23:00'], 'temperature_2m': [21.1, 20.5, 20.1, 19.6, 19.2, 18.9, 18.0, 19.2, 21.6, 24.4, 26.9, 29.1, 31.1, 32.5, 33.1, 33.1, 32.3, 30.6, 28.2, 26.5, 25.3, 24.3, 23.4, 22.6, 22.0, 21.5, 20.9, 20.4, 19.9, 19.5, 19.2, 20.2, 23.0, 26.0, 28.8, 31.1, 32.8, 33.9, 34.4, 34.2, 33.5, 31.7, 29.3, 27.5, 26.3, 25.3, 24.4, 23.6, 22.9, 22.3, 21.7, 21.1, 20.6, 20.2, 19.6, 20.4, 22.6, 25.0, 27.4, 29.6, 31.2, 32.1, 32.4, 32.1, 31.2, 29.6, 27.4, 25.8, 24.6, 23.7, 22.9, 22.3, 21.7, 21.1, 20.5, 20.0, 19.5, 19.0, 18.5, 19.3, 21.3, 23.4, 25.5, 27.6, 29.3, 30.2, 30.7, 30.5, 29.6, 28.1, 26.1, 25.0, 23.9, 22.6, 21.9, 21.3, 20.6, 20.1, 19.7, 19.2, 18.6, 17.9, 17.8, 19.0, 20.8, 23.4, 25.4, 27.4, 29.6, 30.6, 31.1, 31.0, 30.0, 28.4, 26.3, 25.0, 23.8, 22.4, 21.6, 20.9, 20.2, 19.6, 19.1, 18.6, 18.2, 17.9, 17.6, 19.1, 21.3, 24.3, 26.4, 28.7, 31.0, 31.9, 32.4, 32.1, 31.1, 29.4, 27.3, 26.0, 24.8, 23.4, 22.5, 21.8, 21.0, 20.5, 20.1, 19.6, 19.0, 18.3, 18.5, 20.0, 22.4, 25.5, 27.6, 29.7, 31.9, 32.8, 33.2, 33.0, 31.9, 30.3, 28.1, 26.8, 25.5, 24.0, 23.2, 22.6], 'relativehumidity_2m': [24, 25, 25, 25, 25, 25, 27, 26, 22, 18, 15, 13, 11, 10, 9, 9, 9, 10, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 25, 25, 21, 17, 14, 11, 10, 9, 9, 9, 10, 11, 14, 15, 17, 17, 18, 19, 20, 20, 21, 22, 22, 23, 24, 23, 20, 17, 15, 13, 11, 10, 10, 10, 10, 11, 13, 14, 15, 16, 16, 17, 18, 20, 22, 24, 25, 27, 28, 28, 24, 21, 18, 15, 14, 13, 12, 12, 13, 14, 16, 17, 19, 21, 23, 24, 26, 27, 28, 29, 30, 32, 32, 30, 27, 23, 20, 18, 15, 14, 13, 13, 14, 15, 17, 18, 20, 21, 21, 21, 21, 21, 21, 21, 21, 22, 22, 20, 17, 13, 11, 9, 7, 6, 6, 6, 7, 7, 9, 10, 12, 14, 15, 16, 17, 18, 18, 19, 20, 21, 21, 19, 17, 13, 11, 9, 7, 6, 6, 7, 8, 9, 10, 11, 12, 13, 14, 14], 'precipitation': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}}
        buffer = OpenMeteoAdapter.get_data = MagicMock(return_value = dizionario)
        try:
            #act
            result = DecisionIntelligenceService.cercaMeteo(lat, long)
        except Exception as e:
            print(str(e))
            
        #assert that result is a dictionary and has the right keys
        self.assertIsInstance(result, dict)
        #assert that is not null
        self.assertIsNotNone(result)
        print(result)
        #assert that has lat and long keys and that they are almost equal to the ones passed
        self.assertAlmostEqual(result["latitude"], lat, delta=1)
        self.assertAlmostEqual(result["longitude"], long, delta=1)
        
        #clean up
        OpenMeteoAdapter.get_data = buffer

if __name__ == '__main__':
    unittest.main()