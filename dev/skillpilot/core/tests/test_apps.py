from django.test import TestCase
from django.apps import apps
from django.core.management import call_command

#test application config settings
class TestCoreConfig(TestCase):
    def setUp(self):
        self.core_config = apps.get_app_config('core')
    
    #test default field
    def test_default_auto_field(self):
        self.assertEqual(self.core_config.default_auto_field, 'django.db.models.BigAutoField')

    #test app name
    def test_name(self):
        self.assertEqual(self.core_config.name, 'core')
