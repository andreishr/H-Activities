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

