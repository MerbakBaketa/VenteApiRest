from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

db = SQLAlchemy(model_class=Base)


class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"


class Product(db.Model):
    __tablename__ = "produits"

    code = Column(String(100), primary_key=True)
    name = Column(String(100), nullable=False)
    prix = Column(Float, nullable=False)
    qte = Column(Integer, nullable=False)
    categorie = Column(String(255))

    def __repr__(self):
        return f"<Product(name={self.name}, prix={self.prix})>"


class Client(db.Model):
    __tablename__ = "clients"

    code_client = Column(String(100), primary_key=True)
    nom = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    telephone = Column(String(20))

    commandes = db.relationship("Commande", backref="client", lazy=True)

    def __repr__(self):
        return f"<Client {self.nom}>"


class Commande(db.Model):
    __tablename__ = "commandes"

    commande_code = Column(String(100), primary_key=True)
    date_commande = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), nullable=False)
    code_client = Column(String(100), ForeignKey("clients.code_client"), nullable=False)
    produits = db.relationship("Comporter", backref="commande", lazy=True)

    def __repr__(self):
        return f"<Commande {self.id}>"


class Comporter(db.Model):
    __tablename__ = "comporter"

    id = Column(Integer, primary_key=True)

    commande_code = Column(
        String(100), ForeignKey("commandes.commande_code"), nullable=False
    )
    produit_code = Column(String(100), ForeignKey("produits.code"), nullable=False)
    quantite = Column(Integer, nullable=False)
    prix_unitaire = Column(Float, nullable=False)
    sous_total = Column(Float, nullable=False)
    produit = db.relationship("Product")

    def __repr__(self):
        return f"<Comporter cmd={self.commande_code} prod={self.produit_code}>"


def ajouter_donnees_initiales(Entite, Colonnes, Valeurs):
    nouvel_enregistrement = Entite(**dict(zip(Colonnes, Valeurs)))
    db.session.add(nouvel_enregistrement)
    db.session.commit()
