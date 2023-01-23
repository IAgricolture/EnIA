import unittest
import os, sys

from mockito import mock, when
sys.path.append(os.path.abspath(os.path.join('.' )))
from src.logic.Storage.TerrenoDAO import TerrenoDAO
from src.logic.AmbienteAgricolo.AmbienteAgricoloService import AmbienteAgricoloService
from src.dbConnection import terreni

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
        
    def test_aggiungiTerreno(self):
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
        self.assertEqual(risultato, True)
        
        
        
        
        
        