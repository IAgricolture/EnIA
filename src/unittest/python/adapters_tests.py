import datetime
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
    """classe di test per IAdapter
    """
    def setUp(self):
        """
        Inizializza i valori di test
        """
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
        """
        Testa l'init di IAdapter con valori validi
        """
        info = IAdapter(self.valid_lat, self.valid_lon, self.valid_crop, self.valid_stage)
        self.assertEqual(info.lat, self.valid_lat)
        self.assertEqual(info.lon, self.valid_lon)
        self.assertEqual(info.crop, self.translated_crop)
        self.assertEqual(info.stage, self.translated_stage)

    def test_invalid_lat(self):
        """
        Testa l'init di IAdapter con la latitudine non valida
        """
        with self.assertRaises(Exception) as context:
            IAdapter(self.invalid_lat, self.valid_lon, self.valid_crop, self.valid_stage)
        self.assertEqual(str(context.exception), "Latitudine o longitudine non valide")

    def test_invalid_lon(self):
        """
        Testa l'init di IAdapter con la longitudine non valida
        """
        with self.assertRaises(Exception) as context:
            IAdapter(self.valid_lat, self.invalid_lon, self.valid_crop, self.valid_stage)
        self.assertEqual(str(context.exception), "Latitudine o longitudine non valide")

    def test_invalid_crop(self):
        """
        Testa l'init di IAdapter con la coltura non valida
        """
        with self.assertRaises(Exception) as context:
            IAdapter(self.valid_lat, self.valid_lon, self.invalid_crop, self.valid_stage)
        self.assertEqual(str(context.exception), "Coltura non valida")

    def test_invalid_stage(self):
        """
        Testa l'init di IAdapter con lo stadio di crescita non valido
        """
        with self.assertRaises(Exception) as context:
            IAdapter(self.valid_lat, self.valid_lon, self.valid_crop, self.invalid_stage)
        self.assertEqual(str(context.exception), "Stadio di crescita non valido")

    def test_none_value(self):
        """
        Testa l'init di IAdapter con valori None
        """
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
        """
        Testa il metodo getAiPrediction
        """
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
            #get today's date
            today = datetime.date.today()
            #get the date of the next 7 days
            date_list = [today + datetime.timedelta(days=x) for x in range(7)]
            #format the date
            date_list = [x.strftime("%d-%m-%Y") for x in date_list]
            #create the expected result
            expected_result = dict(zip(date_list, mock_response["irrigationLevel"]))
            #substitute 1 with "Basso"
            expected_result = {k: "Basso" if v == 1 else v for k, v in expected_result.items()}
            self.assertEqual(result, expected_result)

class TestOpenMeteoAdapter(unittest.TestCase):
    """
    Testa la classe OpenMeteoAdapter
    """
    def test_valid_lat_lon(self):
        """
        Testa l'init di OpenMeteoAdapter con valori validi di latitudine
        e longitudine
        """
        # Arrange
        lat = 45
        lon = 120

        # Act
        
        result = OpenMeteoAdapter(lat, lon)

        # Assert
        self.assertEqual(result.lat, lat)
        self.assertEqual(result.lon, lon)

    def test_invalid_lat(self):
        """
        Testa l'init di OpenMeteoAdapter con la latitudine non valida
        """
        # Arrange
        lat = 91
        lon = 120

        # Act & Assert
        with self.assertRaises(Exception) as context:
            OpenMeteoAdapter(lat, lon)
        self.assertEqual(str(context.exception), "Latitudine non valida")

    def test_invalid_lon(self):
        """
        Testa l'init di OpenMeteoAdapter con la longitudine non valida
        """
        # Arrange
        lat = 45
        lon = 181

        # Act & Assert
        with self.assertRaises(Exception) as context:
            OpenMeteoAdapter(lat, lon)
        self.assertEqual(str(context.exception), "Longitudine non valida")
        
    def test_get_data(self):
        """
        Testa il metodo get_data che restituisce i dati meteo
        dei prossimi 7 giorni
        """
        # Arrange
        lat = 45
        lon = 120
        my_class = OpenMeteoAdapter(lat, lon)
        expected_data = {"temperature_2m": [], "relativehumidity_2m": [], "precipitation": []}
        #mock sulla risposta della get
        with requests_mock.Mocker() as m:
            m.get("https://api.open-meteo.com/v1/forecast?latitude="+str(lat)+"&longitude="+str(lon)+ "&hourly=temperature_2m,relativehumidity_2m,precipitation", json=expected_data)
            
            # Act
            result = my_class.get_data()

            # Assert that it returns an istance of dict
            self.assertIsInstance(result, dict)

            
class TestNominatimAdapter(unittest.TestCase):
    """
    Testa la classe NominatimAdapter
    """
    def setUp(self) -> None:
        """
        Inizializza i valori validi e invalidi per i test
        """
        self.valid_lat = 0
        self.valid_lon = 0
        self.valid_format = "json"
        self.valid_zoom = 0
        self.invalid_lat = 91
        self.invalid_lon = 181
        self.invalid_format = "invalid"
        self.invalid_zoom = "ss"
    
    def test_valid(self):
        """
        Testa l'init di NominatimAdapter con valori validi
        """
        # test valid nominatim adapter doesn't raise exception
        NominatimAdapter(self.valid_lat, self.valid_lon, self.valid_format, self.valid_zoom)
    
    def test_invalid_latitude(self):
        """
        Testa l'init di NominatimAdapter con la latitudine non valida
        """
        # test invalid latitude
        with self.assertRaises(Exception) as context:
            NominatimAdapter(self.invalid_lat, 0, "json", 0)
        self.assertEqual(str(context.exception), "Latitudine o longitudine non valide")

    def test_invalid_longitude(self):
        """
        Testa l'init di NominatimAdapter con la longitudine non valida
        """
        # test invalid longitude
        with self.assertRaises(Exception) as context:
            NominatimAdapter(0, self.invalid_lon, "json", 0)
        self.assertEqual(str(context.exception), "Latitudine o longitudine non valide")

    def test_invalid_format(self):
        """
        Testa l'init di NominatimAdapter con il formato non valido
        """
        # test invalid format
        with self.assertRaises(Exception) as context:
            NominatimAdapter(0, 0, self.invalid_format, 0)
        self.assertEqual(str(context.exception), "Formato non valido")

    def test_invalid_zoom(self):
        """
        Testa l'init di NominatimAdapter con lo zoom non valido
        """
        # test invalid zoom
        with self.assertRaises(Exception) as context:
            NominatimAdapter(0, 0, "json", self.invalid_zoom)
        self.assertEqual(str(context.exception), "Zoom non valido")
        
    def test_get_data(self):
        """
        Testa il metodo get_data che restituisce gli indirizzi
        """
        # simulate response from Nominatim API
        with requests_mock.Mocker() as m:
            m.get("https://nominatim.openstreetmap.org/reverse", json={"key1": "value1", "key2": "value2"})

            # test get_data method
            nominatim_adapter = NominatimAdapter(0, 0, "json", 0)
            result = nominatim_adapter.get_data()
            self.assertEqual(result, {"key1": "value1", "key2": "value2"})

class SenseSquareAdapterTest(unittest.TestCase):
    """
    Testa la classe SenseSquareAdapter
    """
    def setUp(self):
        """
        Inizializza i valori validi e invalidi per i test
        """
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
        """
        Testa l'init di SenseSquareAdapter con valori validi
        """
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
        """
        Testa il metodo get_data_for_today che restituisce i dati inquinamento per oggi
        """
        adapter = SenseSquareAdapter("valid_nation", "valid_regione", "valid_provincia", "valid_comune")
        with requests_mock.Mocker() as m:
            m.post('https://square.sensesquare.eu:5001/placeView', json={'response_code': 200, 'message': 'Success', 'result': '{data}'})
            data = adapter.get_data_for_today()
            self.assertEqual(data, {'response_code': 200, 'message': 'Success', 'result': '{data}'})
    
    def test_invalid_get_data_for_today(self):
        """
        Testa il metodo get_data_for_today che lancia un eccezione con valori invalidi
        """
        adapter = SenseSquareAdapter("invalid_nation", "valid_regione", "valid_provincia", "valid_comune")
        with self.assertRaises(Exception) as context:
            adapter.get_data_for_today()
        self.assertEqual("Impossibile soddisfare questa richiesta", str(context.exception))
        
    def test_get_data_time_interval(self):
        """
        Testa il metodo get_data_time_interval che restituisce i dati inquinamento per un intervallo di tempo
        """
        with requests_mock.Mocker() as mock:
            mock.post('https://square.sensesquare.eu:5001/download', json={'response_code': 200, 'message': 'Success', 'result': 'test_response'})
            # Assume that self.start_date, self.end_date, and self.formato are set to appropriate values
            adapter = SenseSquareAdapter("valid_nation", "valid_regione", "valid_provincia", "valid_comune", self.valid_start_date, self.valid_end_date, self.valid_formato)
            
            # Test the case when the response code is not 400
            result = adapter.get_data_time_interval()
            #assert that result is an array
            self.assertEqual(result, [])

            # Test the case when the response code is 400
            mock.post('https://square.sensesquare.eu:5001/download', status_code=400)
            with self.assertRaises(Exception) as context:
                result = adapter.get_data_time_interval()
            self.assertEqual(str(context.exception), 'Impossibile soddisfare questa richiesta')

            # Test the case when start_date or end_date is None
            self.start_date = None
            with self.assertRaises(Exception) as context:
                result = adapter.get_data_time_interval()
            self.assertEqual(str(context.exception), 'Impossibile soddisfare questa richiesta')

if __name__ == '__main__':
    t = TestOpenMeteoAdapter()
    t.setUp()
    t.test_get_data()