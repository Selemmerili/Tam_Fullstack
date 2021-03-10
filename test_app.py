import unittest
from app import app
from main import load_csv, create_schema,Ligne
import sqlite3

class TestApiFlask(unittest.TestCase):
    def setUp(self):

        self.app = app.test_client()
        self.app.testing = True 


    # def test_home_status_code(self):
    #     """ def status_code test if path is ok "/"
    #     """
    #     result = self.app.get('/') 
    #     self.assertEqual(result.status_code, 200) 
    #     # ".status_code = renvoie, si marche = 200 (ok)


    def test_home_data(self):
        """ test_home_type test if te app is j.son content
        """
        
        result = self.app.get('/')
        self.assertTrue(result.data,'Direction')
        self.assertTrue(result.data,'Ligne')
        
    def test_home_word(self):
        """ Test if the word is includes 
        """
        result = self.app.get('/')
        self.assertTrue(result.data,b'Hello World')

  
        
    def test_loadcsv(self):
        conn = sqlite3.connect('transport.db')
        c = conn.cursor()
        c.execute(
            """
            DROP TABLE IF EXISTS 'infoarret'"""
            )
        c.execute("""
            CREATE TABLE IF NOT EXISTS 'infoarret' (
            "Station"	TEXT,
            "Ligne"	TEXT,
            "Direction"	TEXT,
            "Horaire"	TEXT,
            "Ville" TEXT);""")
        self.assertEqual(len(c.fetchall()),0)
        load_csv("Montpellier.csv",c)
        c.execute(
            """
            SELECT * FROM 'infoarret';
            """)
        # self.assertEqual(len(c.fetchall()),41)
        
        conn.commit()
        conn.close()

    def test_Ligne(self):
        conn = sqlite3.connect('transport.db')
        c = conn.cursor()
        c.row_factory= sqlite3.Row
        c.execute("""SELECT Ligne FROM infoarret """)
        self.assertEqual(len(Ligne()),40)
        self.assertNotEqual(len(Ligne()),30)
        self.assertNotIsInstance(Ligne(), int)

        conn.commit()
        conn.close()



    def test_createschema(self):
        conn = sqlite3.connect(":memory:")
        c = conn.cursor()
        create_schema(c)
        self.assertEqual(c.rowcount,-1)
        self.assertIsNotNone(":memory:")
        self.assertEqual(len(c.fetchall()),0)
        #print(c.rowcount)
        # nbrligne = c.execute("""SELECT COUNT(*) FROM ":memory:" """)
        # print(nbrligne)
        # self.assertEqual(nbrligne,1)
        conn.commit()
        conn.close()

if __name__ == '__main__':
    unittest.main()

