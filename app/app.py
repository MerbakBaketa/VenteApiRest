from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from app.models import *
from app.resources import ProductListResource
from app.shemas import ma
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ventedb.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
ma.init_app(app)
migrate = Migrate(app, db) 


api = Api(app)
api.add_resource(ProductListResource, '/products', '/products/<string:product_id>')




with app.app_context():

    try:
        db.drop_all()
        db.create_all()
        print("Database and tables created successfully.")
        
        ajouter_donnees_initiales(Product, ["code", "name", "prix", "qte", "categorie"], ["P001", "Burger Classic", 5.0, 50, "Burger"])
        ajouter_donnees_initiales(Product, ["code", "name", "prix", "qte", "categorie"], ["P002", "Burger Cheese", 6.0, 40, "Burger"])
        ajouter_donnees_initiales(Product, ["code", "name", "prix", "qte", "categorie"], ["P003", "Burger Double", 7.5, 30, "Burger"])
        ajouter_donnees_initiales(Product, ["code", "name", "prix", "qte", "categorie"], ["P004", "Frites Small", 2.0, 100, "Accompagnement"])
        ajouter_donnees_initiales(Product, ["code", "name", "prix", "qte", "categorie"], ["P005", "Frites Large", 3.0, 80, "Accompagnement"])
        ajouter_donnees_initiales(Product, ["code", "name", "prix", "qte", "categorie"], ["P006", "Coca-Cola", 1.5, 120, "Boisson"])
        ajouter_donnees_initiales(Product, ["code", "name", "prix", "qte", "categorie"], ["P007", "Sprite", 1.5, 110, "Boisson"])
        ajouter_donnees_initiales(Product, ["code", "name", "prix", "qte", "categorie"], ["P008", "Eau Minérale", 1.0, 200, "Boisson"])
        ajouter_donnees_initiales(Product, ["code", "name", "prix", "qte", "categorie"], ["P009", "Milkshake Vanille", 3.5, 25, "Dessert"])
        ajouter_donnees_initiales(Product, ["code", "name", "prix", "qte", "categorie"], ["P010", "Glace Chocolat", 2.5, 30, "Dessert"])

        ajouter_donnees_initiales(Client, ["code_client", "nom", "email", "telephone"], ["CL001", "Kabila", "jean1@mail.com", "099000001"])
        ajouter_donnees_initiales(Client, ["code_client", "nom", "email", "telephone"], ["CL002", "Tshisekedi", "paul2@mail.com", "099000002"])
        ajouter_donnees_initiales(Client, ["code_client", "nom", "email", "telephone"], ["CL003", "Mukendi", "sarah3@mail.com", "099000003"])
        ajouter_donnees_initiales(Client, ["code_client", "nom", "email", "telephone"], ["CL004", "Ilunga", "david4@mail.com", "099000004"])
        ajouter_donnees_initiales(Client, ["code_client", "nom", "email", "telephone"], ["CL005", "Kasongo", "marie5@mail.com", "09900005"])
        ajouter_donnees_initiales(Client, ["code_client", "nom", "email", "telephone"], ["CL006", "Mbala", "lucie6@mail.com", "099000006"])
        ajouter_donnees_initiales(Client, ["code_client", "nom", "email", "telephone"], ["CL007", "Kalala", "marie7@mail.com", "099000007"])
        ajouter_donnees_initiales(Client, ["code_client", "nom", "email", "telephone"], ["CL008", "Mutombo", "jean8@mail.com", "099000008"])
        ajouter_donnees_initiales(Client, ["code_client", "nom", "email", "telephone"], ["CL009", "Banza", "jean9@mail.com", "099000009"])
        ajouter_donnees_initiales(Client, ["code_client", "nom", "email", "telephone"], ["CL010", "Lukaku", "jean10@mail.com", "099000010"])

        ajouter_donnees_initiales(Commande, ["commande_code", "date_commande", "status", "code_client"], ["CMD001", datetime.utcnow(), "En cours", "CL001"])
        ajouter_donnees_initiales(Commande, ["commande_code", "date_commande", "status", "code_client"], ["CMD002", datetime.utcnow(), "En attente", "CL002"])
        ajouter_donnees_initiales(Commande, ["commande_code", "date_commande", "status", "code_client"], ["CMD003", datetime.utcnow(), "En attente", "CL002"])
        ajouter_donnees_initiales(Commande, ["commande_code", "date_commande", "status", "code_client"], ["CMD004", datetime.utcnow(), "En Livrée", "CL002"])
        ajouter_donnees_initiales(Commande, ["commande_code", "date_commande", "status", "code_client"], ["CMD005", datetime.utcnow(), "En Livrée", "CL001"])
        ajouter_donnees_initiales(Commande, ["commande_code", "date_commande", "status", "code_client"], ["CMD006", datetime.utcnow(), "En attente", "CL006"])
        ajouter_donnees_initiales(Commande, ["commande_code", "date_commande", "status", "code_client"], ["CMD007", datetime.utcnow(), "En Livrée", "CL006"])
        ajouter_donnees_initiales(Commande, ["commande_code", "date_commande", "status", "code_client"], ["CMD008", datetime.utcnow(), "En Livrée", "CL008"])
        ajouter_donnees_initiales(Commande, ["commande_code", "date_commande", "status", "code_client"], ["CMD009", datetime.utcnow(), "En cours", "CL008"])
        ajouter_donnees_initiales(Commande, ["commande_code", "date_commande", "status", "code_client"], ["CMD010", datetime.utcnow(), "En cours", "CL008"])

        ajouter_donnees_initiales(Comporter, ["commande_code", "produit_code", "prix_unitaire", "quantite", "sous_total"], ["CMD001", "P001", 2000, 2, 4000])
        ajouter_donnees_initiales(Comporter, ["commande_code", "produit_code", "prix_unitaire", "quantite", "sous_total"], ["CMD001", "P004", 1500, 1, 1500])
        ajouter_donnees_initiales(Comporter, ["commande_code", "produit_code", "prix_unitaire", "quantite", "sous_total"], ["CMD002", "P002", 3500, 1, 3500])
        ajouter_donnees_initiales(Comporter, ["commande_code", "produit_code", "prix_unitaire", "quantite", "sous_total"], ["CMD002", "P005", 2800, 2, 5600])
        ajouter_donnees_initiales(Comporter, ["commande_code", "produit_code", "prix_unitaire", "quantite", "sous_total"], ["CMD003", "P003", 4250, 1, 4250])
        ajouter_donnees_initiales(Comporter, ["commande_code", "produit_code", "prix_unitaire", "quantite", "sous_total"], ["CMD003", "P006", 2500, 1, 2500])
        ajouter_donnees_initiales(Comporter, ["commande_code", "produit_code", "prix_unitaire", "quantite", "sous_total"], ["CMD004", "P001", 2000, 1, 2000])
        ajouter_donnees_initiales(Comporter, ["commande_code", "produit_code", "prix_unitaire", "quantite", "sous_total"], ["CMD004", "P007", 1850, 2, 3700])
        ajouter_donnees_initiales(Comporter, ["commande_code", "produit_code", "prix_unitaire", "quantite", "sous_total"], ["CMD005", "P002", 3500, 2, 7000])
        ajouter_donnees_initiales(Comporter, ["commande_code", "produit_code", "prix_unitaire", "quantite", "sous_total"], ["CMD005", "P008", 3259.99, 1, 3259.99])

        app.run(debug=True)
    except Exception as e:
        print(f"An error occurred: {e}")

