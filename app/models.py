from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

db = SQLAlchemy(model_class=Base)


class User(db.Model):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    role = Column(String(50), nullable=False, default="Admin")

    def __repr__(self):
        return f"<User {self.username}>"


class Product(db.Model):
    __tablename__ = "produit"

    code = Column(String(100), primary_key=True)
    name = Column(String(100), nullable=False)
    prix = Column(Float, nullable=False)
    qte = Column(Integer, nullable=False)
    categorie = Column(String(255))

    lignes_commande = db.relationship("Comporter", back_populates="produit", lazy=True)

    def __repr__(self):
        return f"<Product(name={self.name}, prix={self.prix})>"


class Client(db.Model):
    __tablename__ = "client"

    code_client = Column(String(100), primary_key=True)
    nom = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    telephone = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)

    commande = db.relationship("Commande", back_populates="client", lazy=True)

    def __repr__(self):
        return f"<Client {self.nom}>"


class Commande(db.Model):
    __tablename__ = "commande"

    commande_code = Column(String(100), primary_key=True)
    date_commande = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), nullable=False)

    code_client = Column(
        String(100),
        ForeignKey("client.code_client"),
        nullable=False,
    )

    created_at = Column(DateTime, default=datetime.utcnow)

    client = db.relationship("Client", back_populates="commande", lazy=True)

    lignes_commande = db.relationship("Comporter", back_populates="commande", lazy=True)

    def __repr__(self):
        return f"<Commande {self.commande_code}>"


class Comporter(db.Model):
    __tablename__ = "comporter"

    id = Column(Integer, primary_key=True)

    commande_code = Column(
        String(100),
        ForeignKey("commande.commande_code"),
        nullable=False,
    )

    produit_code = Column(
        String(100),
        ForeignKey("produit.code"),
        nullable=False,
    )

    quantite = Column(Integer, nullable=False)
    prix_unitaire = Column(Float, nullable=False)
    sous_total = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    commande = db.relationship("Commande", back_populates="lignes_commande", lazy=True)

    produit = db.relationship("Product", back_populates="lignes_commande", lazy=True)

    def __repr__(self):
        return f"<Comporter cmd={self.commande_code} " f"prod={self.produit_code}>"


def ajouter_donnees_initiales(entite, colonnes, valeurs):
    nouvel_enregistrement = entite(**dict(zip(colonnes, valeurs)))

    db.session.add(nouvel_enregistrement)
    db.session.commit()
