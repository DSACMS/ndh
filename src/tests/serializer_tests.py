import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from pathlib import Path

class GenericFHIRJSONTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Load test data once for all tests"""
        test_file_path = Path(__file__).parent / 'test_data' / 'users.json'
        with open(test_file_path, 'r') as f:
            cls.test_data = json.load(f)
    
    def test_json_structure_exists(self):
        """Verify the JSON file exists and has content"""
        self.assertIsNotNone(self.test_data, "JSON data failed to load")
        self.assertIsInstance(self.test_data, (dict, list), 
                             "JSON should be an object or array")




class ProviderFHIRJSONTests(GenericFHIRJSONTests):
    def test_required_top_level_fields(self):
        """Test for required top-level fields in FHIR JSON"""
        required_fields = {
            'resourceType': str,
            'id': str,
            'meta': dict,
            'name': str,
            'mode': str,
            'address': dict,
            'physicalType': str,
            'managingOrganization': str
        }
        
        if isinstance(self.test_data, dict):
            for field, field_type in required_fields.items():
                with self.subTest(field=field):
                    self.assertIn(field, self.test_data, 
                                 f"Missing required field: {field}")
                    self.assertIsInstance(self.test_data[field], field_type,
                                         f"Field {field} has wrong type")

    def test_fhir_object_structure(self):
        """Test structure of individual FHIR objects"""
        if isinstance(self.test_data, dict) and 'meta' in self.test_data:
            self.assertIn('profile',self.test_data['meta'])

        if isinstance(self.test_data,dict) and 'address' in self.test_data:
            required_fhir_fields = {
                'line': list,
                'city': str,
                'state': str,
                'postalCode': str
            }

            for field, field_type in required_fhir_fields.items():
                with self.subTest(address_field=field):

                    self.assertIn(field, self.test_data['address'], 
                                f"Provider missing required field: {field}")
                    self.assertIsInstance(self.test_data['address'][field], field_type,
                                        f"Provider field {field} has wrong type")