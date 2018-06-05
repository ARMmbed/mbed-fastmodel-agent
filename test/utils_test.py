from unittest import TestCase


from fm_agent.utils import SimulatorError
from fm_agent.utils import check_host_os
from fm_agent.utils import remove_comments
from fm_agent.utils import strip_quotes
from fm_agent.utils import boolean_filter


class Testutils(TestCase):
    def test_remove_comments(self):
        self.assertEqual(remove_comments("#"),"")
        self.assertEqual(remove_comments("#"),"")
        self.assertEqual(remove_comments("#single hash"),"")
        self.assertEqual(remove_comments("##double hash"),"")
        self.assertEqual(remove_comments("text#comment"),"text")
        self.assertEqual(remove_comments("text"),"text")
        
    def test_remove_comments(self):
        self.assertEqual(strip_quotes("no quote"),"no quote")
        self.assertEqual(strip_quotes("'single quote'"),"single quote")
        self.assertEqual(strip_quotes("\"double quote\""),"double quote")
