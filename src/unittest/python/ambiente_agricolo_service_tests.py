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
    
    #Oracolo:Inserimento fallito perchè la posizione è nulla
    def test_aggiungiTerreno_TC_2_1_5(self):
        print("TC_2_1_5")
        nome = "Terreno-A"
        coltura = "Limoni"
        posizione = None
        preferito = True
        priorita = 15
        proprietario = "63b9e6a27862c31f1f7b221f"
        stadio_crescita = "Sviluppo"
        risultato = AmbienteAgricoloService.aggiungiTerreno(nome, coltura, stadio_crescita, posizione, preferito, priorita, proprietario)
        self.assertEqual(risultato["esitoOperazione"], False)

    #ORACOLO: Fallisce in quanto manca la posizione
    def test_aggiungiTerreno_TC_2_1_8(self):
        print("TC_2_1_5")
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
    def test_aggiungiTerreno_TC_2_1_6(self):
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
    
    #ORACOLO: Fallito a causa del tipo sbagliato di preferito, che dovrebbe essere un bool e non un int.
    def test_aggiungiTerreno_TC_2_1_7(self):
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

    #Oracolo : Fallito a causa del tipo sbagliato di crescita
    def test_aggiungiTerreno_TC_2_1_8(self):
        print("TC_2_1_8")
        nome = "Terreno-A"
        coltura = "Limoni"
        posizione = {"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[14.783607,40.772225],[14.783735,40.772745],[14.784594,40.771965],[14.783607,40.772225]]]}}
        preferito = True
        priorita = 15
        proprietario = "63b9e6a27862c31f1f7b221f"
        stadio_crescita = 45
        AmbienteAgricoloService.aggiungiTerreno(nome, coltura, stadio_crescita, posizione, preferito, priorita, proprietario)
        self.assertRaises(TypeError)
   
    #ORACOLO: Inserimento va a buon fine in quanto tutti i campi sono corretti.
    def test_aggiungiTerreno_TC_2_1_9(self):
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
    
 
    
if __name__ == '__main__':
    unittest.main()