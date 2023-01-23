import unittest
import os, sys

sys.path.append(os.path.abspath(os.path.join('.' )))

from src.logic.AmbienteAgricolo.AmbienteAgricoloService import AmbienteAgricoloService

class provaTest(unittest.TestCase):
    def test_prova(self):
        self.assertEqual(1, 1)