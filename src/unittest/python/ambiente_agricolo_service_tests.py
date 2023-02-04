import unittest
import os, sys
from unittest.mock import MagicMock, Mock
from bson import ObjectId
from mockito import mock, patch, when



sys.path.append(os.path.abspath(os.path.join('.' )))
from src.logic.Adapters.OpenMeteoAdapter import OpenMeteoAdapter
from src.logic.GestioneEventi import GestioneEventiService
from src.logic.Storage.ImpiantoDiIrrigazioneDAO import ImpiantoDiIrrigazioneDAO
from src.logic.Adapters.NominatimAdapter import NominatimAdapter
from src.logic.Storage.TerrenoDAO import TerrenoDAO
from src.logic.AmbienteAgricolo.AmbienteAgricoloService import AmbienteAgricoloService
from src.dbConnection import terreni
from src.logic.model.Terreno import Terreno

"""
    IMPORTANTISSIMO: QUESTE SONO SOLO TEST DI ESEMPIO, QUANDO INZIEREMO A FARLI DOBBIAMO TASSATIVAMENTE
    SEGUIRE IL TCS
"""
class AmbienteAgricoloServiceTest(unittest.TestCase):
    
    # Arrange
    
    def test_visualizza_terreni(self):
        # Creare una lista fittizia di oggetti Terreno
        fake_terreni = [Terreno(1, "Terreno 1", "Pomodoro", "Semina", (10, 20), True, 1, "Farmer 1"),
                        Terreno(2, "Terreno 2", "Zucchine", "Fiore", (30, 40), False, 2, "Farmer 1"),
                        Terreno(3, "Terreno 3", "Fragole", "Frutto", (50, 60), True, 3, "Farmer 2")]
        
        # Sovrascrivere il metodo restituisciTerreniByFarmer per restituire sempre la lista fittizia
        def mock_restituisciTerreniByFarmer(farmer):
            # quando passi il farmer 1 restituisci il primo e il secondo terreno
            if farmer == "Farmer 1":
                return [fake_terreni[0], fake_terreni[1]]
            else:
                return [fake_terreni[2]]
        buffer = TerrenoDAO.restituisciTerreniByFarmer
        TerrenoDAO.restituisciTerreniByFarmer = mock_restituisciTerreniByFarmer
        
        # quando passi il farmer 1 restituisci il primo e il secondo terreno
        
        
        # Testare il metodo visualizzaTerreni per il proprietario "Farmer 1"
        terreni = AmbienteAgricoloService.visualizzaTerreni("Farmer 1")
        print("prova" + str(terreni))
        self.assertEqual(terreni, [fake_terreni[0], fake_terreni[1]])
        
        # Testare il metodo visualizzaTerreni per il proprietario "Farmer 2"
        terreni = AmbienteAgricoloService.visualizzaTerreni("Farmer 2")
        self.assertEqual(terreni, [fake_terreni[2]])
        TerrenoDAO.restituisciTerreniByFarmer = buffer
    
    def test_trova_terreno(self):
        # Creare un oggetto fittizio di Terreno
        fake_terreno = Terreno(1, "Terreno 1", "Pomodoro", "Semina", (10, 20), True, 1, "Farmer 1")
        
        # Sovrascrivere il metodo TrovaTerreno per restituire sempre l'oggetto fittizio
        def mock_TrovaTerreno(id):
            return fake_terreno
        buffer = TerrenoDAO.TrovaTerreno
        TerrenoDAO.TrovaTerreno = mock_TrovaTerreno
        
        # Testare il metodo trovaTerreno per l'identificatore "1"
        terreno = AmbienteAgricoloService.trovaTerreno("1")
        self.assertEqual(terreno, fake_terreno)
        TerrenoDAO.TrovaTerreno = buffer
        
    def test_cercaPosizione(self):
        # Dati di test fittizi per l'oggetto Terreno
        #get a 12 byte string
        id = ObjectId()
        
        dict ={
            "type": "Feature",
            "properties": {},
            "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                [
                    14.512253,
                    40.811619
                ],
                [
                    14.519634,
                    40.813957
                ],
                [
                    14.523411,
                    40.807851
                ],
                [
                    14.514484,
                    40.802653
                ],
                [
                    14.512253,
                    40.811619
                ]
                ]
            ]
            }
        }
        terreno = Terreno(id, "Terreno di prova", "Pomodori", "Semina",dict, False, 1, "Farmer1")
        # Creare una mock del metodo TrovaTerreno su TerrenoDAO
        bufferTrovaTerreno = TerrenoDAO.TrovaTerreno
        TerrenoDAO.TrovaTerreno = unittest.mock.Mock(return_value=terreno)

        # Creare una mock del metodo get_data su NominatimAdapter
        nominatim_mock = Mock()
        nominatim_mock.get_data.return_value = "posizione"
        NominatimAdapter.return_value = nominatim_mock

        # Chiamare il metodo da testare e verificare il risultato
        risultato = AmbienteAgricoloService.cercaPosizione(id)
        print(risultato)
        #cut place_id, license and osm_id from result
        risultato.pop('place_id')
        risultato.pop('licence')
        risultato.pop('osm_id')
        risultatodaaspettarsi = {'osm_type': 'relation','lat': '40.829811', 'lon': '14.504436', 'display_name': 'San Giuseppe Vesuviano, Napoli, Campania, Italia', 'address': {'town': 'San Giuseppe Vesuviano', 'county': 'Napoli', 'ISO3166-2-lvl6': 'IT-NA', 'state': 'Campania', 'ISO3166-2-lvl4': 'IT-72', 'country': 'Italia', 'country_code': 'it'}, 'boundingbox': ['40.8048817', '40.8449205', '14.4457768', '14.5322165']}
        self.assertEqual(risultato, risultatodaaspettarsi)
        TerrenoDAO.TrovaTerreno = bufferTrovaTerreno
    
    def test_modificaTerreno(self):
        # Arrange
        id = ObjectId()
        nome = "Terreno A"
        coltura = "Mais"
        stadio_crescita = "Fine Stagione"
        dict = dict ={
            "type": "Feature",
            "properties": {},
            "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                [
                    14.512253,
                    40.811619
                ],
                [
                    14.519634,
                    40.813957
                ],
                [
                    14.523411,
                    40.807851
                ],
                [
                    14.514484,
                    40.802653
                ],
                [
                    14.512253,
                    40.811619
                ]
                ]
            ]
            }
        }
        posizione = {"type": "Polygon", "coordinates": [[[-75.343, 39.984], [-75.534, 39.123], [-75.243, 39.243]]]}
        preferito = True
        priorita = 2
        proprietario = "Mario Rossi"

        modificaTerreno_mock = Mock()
        modificaTerreno_mock.return_value.matched_count = 1
        buffer = TerrenoDAO.modificaTerreno
        TerrenoDAO.modificaTerreno = modificaTerreno_mock
        
        modificaTerreno_mock.return_value.matched_count = 1

        # Act
        result = AmbienteAgricoloService.modificaTerreno(id, nome, coltura, stadio_crescita, posizione, preferito, priorita, proprietario)

        # Assert
        self.assertTrue(result)
        TerrenoDAO.modificaTerreno = buffer
    
    def test_aggiungiIrrigatore(self):
        id_terreno = ObjectId()
        id_irr = ObjectId()
        nome_irrigatore = "Irrigatore1"
        posizione_irrigatore = "Posizione1"
        aggiungi_irrigatore_mock = Mock()
        aggiungi_irrigatore_mock.return_value = id_irr
        creaEvento_mock = Mock()
        
        bufferIrrDao = ImpiantoDiIrrigazioneDAO.creaImpianto
        ImpiantoDiIrrigazioneDAO.creaImpianto = aggiungi_irrigatore_mock
        bufferEventi = GestioneEventiService.GestioneEventiService.creaEvento
        GestioneEventiService.GestioneEventiService.creaEvento = creaEvento_mock
        id = AmbienteAgricoloService.aggiungiIrrigatore(ObjectId(), nome_irrigatore, posizione_irrigatore)
        
        self.assertEquals(id, id_irr)
        
        ImpiantoDiIrrigazioneDAO.creaImpianto = bufferIrrDao
        GestioneEventiService.GestioneEventiService.creaEvento = bufferEventi
    
    def test_modifica_irrigatore(self):
        buffer = ImpiantoDiIrrigazioneDAO.modificaImpianto
        ImpiantoDiIrrigazioneDAO.modificaImpianto = Mock()
        result = AmbienteAgricoloService.modificaIrrigatore(ObjectId(), "Irrigatore1", "Posizione1")
        
        self.assertTrue(result)
        ImpiantoDiIrrigazioneDAO.modificaImpianto = buffer

       
    #Limoni non sono una coltura valida
    #Controllo colture non dovrebbe essere il formato ma se esistono tra quelle preinserite
    
    def test_eliminaTerreno(self):
        print("Elimina Terreno")
        #Creo il Terreno
        nome = "Terreno-B"
        coltura = "Orzo"
        posizione = {"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[14.783607,40.772225],[14.783735,40.772745],[14.784594,40.771965],[14.783607,40.772225]]]}}
        preferito = True
        priorita = 15
        proprietario = "63b9e6a27862c31f1f7b221f"
        stadio_crescita = "Sviluppo"
        risultato = AmbienteAgricoloService.aggiungiTerreno(nome, coltura, stadio_crescita, posizione, preferito, priorita, proprietario)
        print(risultato["restituito"])
        #Elimino il Terreno
        risultato2 = AmbienteAgricoloService.eliminaTerreno(risultato["restituito"]) 
        self.assertTrue(risultato2) #Eliminazione Riuscita
       
    #ORACOLO: Inserimento fallisce per formato del nome errato       
    def test_aggiungiTerreno_TC_2_1_1(self):
        print("TC_2_1_1")
        nome = "Ç?(&%U"
        coltura = "Orzo" 
        posizione = {"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[14.783607,40.772225],[14.783735,40.772745],[14.784594,40.771965],[14.783607,40.772225]]]}}
        preferito = True
        priorita = 15
        proprietario = "63b9e6a27862c31f1f7b221f"
        stadio_crescita = "Sviluppo"
        risultato = AmbienteAgricoloService.aggiungiTerreno(nome, coltura, stadio_crescita, posizione, preferito, priorita, proprietario)
        print(risultato)
        self.assertEqual(risultato["esitoOperazione"], False)  #Fallito inserimento
        self.assertEqual(risultato["nomeNonValido"], True) #Fallito a causa del formato del nome
   
    #ORACOLO: Inserimento fallisce per nome mancante
    def test_aggiungiTerreno_TC_2_1_2(self):
        print("TC_2_1_2")
        nome = ""
        coltura = "Orzo"
        posizione = {"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[14.783607,40.772225],[14.783735,40.772745],[14.784594,40.771965],[14.783607,40.772225]]]}}
        preferito = True
        priorita = 15
        proprietario = "63b9e6a27862c31f1f7b221f"
        stadio_crescita = "Sviluppo"
        risultato = AmbienteAgricoloService.aggiungiTerreno(nome, coltura, stadio_crescita, posizione, preferito, priorita, proprietario)
        print(risultato)
        self.assertEqual(risultato["esitoOperazione"], False)  #Fallito inserimento
        self.assertEqual(risultato["nomeNonValido"], True) #Fallito a causa della mancanza del nome     
    
    #ORACOLO: Inserimento fallisce per mancanza di coltura
    def test_aggiungiTerreno_TC_2_1_3(self):
        print("TC_2_1_3")
        nome = "Terreno-A"
        coltura = ""
        posizione = {"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[14.783607,40.772225],[14.783735,40.772745],[14.784594,40.771965],[14.783607,40.772225]]]}}
        preferito = True
        priorita = 15
        proprietario = "63b9e6a27862c31f1f7b221f"
        stadio_crescita = "Sviluppo"
        risultato = AmbienteAgricoloService.aggiungiTerreno(nome, coltura, stadio_crescita, posizione, preferito, priorita, proprietario)
        print(risultato)
        self.assertEqual(risultato["esitoOperazione"], False)  #Fallito inserimento
        self.assertEqual(risultato["colturaNonValida"], True) #Fallito a causa della mancanza della coltura
    
    #ORACOLO: Inserimento fallisce per formato invalido di coltura
    def test_aggiungiTerreno_TC_2_1_4(self):
        print("TC_2_1_4")
        nome = "Terreno-A"
        coltura = "*çéçé=("
        posizione = {"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[14.783607,40.772225],[14.783735,40.772745],[14.784594,40.771965],[14.783607,40.772225]]]}}
        preferito = True
        priorita = 15
        proprietario = "63b9e6a27862c31f1f7b221f"
        stadio_crescita = "Sviluppo"
        risultato = AmbienteAgricoloService.aggiungiTerreno(nome, coltura, stadio_crescita, posizione, preferito, priorita, proprietario)
        print(risultato)
        self.assertEqual(risultato["esitoOperazione"], False)  #Fallito inserimento
        self.assertEqual(risultato["colturaNonValida"], True) #Fallito a causa del formato sbagliato della coltura 
    
    #ORACOLO: Inserimento fallisce per formato invalido di coltura 
    #Si potrebbe eliminare in quanto una ripetizione del 4, stessi controlli.
    def test_aggiungiTerreno_TC_2_1_5(self):
        print("TC_2_1_5")
        nome = "Terreno-A"
        coltura = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap intoele"
        posizione = {"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[14.783607,40.772225],[14.783735,40.772745],[14.784594,40.771965],[14.783607,40.772225]]]}}
        preferito = True
        priorita = 15
        proprietario = "63b9e6a27862c31f1f7b221f"
        stadio_crescita = "Sviluppo"
        risultato = AmbienteAgricoloService.aggiungiTerreno(nome, coltura, stadio_crescita, posizione, preferito, priorita, proprietario)
        print(risultato)
        self.assertEqual(risultato["esitoOperazione"], False)  #Fallito inserimento
        self.assertEqual(risultato["colturaNonValida"], True) #Fallito a causa del formato sbagliato della coltura                                   
        
    #2_1_6, 2_1_7 non si possono fare perchè la dimensione del terreno non esiste più.
    
    #ORACOLO: Fallisce in quanto manca la posizione
    def test_aggiungiTerreno_TC_2_1_8(self):
        print("TC_2_1_8")
        nome = "Terreno-A"
        coltura = "Limoni"
        posizione = {}
        preferito = True
        priorita = 15
        proprietario = "63b9e6a27862c31f1f7b221f"
        stadio_crescita = "Sviluppo"
        risultato = AmbienteAgricoloService.aggiungiTerreno(nome, coltura, stadio_crescita, posizione, preferito, priorita, proprietario)
        print(risultato)
        self.assertEqual(risultato["esitoOperazione"], False)  #Fallito inserimento
        self.assertEqual(risultato["posizioneNonValida"], True) #Fallito a causa dell'assenza della posizione
   
    #ORACOLO: Fallito per il formato sbagliato della posizione
    def test_aggiungiTerreno_TC_2_1_9(self):
        print("TC_2_1_9")
        nome = "Terreno-A"
        coltura = "Limoni"
        posizione = {"type": "FeatureCollection","features": [{"type": "Feature","properties": {},"geometry": {"coordinates": [[12.682885346272485,42.42118547557695],[12.683224252299652,42.421660820429594]],"type": "LineString"}}]}
        preferito = True
        priorita = 15
        proprietario = "63b9e6a27862c31f1f7b221f"
        stadio_crescita = "Sviluppo"
        risultato = AmbienteAgricoloService.aggiungiTerreno(nome, coltura, stadio_crescita, posizione, preferito, priorita, proprietario)
        print(risultato)
        self.assertEqual(risultato["esitoOperazione"], False)  #Fallito inserimento
        self.assertEqual(risultato["posizioneNonValida"], True) #Fallito a causa del formato sbagliato della posizione
    
    #2_1_10 è per preferito e non per priorità, va cambiato nel TCS.
    
    #ORACOLO: Fallito a causa del tipo sbagliato di preferito, che dovrebbe essere un bool e non un int.
    def test_aggiungiTerreno_TC_2_1_10(self):
        print("TC_2_1_10")
        nome = "Terreno-A"
        coltura = "Limoni"
        posizione = {"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[14.783607,40.772225],[14.783735,40.772745],[14.784594,40.771965],[14.783607,40.772225]]]}}
        preferito = 45
        priorita = 15
        proprietario = "63b9e6a27862c31f1f7b221f"
        stadio_crescita = "Sviluppo"
        risultato = AmbienteAgricoloService.aggiungiTerreno(nome, coltura, stadio_crescita, posizione, preferito, priorita, proprietario)
        print(risultato)
        self.assertRaises(TypeError)
    
    #Necessario cambiare coltura da Limoni ad Orzo nel Test Case
    #ORACOLO: Inserimento va a buon fine in quanto tutti i campi sono corretti.
    def test_aggiungiTerreno_TC_2_1_11(self):
        print("TC_2_1_11")
        nome = "Terreno-A"
        coltura = "Orzo"
        posizione = {"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[14.783607,40.772225],[14.783735,40.772745],[14.784594,40.771965],[14.783607,40.772225]]]}}
        preferito = True
        priorita = 15
        proprietario = "63b9e6a27862c31f1f7b221f"
        stadio_crescita = "Sviluppo"
        risultato = AmbienteAgricoloService.aggiungiTerreno(nome, coltura, stadio_crescita, posizione, preferito, priorita, proprietario)
        print(risultato)
        AmbienteAgricoloService.eliminaTerreno(risultato["restituito"])        
        self.assertEqual(risultato["esitoOperazione"], True)  #Inserimento riesce
    
    #TEST VISUALIZZAZIONE METEO
    
    def test_visualizza_meteo_tc_3_1_1(self):
        print("TC_3_1_1")
        
        #arrange
        long = 190
        lat = 12.2
        
        try:
            #act
            AmbienteAgricoloService.cercaMeteo(lat, long)
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
            AmbienteAgricoloService.cercaMeteo(lat, long)
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
            result = AmbienteAgricoloService.cercaMeteo(lat, long)
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