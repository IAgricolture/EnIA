
import os
import sys
from bson.objectid import ObjectId
sys.path.append(os.path.abspath(os.path.join('.' )))
from src.logic.DecisionIntelligence.DecisionIntelligenceService import DecisionIntelligenceService
from src.logic.GestioneEventi.GestioneEventiService import GestioneEventiService
import unittest
from unittest.mock import MagicMock
from src.logic.GestioneSchedule.GestioneScheduleService import GestioneScheduleService
from src.logic.Storage.ScheduleDAO import ScheduleDAO


class gestione_schedule_service_tests(unittest.TestCase):
    
    def test_trovaScheduleTerreno(self):
        # Arrange
        id_terreno = "id_terreno"
        buffer_schedule_dao = ScheduleDAO.getWeeklySchedule
        ScheduleDAO.getWeeklySchedule = MagicMock(return_value=[{'_id': ObjectId('63d6a4dabb3af4a7f8b38057'), 'inizio': '30-01-2023', 'fine': '30-01-2023', 'modalita': 'Nessuno', 'terreno': ObjectId('63c8641c723828186bb76298')}, {'_id': ObjectId('63d6a4dabb3af4a7f8b38058'), 'inizio': '31-01-2023', 'fine': '31-01-2023', 'modalita': 'Nessuno', 'terreno': ObjectId('63c8641c723828186bb76298')}, {'_id': ObjectId('63d6a4dabb3af4a7f8b38059'), 'inizio': '01-02-2023', 'fine': '01-02-2023', 'modalita': 'Nessuno', 'terreno': ObjectId('63c8641c723828186bb76298')}, {'_id': ObjectId('63d6a4dabb3af4a7f8b3805a'), 'inizio': '02-02-2023', 'fine': '02-02-2023', 'modalita': 'Nessuno', 'terreno': ObjectId('63c8641c723828186bb76298')}, {'_id': ObjectId('63d6a4dabb3af4a7f8b3805b'), 'inizio': '03-02-2023', 'fine': '03-02-2023', 'modalita': 'Nessuno', 'terreno': ObjectId('63c8641c723828186bb76298')}, {'_id': ObjectId('63d6a4dabb3af4a7f8b3805c'), 'inizio': '04-02-2023', 'fine': '04-02-2023', 'modalita': 'Nessuno', 'terreno': ObjectId('63c8641c723828186bb76298')}, {'_id': ObjectId('63d789d34c5aa4fddd39afb9'), 'inizio': '05-02-2023', 'fine': '05-02-2023', 'modalita': 'nessuno', 'terreno': ObjectId('63c8641c723828186bb76298')}])
        
        # Act
        result = GestioneScheduleService.trovaScheduleTerreno(id_terreno)
        # Assert
        da_aspettarsi = {'30-01-2023': 'Nessuno',
                         '31-01-2023': 'Nessuno',
                         '01-02-2023': 'Nessuno',
                         '02-02-2023': 'Nessuno',
                         '03-02-2023': 'Nessuno',
                         '04-02-2023': 'Nessuno',
                         '05-02-2023': 'nessuno'}
        self.assertEqual(result, da_aspettarsi)
        #clean
        ScheduleDAO.getWeeklySchedule = buffer_schedule_dao
        
    def test_usa_scheduling_consigliato(self):
        # Arrange
        id_terreno = "id_terreno"
        buffer_schedule_dao = ScheduleDAO.getWeeklySchedule
        buffer_eventi = GestioneEventiService.creaEvento
        
        #mock per DecisionIntelligenceService
        buffer_decision_intelligence_service = DecisionIntelligenceService.getPredizioneLivelliIrrigazione
        return_value = {'30-01-2023': 'Basso',
                        '31-01-2023': 'Medio',
                        '01-02-2023': 'Basso',
                        '02-02-2023': 'Basso',
                        '03-02-2023': 'Medio',
                        '04-02-2023': 'Medio',
                        '05-02-2023': 'Medio'}
        DecisionIntelligenceService.getPredizioneLivelliIrrigazione = MagicMock(return_value = return_value)
        ScheduleDAO.modificaLivelloSchedule = MagicMock(return_value = True)
        GestioneEventiService.creaEvento = MagicMock(return_value = True)
        #act
        result_gestione_schdule = GestioneScheduleService.usaSchedulingConsigliato(id_terreno, "12.4", "12.4", "cereale", "fase")

        #assert
        self.assertEqual(ScheduleDAO.modificaLivelloSchedule.call_count, 7)
        self.assertEqual(GestioneEventiService.creaEvento.call_count, 1)
        self.assertTrue(result_gestione_schdule)
        
        #clean
        ScheduleDAO.getWeeklySchedule = buffer_schedule_dao
        GestioneEventiService.creaEvento = buffer_eventi
        DecisionIntelligenceService.getPredizioneLivelliIrrigazione = buffer_decision_intelligence_service
        
        
if __name__ == '__main__':
    unittest.main()
        