from unittest import TestCase

from fm_agent.fm_config import FastmodelConfig
from fm_agent.utils import SimulatorError

class TestFastmodelConfig(TestCase):
    def test_Setting_File(self):
        self.assertTrue(FastmodelConfig.SETTINGS_FILE,"settings.json")
    def test_parse_params_file_failed(self):
        c=FastmodelConfig()

        try:
            c.parse_params_file("FILE_NOT_EXIST")
        except SimulatorError as e:
            pass
        else:
            self.fail("failed to catch the exception")
                
    def test_parse_params_file(self):
        c=FastmodelConfig()
        try:
            c.parse_params_file("DEFAULT.conf")
        except SimulatorError as e:
            self.fail("caught an SimulatorError exception")
            
    def test_get_configs_none(self):
        c=FastmodelConfig()
        self.assertIsNone(c.get_configs("NOT_A_MODEL"))
        
    def test_get_configs(self):
        c=FastmodelConfig()
        self.assertIsNotNone(c.get_configs("FVP_MPS2_M3"))
        
    def test_get_all_configs(self):
        c=FastmodelConfig()
        self.assertIsNotNone(c.get_all_configs())  