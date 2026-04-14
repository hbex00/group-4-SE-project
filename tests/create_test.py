import unittest
from app.routes.create import create_recepie

class Testcreat_recepie(unittest.TestCase):

    def test_upper(self):
        result = create_recepie("Köttbullar","goda kötbullar", 2)
        self.assertEqual(result.recipe_title,"Köttbullar")
        self.assertEqual(result.description,"goda kötbullar")
        self.assertEqual(result.user_id, 2)

if __name__ == '__main__':
    unittest.main()