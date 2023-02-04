import os
import sys
import unittest
import requests_mock

sys.path.append(os.path.abspath(os.path.join('.' )))
from src.logic.Adapters.SenseSquareAdapter import SenseSquareAdapter
from src.logic.Adapters.OpenMeteoAdapter import OpenMeteoAdapter
from src.logic.Adapters.NominatimAdapter import NominatimAdapter
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
            
class TestNominatimAdapter(unittest.TestCase):
    
    def setUp(self) -> None:
        self.valid_lat = 0
        self.valid_lon = 0
        self.valid_format = "json"
        self.valid_zoom = 0
        self.invalid_lat = 91
        self.invalid_lon = 181
        self.invalid_format = "invalid"
        self.invalid_zoom = "ss"
    
    def test_valid(self):
        # test valid nominatim adapter doesn't raise exception
        NominatimAdapter(self.valid_lat, self.valid_lon, self.valid_format, self.valid_zoom)
    
    def test_invalid_latitude(self):
        # test invalid latitude
        with self.assertRaises(Exception) as context:
            NominatimAdapter(self.invalid_lat, 0, "json", 0)
        self.assertEqual(str(context.exception), "Latitudine o longitudine non valide")

    def test_invalid_longitude(self):
        # test invalid longitude
        with self.assertRaises(Exception) as context:
            NominatimAdapter(0, self.invalid_lon, "json", 0)
        self.assertEqual(str(context.exception), "Latitudine o longitudine non valide")

    def test_invalid_format(self):
        # test invalid format
        with self.assertRaises(Exception) as context:
            NominatimAdapter(0, 0, self.invalid_format, 0)
        self.assertEqual(str(context.exception), "Formato non valido")

    def test_invalid_zoom(self):
        # test invalid zoom
        with self.assertRaises(Exception) as context:
            NominatimAdapter(0, 0, "json", self.invalid_zoom)
        self.assertEqual(str(context.exception), "Zoom non valido")
        
    def test_get_data(self):
        # simulate response from Nominatim API
        with requests_mock.Mocker() as m:
            m.get("https://nominatim.openstreetmap.org/reverse", json={"key1": "value1", "key2": "value2"})

            # test get_data method
            nominatim_adapter = NominatimAdapter(0, 0, "json", 0)
            result = nominatim_adapter.get_data()
            self.assertEqual(result, {"key1": "value1", "key2": "value2"})

class SenseSquareAdapterTest(unittest.TestCase):
    def setUp(self):
        self.valid_nazione = "Italy"
        self.valid_regione = "Lombardy"
        self.valid_provincia = "Milan"
        self.valid_comune = "Milan"
        self.valid_start_date = "2022-01-01"
        self.valid_end_date = "2022-12-31"
        self.valid_formato = "json"
        self.invalid_nazione = "invalid"
        self.invalid_regione = "invalid"
        self.invalid_provincia = "invalid"
        self.invalid_comune = "invalid"
        self.invalid_start_date = "invalid"
        self.invalid_end_date = "invalid"
        self.invalid_formato = "invalid"
    
    def test_init(self):
        nazione = "Italy"
        regione = "Lombardy"
        provincia = "Milan"
        comune = "Milan"
        start_date = "2022-01-01"
        end_date = "2022-12-31"
        formato = "json"
        
        adapter = SenseSquareAdapter(nazione, regione, provincia, comune, start_date, end_date, formato)
        
        self.assertEqual(adapter.nazione, nazione)
        self.assertEqual(adapter.regione, regione)
        self.assertEqual(adapter.provincia, provincia)
        self.assertEqual(adapter.comune, comune)
        self.assertEqual(adapter.start_date, start_date)
        self.assertEqual(adapter.end_date, end_date)
        self.assertEqual(adapter.formato, formato)
    
    def test_get_data_for_today(self):
        adapter = SenseSquareAdapter("valid_nation", "valid_regione", "valid_provincia", "valid_comune")
        with requests_mock.Mocker() as m:
            m.post('https://square.sensesquare.eu:5001/placeView', json={'response_code': 200, 'message': 'Success', 'result': '{data}'})
            data = adapter.get_data_for_today()
            self.assertEqual(data, {'response_code': 200, 'message': 'Success', 'result': '{data}'})
    
    def test_invalid_get_data_for_today(self):
        adapter = SenseSquareAdapter("invalid_nation", "valid_regione", "valid_provincia", "valid_comune")
        with self.assertRaises(Exception) as context:
            adapter.get_data_for_today()
        self.assertEqual("Impossibile soddisfare questa richiesta", str(context.exception))
        
    def test_get_data_time_interval(self):
        with requests_mock.Mocker() as mock:
            mock.post('https://square.sensesquare.eu:5001/download', json={'response_code': 200, 'message': 'Success', 'result': 'test_response'})
            # Assume that self.start_date, self.end_date, and self.formato are set to appropriate values
            adapter = SenseSquareAdapter("valid_nation", "valid_regione", "valid_provincia", "valid_comune", self.valid_start_date, self.valid_end_date, self.valid_formato)
            
            # Test the case when the response code is not 400
            result = adapter.get_data_time_interval()
            #assert that result is an array
            self.assertEqual(result, [])

            # Test the case when the response code is 400
            mock.post('https://square.sensesquare.eu:5001/download', json={'response_code': 400})
            with self.assertRaises(Exception) as context:
                result = adapter.get_data_time_interval()
            self.assertEqual(str(context.exception), 'Impossibile soddisfare questa richiesta')

            # Test the case when start_date or end_date is None
            self.start_date = None
            with self.assertRaises(Exception) as context:
                result = adapter.get_data_time_interval()
            self.assertEqual(str(context.exception), 'Impossibile soddisfare questa richiesta')

if __name__ == '__main__':
    unittest.main()