I. migration de la BD
    a/ installer : pip install flask-migrate s'il nexiste pas dans le requirements
    b/ Initialiser Flask-Migrate dans app.py
    c/ Sur windows CMD; executé : 
        set FLASK_APP=app.py
        set FLASK_ENV=development
    d/ Initialiser les migrations (une seule fois)
       flask db init
    e/ Créer une migration pour tes modèles
    flask db migrate -m "Ajout nouvelles colonnes"
    f/ flask db upgrade
    g/ Vérification : flask db current