import unittest
from data.drdFile.drdFile import DrdFile
import os
import zipfile
import shutil


class TestDrdFile(unittest.TestCase):
    """
    Test with create new drd file from database
    """


    @classmethod
    def setUpClass(cls):
        pass


    @classmethod
    def tearDownClass(cls):
        if os.path.isfile('tests/resources/test.drd'):
            os.remove('tests/resources/test.drd')

        if os.path.isfile('tests/resources/database'):
            os.remove('tests/resources/database')

        if os.path.isdir('tests/resources/maps'):
            shutil.rmtree('tests/resources/maps')


    def test_create(self):
        """
        Create new .drd file
        :return: 
        """
        DrdFile().create('tests/resources/test.drd', 'unitTests.db')

        self.assertTrue(os.path.isfile('tests/resources/test.drd'))

        with zipfile.ZipFile('tests/resources/test.drd') as myZip:
            myZip.extractall('tests/resources')

        self.assertTrue(os.path.isfile('tests/resources/database'))
        self.assertTrue(os.path.isdir('tests/resources/maps'))
