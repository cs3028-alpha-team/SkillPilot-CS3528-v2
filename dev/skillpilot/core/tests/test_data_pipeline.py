from django.test import TestCase
import pandas as pd
from core import data_pipeline 
from core.data_pipeline import DataPipeline

#test functionality of the data pipeline
class TestDataPipeline(TestCase):
     # set up test data
    def setUp(self):
        student_data = {
            'studyMode': [None, 'online', 'hybrid', 'in-person', None],
            'studyPattern': ['FT', None, 'PT', None, 'FT'],
            'GPA': [3.2, 2.75, 3.87, 2.1, 3.99]
        }
        internship_data = {
            'minGPA': [2.5, 3.0, None, 3.7, 2.85]
        }

        self.students_df = pd.DataFrame(student_data)
        self.internships_df = pd.DataFrame(internship_data)

        self.pipeline = DataPipeline(self.students_df, self.internships_df)
        
    # Test rounding function
    def test_round(self):  
        self.assertEqual(self.pipeline._DataPipeline__round(3.2), 0)
        self.assertEqual(self.pipeline._DataPipeline__round(2.75), 0)
        self.assertEqual(self.pipeline._DataPipeline__round(3.87), 0)
        self.assertEqual(self.pipeline._DataPipeline__round(2.1), 0)
        self.assertEqual(self.pipeline._DataPipeline__round(3.99), 0)
        
    # Test for valid study modes
    def test_check_studymode(self):
        self.assertTrue(self.pipeline._DataPipeline__check_studymode('online'))
        self.assertTrue(self.pipeline._DataPipeline__check_studymode('in-person'))
        self.assertTrue(self.pipeline._DataPipeline__check_studymode('hybrid'))
        self.assertFalse(self.pipeline._DataPipeline__check_studymode('remote'))
        self.assertFalse(self.pipeline._DataPipeline__check_studymode(None))
    
    # Test for valid study patterns
    def test_check_studypattern(self):
        self.assertTrue(self.pipeline._DataPipeline__check_studypattern('FT'))
        self.assertTrue(self.pipeline._DataPipeline__check_studypattern('PT'))
        self.assertFalse(self.pipeline._DataPipeline__check_studypattern('full-time'))
        self.assertFalse(self.pipeline._DataPipeline__check_studypattern(None))
        
    # Test the clean method functionality
    def test_clean(self):
        students_cleaned, internships_cleaned = self.pipeline.clean()

        # Checking if None values are replaced
        self.assertEqual(students_cleaned.loc[0, 'studyMode'], 'in-person')
        self.assertEqual(students_cleaned.loc[1, 'studyPattern'], 'FT')
        self.assertEqual(students_cleaned.loc[3, 'studyPattern'], 'FT')
        self.assertEqual(internships_cleaned.loc[2, 'minGPA'], 0) 
    
    # Test overall data processing 
    def test_integration(self):
        students_original = self.students_df.copy()
        internships_original = self.internships_df.copy()

        students_cleaned, internships_cleaned = self.pipeline.clean()

        # test dataframes maintain the same size
        self.assertEqual(students_original.shape, students_cleaned.shape)
        self.assertEqual(internships_original.shape, internships_cleaned.shape)

        # test data types are unchanged
        self.assertEqual(students_cleaned.dtypes['studyMode'], object)
        self.assertEqual(students_cleaned.dtypes['studyPattern'], object)
        self.assertTrue(pd.api.types.is_float_dtype(students_cleaned['GPA']))

