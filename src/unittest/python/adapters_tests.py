import os
import sys
import unittest
import requests_mock


sys.path.append(os.path.abspath(os.path.join('.' )))
from src.logic.Adapters.OpenMeteoAdapter import OpenMeteoAdapter
from src.logic.Adapters.IAdapter import IAdapter
class TestIAdapter(unittest.TestCase):
    def setUp(self):
        self.valid_lat = 45.0
        self.valid_lon = 90.0
        self.valid_crop = "Orzo"
        self.translated_crop = "Barley"
        self.valid_stage = "Sviluppo"
        self.translated_stage = "CropDevStage"
        self.invalid_lat = 91.0
        self.invalid_lon = 181.0
        self.invalid_crop = "banana"
        self.invalid_stage = "germoglione"

    def test_valid_input(self):
        info = IAdapter(self.valid_lat, self.valid_lon, self.valid_crop, self.valid_stage)
        self.assertEqual(info.lat, self.valid_lat)
        self.assertEqual(info.lon, self.valid_lon)
        self.assertEqual(info.crop, self.translated_crop)
        self.assertEqual(info.stage, self.translated_stage)

    def test_invalid_lat(self):
        with self.assertRaises(Exception) as context:
            IAdapter(self.invalid_lat, self.valid_lon, self.valid_crop, self.valid_stage)
        self.assertEqual(str(context.exception), "Latitudine o longitudine non valide")

    def test_invalid_lon(self):
        with self.assertRaises(Exception) as context:
            IAdapter(self.valid_lat, self.invalid_lon, self.valid_crop, self.valid_stage)
        self.assertEqual(str(context.exception), "Latitudine o longitudine non valide")

    def test_invalid_crop(self):
        with self.assertRaises(Exception) as context:
            IAdapter(self.valid_lat, self.valid_lon, self.invalid_crop, self.valid_stage)
        self.assertEqual(str(context.exception), "Coltura non valida")

    def test_invalid_stage(self):
        with self.assertRaises(Exception) as context:
            IAdapter(self.valid_lat, self.valid_lon, self.valid_crop, self.invalid_stage)
        self.assertEqual(str(context.exception), "Stadio di crescita non valido")

    def test_none_value(self):
        with self.assertRaises(Exception) as context:
            IAdapter(None, self.valid_lon, self.valid_crop, self.valid_stage)
        self.assertEqual(str(context.exception), "None value not allowed")
        with self.assertRaises(Exception) as context:
            IAdapter(self.valid_lat, None, self.valid_crop, self.valid_stage)
        self.assertEqual(str(context.exception), "None value not allowed")
        with self.assertRaises(Exception) as context:
            IAdapter(self.valid_lat, self.valid_lon, None, self.valid_stage)
        self.assertEqual(str(context.exception), "Coltura non valida")
        with self.assertRaises(Exception) as context:
            IAdapter(self.valid_lat, self.valid_lon, self.valid_crop, None)
        self.assertEqual(str(context.exception), "Stadio di crescita non valido")
        
    def test_get_ai_prediction(self):
        # Arrange
        mock_response = {
            "irrigationLevel": [1, 1, 1, 1, 1, 1, 1]
        }
        with requests_mock.Mocker() as m:
            m.get("https://benedettoscala.pythonanywhere.com/getIrrigationDecision?"
                  "lat=0&lon=0&crop=Barley&growthStage=CropDevStage",
                  json=mock_response)

            # Act
            adapter = IAdapter(0, 0, self.valid_crop, self.valid_stage)
            result = adapter.getAiPrediction()

            # Assert
            expected_result = {
                '04-02-2023': 'Basso',
                '05-02-2023': 'Basso',
                '06-02-2023': 'Basso',
                '07-02-2023': 'Basso',
                '08-02-2023': 'Basso',
                '09-02-2023': 'Basso',
                '10-02-2023': 'Basso'
            }
            self.assertEqual(result, expected_result)
class TestOpenMeteoAdapter(unittest.TestCase):
    def test_valid_lat_lon(self):
        # Arrange
        lat = 45
        lon = 120

        # Act
        
        result = OpenMeteoAdapter(lat, lon)

        # Assert
        self.assertEqual(result.lat, lat)
        self.assertEqual(result.lon, lon)

    def test_invalid_lat(self):
        # Arrange
        lat = 91
        lon = 120

        # Act & Assert
        with self.assertRaises(Exception) as context:
            OpenMeteoAdapter(lat, lon)
        self.assertEqual(str(context.exception), "Latitudine non valida")

    def test_invalid_lon(self):
        # Arrange
        lat = 45
        lon = 181

        # Act & Assert
        with self.assertRaises(Exception) as context:
            OpenMeteoAdapter(lat, lon)
        self.assertEqual(str(context.exception), "Longitudine non valida")
        
    def test_get_data(self):
        # Arrange
        lat = 45
        lon = 120
        my_class = OpenMeteoAdapter(lat, lon)
        expected_data = {"temperature_2m": [], "relativehumidity_2m": [], "precipitation": []}
        
        with requests_mock.Mocker() as m:
            m.get("https://api.open-meteo.com/v1/forecast?latitude="+str(lat)+"&longitude="+str(lon)+ "&hourly=temperature_2m,relativehumidity_2m,precipitation", json=expected_data)
            
            # Act
            result = my_class.get_data()

            # Assert
            self.assertEqual(result, expected_data)
if __name__ == '__main__':
    unittest.main()