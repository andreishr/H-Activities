# Hospital Activities API
## Install process:       
### ∙ Creating environment:  
python -m venv .<env_name> (ex: .apienv)  

### ∙ Installing dependencies:
pip install -r requirements.txt
    
### ∙ Running:  
flask run  

## For changes applied to the database:  
### ∙ Initializing db for migration:  
flask db init  
### ∙ After changes in the model file:  
flask db migrate

## Routes:
### List of routes:
Auth: *__/login__*   
Employee management: *__/manage/add__* , *__/manage/{id}__* , *__/manage/{id}/remove__*  
Patient management: *__/patient/add__* , *__/patient/{id}/edit__* , *__/patient/{id}/delete__*  
Treatment management: *__/treatment/add__* , *__/treatment/{id}/edit__* , *__/treatment/{id}/remove__*  
Apply treatment and check treatment: *__/give/treatment/{patiendID}/{treatID}__* , *__/tr/prescribed__*  
Assign patient to assistant: *__/assign__*  
Treatment applied by assistants: *__/tr/applied__*  
Reports: *__/docs/report__* , *__/treat/report__*

For detailed documentation about routes: *__/swagger__*

/logout : Unset jwt
/refresh : Route defined for generating token when the acces token expires

## Test file:  
∙ For running the test file:  
python test_api.py

#### Notes:  
Some tests might fail because of the changes inside the database (ex: in the case of providing a specific id in path).
More tests have been made using Postman in order to observe more responses returned from each route.  
Because multiple patients can have the same name and a doctor can have multiple patients, it can become difficult to identify patients in the *patient* table.  
More queries might be used in order to get more details since few endpoints return only IDs.
&nbsp;  
&nbsp;  
&nbsp;  
&nbsp;  
Name: Ghiteanu Andrei-Daniel  
