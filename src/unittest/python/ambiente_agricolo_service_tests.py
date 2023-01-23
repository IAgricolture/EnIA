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
        # Arrange
        nome = "Terreno1"
        coltura = "Coltura1"
        posizione = "Posizione1"
        preferito = True
        priorita = 1
        proprietario = "63cec530e69b425d8b49d8df"
        stadio_crescita = "Sviluppo"
        
        #act
        risultato = AmbienteAgricoloService.aggiungiTerreno(nome, coltura,stadio_crescita, posizione, preferito, priorita, proprietario)
        
        terreni.delete_one({"Nome" : nome, "proprietario" : proprietario})
        
        #assert
        self.assertEqual(risultato, True)
        
        
        
        
        
        