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
Auth: /login   
Employee management: /manage/add, /manage/{id}, /manage/{id}/remove  
Patient management: /patient/add, /patient/{id}/edit, /patient/{id}/delete  
Treatment management: /treatment/add, /treatment/{id}/edit, /treatment/{id}/remove
Apply treatment and check treatment: /give/treatment/{patiendID}/{treatID}, /tr/prescribed
Assign patient to assistant: /assign
Treatment applied by assistants: /tr/applied  
Reports: /docs/report, /treat/report

For detailed documentation about routes: /swagger

/logout : Unset jwt
/refresh : Route defined for generating token when the acces token expires

## Test file:  
∙ For running the test file:  
python test_api.py

Note:
Some tests might fail because of the changes inside the database (ex: in the case of providing a specific id in path).
More tests have been made using Postman in order to observe more responses returned from each route.  
&nbsp;  
&nbsp;  
&nbsp;  
&nbsp;  
Name: Ghiteanu Andrei-Daniel  
