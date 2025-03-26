# Developer İnkişaf Paketi
Bu layihə **Developer İnkişaf Paketi** əsasında **əlsələ gətirilmişdir**. Task-da qeyd olunan şərtlər diqqətə alınaraq hazırlanmışdır.

## İstifadə olunan texnologiyalar
- **Python**, **Django**, **Django Rest Framework**, **SQLite** - Backend hissəsində  
- **HTML**, **CSS**, **JS**, **Bootstrap** - Frontend hissəsində  

## Quraşdırma (Windows OS)
1. İstənilən qovluğa keçin (Nümunə: `cd desktop/app/`).
2. `git clone https://github.com/ismayilovasgar/developer_task.git` komandasını icra edin.
3. **app** qovluğunda `.env` faylı yaradın və nümunə olaraq aşağıdakıları əlavə edin:
   ```env
   SECRET_KEY=d7anfo-i3s3cude-mh+dg(@l-+wlt1v#iahy^45mw(ddoh28yi8dtv+j2a&ultzloi
   DEBUG=True
4. `python -m venv venv` komandasını istifadə edərək virtual mühit yaradın.
5. `cd venv/Scripts/activate.bat` komandasını icra edərək virtual mühiti aktivləşdirin.
6. `pip install -r requirements.txt` komandasını icra edərək lazım olan paketləri yükləyin.
7. `python manage.py makemigrations` komandasını icra edərək verilənlər bazasını tərtib edin.
8. `python manage.py migrate` komandasını icra edərək verilənlər bazasına dəyişiklikləri tətbiq edin.
9. Əgər admin paneldən istifadə etmək istəyirsinizsə, `python manage.py createsuperuser` komandasını istifadə edin.
10. `python manage.py runserver` komandasını icra edərək layihəni işə salın və səhv xətaları düzəldin.
