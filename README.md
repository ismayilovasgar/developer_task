# Developer İnkişaf Paketi
Bu layihə Developer İnkişaf Paketi əsasında əlsələ gətirilmişdir.Task-da qeyd olunan şərtlər diqqətə alınaraq hazırlanmışdır.

## İstifadə olunan teknologilər
Python, Django, Django Rest Framework, SQLite - Backend hissəsində  
HTML,CSS,JS,Bootstrap - Frontend hissəsində
  
## Quraşdırma (Windows OS)  
- istənilən qovluğa gedilir(Nümünə: cd desktop/app/)    
- git clone https://github.com/ismayilovasgar/developer_task.git    
- app qovluğunda .env yaradılır və nümünə üçün asagidaki kimi elave edilir.    
  SECRET_KEY =d7anfo-i3s3cude-mh+dg(@l-+wlt1v#iahy^45mw(ddoh28yi8dtv+j2a&ultzloi    
  DEBUG=True   
- python -m venv venv     
- cd venv/Scripts/activate.bat   ile venv aktiv edilir  
- pip install -r requirements.txt ile lazimli paketler yuklenir   
- python manage.py makemigrations  
- python manage.py migrate   
- eger admin panel istifade olunmaq isteyinilse   
  python manage.py createsuperuser   
- 


