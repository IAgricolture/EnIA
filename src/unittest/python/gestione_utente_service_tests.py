import unittest
import os, sys

from mockito import mock, verify
sys.path.append(os.path.abspath(os.path.join('.' )))
from src.logic.Storage.AutenticazioneDAO import AutenticazioneDAO
from src.logic.Utente.GestioneUtenteService import GestioneUtenteService

farmer = "63b9e6a27862c31f1f7b221f"
ruoli = ["irrigation manager", "pollution analyst"]

class GestioneUtenteServiceTest(unittest.TestCase):

    def test_case_1_3_1(self):

        ruolo = "zappatore"

        risultato = GestioneUtenteService.GenerateCode(ruolo, farmer)

        self.assertEqual("Error", risultato)

    def test_case_1_3_2(self):

        risultato = GestioneUtenteService.GenerateCode(ruoli[0], farmer)

        self.assertNotEqual("Error", risultato)

        AutenticazioneDAO.eliminaUtente(AutenticazioneDAO.trovaUtenteByCodiceDiAccesso(risultato).id)

    def test_visualizza_dipendenti(self):
        
        dipendenti = GestioneUtenteService.getUtenti(farmer)
        
        for dipendente in dipendenti:
            self.assertEqual(farmer, dipendente.get("datore"))

    def test_aggiunta_codice_accesso(self):

        codice = GestioneUtenteService.GenerateCode(ruoli[0], farmer)

        self.assertEqual(codice, AutenticazioneDAO.trovaUtenteByCodiceDiAccesso(codice).codice)

        AutenticazioneDAO.eliminaUtente(AutenticazioneDAO.trovaUtenteByCodiceDiAccesso(codice).id)

    def test_rimozione_utente_from_azienda(self):

        codice = GestioneUtenteService.GenerateCode(ruoli[0], farmer)

        risultato = GestioneUtenteService.removeUtenteFromAzienda(AutenticazioneDAO.trovaUtenteByCodiceDiAccesso(codice).id)

        self.assertTrue(risultato)

        self.assertIsNone(AutenticazioneDAO.trovaUtenteByCodiceDiAccesso(codice))


        



        