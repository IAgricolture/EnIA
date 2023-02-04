import os
import sys
import unittest
sys.path.append(os.path.abspath(os.path.join('.' )))
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
        
if __name__ == '__main__':
    unittest.main()