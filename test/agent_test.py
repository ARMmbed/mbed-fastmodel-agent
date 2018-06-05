from unittest import TestCase

import fm_agent

class TestFastmodelAgent(TestCase):
    def test_check_configs_true(self):
        s = fm_agent.create().check_config_exist("DEFAULT.conf")
        self.assertTrue(s)
    def test_check_configs_false(self):
        s = fm_agent.create().check_config_exist("THISFILENOTEXIST.conf")
        self.assertFalse(s)
    def test_init_without_run(self):
        s = fm_agent.create()
        self.assertFalse(s.fastmodel_name)
        self.assertFalse(s.config_name)
        self.assertTrue(s.configuration)
    def test_init_with_run(self):
        s = fm_agent.create("FVP_MPS2_M3","DEFAULT")
        self.assertTrue(s.fastmodel_name)
        self.assertTrue(s.config_name)
        self.assertTrue(s.configuration)