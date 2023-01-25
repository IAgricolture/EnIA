import unittest
import os, sys

from mockito import mock, when
sys.path.append(os.path.abspath(os.path.join('.' )))
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
    
    def test_visualizzaTerreni(self):
        # Arrange
        farmer = "63cec530e69b425d8b49d8df"

        # Act
        terreni = AmbienteAgricoloService.visualizzaTerreni(farmer)

        # Assert
        
        self.assertEqual(terreni[0].id, "63cec54ce69b425d8b49d8e2")
        self.assertEqual(terreni[0].proprietario, "63cec530e69b425d8b49d8df")
        
    '''def test_aggiungiTerreno(self):
        #crea un mock dell'oggetto terreno usando mockito
        terreno = mock()
        #aggiungi al mock terreno l'attributo nome e assegnagli il valore "Terreno1"
        terreno.nome = "Terreno1"
        terreno.coltura = "Coltura1"
        terreno.stadio_crescita = "Sviluppo"
        terreno.posizione = "Posizione1"
        terreno.preferito = True
        terreno.priorita = 1
        terreno.proprietario = "63cec530e69b425d8b49d8df"
        
        #act
        risultato = AmbienteAgricoloService.aggiungiTerreno(terreno.nome, terreno.coltura,terreno.stadio_crescita, terreno.posizione,
                                                            terreno.preferito, terreno.priorita, terreno.proprietario)
        
        terreni.delete_one({"Nome" : terreno.nome, "proprietario" : terreno.proprietario})
        
        #assert
        self.assertEqual(risultato, True)'''
    
    #Limoni non sono una coltura valida
    #Controllo colture non dovrebbe essere il formato ma se esistono tra quelle preinserite
       
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
        
        
