# 📰 Burundi News — Site d'Actualités

Application web mobile de lecture d'actualités burundaises.
Développée avec **Vue.js** (frontend) et **Django REST Framework** (backend).

## 🚀 Technologies

- **Frontend** : Vue.js 3, Vue Router, Axios
- **Backend** : Django 5, Django REST Framework, JWT Auth
- **Base de données** : SQLite (dev)

## ✨ Fonctionnalités

- 🔐 Authentification JWT (login / inscription)
- 📰 Flux d'articles avec pagination
- 💬 Commentaires imbriqués (réponses)
- 📴 Mode hors-ligne (cache local)
- 👤 Rôles : Admin / Utilisateur

## ⚙️ Installation

### Backend
```bash
cd actualites
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend
```bash
cd site_actualites_vue
npm install
npm run serve
```

## 👤 Auteur
**Abdoul** — [@abdoulncuti14-ai](https://github.com/abdoulncuti14-ai)
🇧🇮 Bujumbura, Burundi