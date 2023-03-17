import unittest
import requests

class Test(unittest.TestCase):
    BASE = "http://127.0.0.1:5000"

    data_login_gm = {
        'email': 'michaelgm@hospital-api.com',
        'password': 'gmMichael'
    }
    
    def get_cookie_headers(self):
        response = requests.post(self.BASE + "/login", json=self.data_login_gm)
        token = response.json().get('access_token')
        headers = {'Cookie': f'access_token_cookie='+ token}
        return headers

    def test_login(self):
        response = requests.post(self.BASE + "/login", json = self.data_login_gm)
        self.assertEqual(response.status_code, 200) 
        print('[=====> TEST 1 COMPLETED:')

    def test_add_patient(self):
        headers = self.get_cookie_headers()
        response = requests.post(self.BASE + "/patient/add", json = { "name" : "Will",
                "age" : 42,
                "doc_id" : "7"
                }, headers=headers)
        self.assertEqual(response.status_code, 201)
        print('[=====> TEST 2 COMPLETED:')
        
    def test_delete_patient(self):
        headers = self.get_cookie_headers()
        response = requests.delete(self.BASE + "/patient/19/delete", headers=headers)
        self.assertEqual(response.status_code, 204)
        print('[=====> TEST 3 COMPLETED:')

    def test_edit_patient(self):
        headers = self.get_cookie_headers()
        response = requests.put(self.BASE + "/patient/12/edit", json = { "doc_id": "2",
                "name": "Matt",
                "age": "30",
                "disease": "Diabetis",
                "details": ""
                },headers=headers)
        self.assertEqual(response.status_code, 200)
        print('[=====> TEST 4 COMPLETED:')

    def test_treat_add(self):
        headers = self.get_cookie_headers()
        response = requests.post(self.BASE + "/treatment/add", json = { "name": "Bronchitis Treatment",
                "description": "Ventolin, Mucinex",
                "doc_id": "2"
                },headers=headers)
        self.assertEqual(response.status_code, 201)
        print('[=====> TEST 5 COMPLETED:')

if __name__=='__main__':
    unittest.main()