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
        print('\nTEST 1 COMPLETED:')

    def test_add_patient(self):
        headers = self.get_cookie_headers()
        response = requests.post(self.BASE + "/patient/add", json = { "name" : "Will",
                "age" : 42,
                "doc_id" : "7"
                }, headers=headers)
        self.assertEqual(response.status_code, 201)
        print('\nTEST 2 COMPLETED:')
        
    def test_delete_patient(self):
        headers = self.get_cookie_headers()
        response = requests.delete(self.BASE + "/patient/32/delete", headers=headers)
        self.assertEqual(response.status_code, 204)
        print('\nTEST 3 COMPLETED:')

    def test_edit_patient(self):
        headers = self.get_cookie_headers()
        response = requests.put(self.BASE + "/patient/12/edit", json = { "doc_id": "2",
                "name": "Matt",
                "age": "30",
                "disease": "Diabetis",
                "details": ""
                },headers=headers)
        self.assertEqual(response.status_code, 200)
        print('\nTEST 4 COMPLETED:')

    def test_treat_add(self):
        headers = self.get_cookie_headers()
        response = requests.post(self.BASE + "/treatment/add", json = { "name": "Bronchitis Treatment",
                "description": "Ventolin, Mucinex",
                "doc_id": "2"
                },headers=headers)
        self.assertEqual(response.status_code, 201)
        print('\nTEST 5 COMPLETED:')

    def test_report_docs(self):
        headers = self.get_cookie_headers()
        response = requests.get(self.BASE + "/docs/report", headers=headers)
        self.assertEqual(response.status_code, 200)
        print('\nTEST 6 COMPLETED:')

    def test_assign_patient(self):
        headers = self.get_cookie_headers()
        response = requests.post(self.BASE + "/assign", json={
                "assistant_id": 5,
                "patient_id": 4
                },headers=headers)
        self.assertEqual(response.status_code, 400)
        print('\nTEST 7 COMPLETED:')

    def test_apply_treat(self):
        headers = self.get_cookie_headers()
        response = requests.post(self.BASE + '/tr/applied', json={
                "treat_id": 1
                },headers=headers)
        self.assertEqual(response.status_code, 401)
        print('\nTEST 8 COMPLETED:')

if __name__=='__main__':
    unittest.main()