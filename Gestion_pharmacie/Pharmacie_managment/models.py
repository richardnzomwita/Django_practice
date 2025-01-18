from django.db import models
from datetime import date,datetime
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date, datetime
from django.utils import timezone

# Create your models here.
class Pharmacie(models.Model): #Modèle représentant la pharmacie elle-même
    nom=models.CharField( max_length=50)
    adresse=models.CharField( max_length=250)
    telephone=models.CharField( max_length=15)
    
    def __str__(self):
        return self.nom
    
    
# class Produit(models.Model):
#     nom = models.CharField(max_length=255)
#     lot = models.CharField(max_length=50)
#     expiration = models.DateField(default=timezone.now)
#     description = models.TextField(null=True, blank=True)
#     quantite_en_stock = models.PositiveIntegerField()
#     prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
#     quantite_en_stock = models.PositiveIntegerField()
#     pharmacie = models.ForeignKey(Pharmacie, on_delete=models.CASCADE)
#     seuil_alerte_stock = models.PositiveIntegerField(default=10)  # Seuil pour alerter sur le stock faible

#     def est_perime(self):
#         """Vérifie si le médicament est périmé."""
#         return date.today() > self.expiration

#     def est_proche_peremption(self):
#         """Vérifie si le médicament approche de sa date de péremption (dans 30 jours)."""
#         return (self.expiration - date.today()).days <= 30

#     def __str__(self):
#         return self.nom
#     def est_en_stock_faible(self):
#         """Vérifie si le stock du médicament est faible."""
#         return self.quantite_en_stock <= self.seuil_alerte_stock
#     def est_en_stock_normal(self):
#         """Vérifie si le stock du médicament est normal."""
#         return self.quantite_en_stock > self.seuil_alerte_stock     
#     @property
#     def prix_total(self):
#        return self.quantite_en_stock * self.prix_unitaire
    
    
class Client(models.Model): #Le modèle représentant les clients de la Pharmacie
    nom=models.CharField( max_length=50)
    prenom=models.CharField( max_length=50)
    email=models.EmailField( max_length=50)
    identite=models.CharField( max_length=15)
    photo=models.ImageField(upload_to='photos/', blank=True,)
    def __str__(self):
        return self.nom +" "+ self.prenom
    
class Produit(models.Model):  # Modèle représentant les médicaments ou produits disponibles dans la pharmacie
    categorie = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    lot = models.CharField(max_length=50)
    date_expiration = models.DateTimeField()
    description = models.TextField()
    quantite_en_stock = models.DecimalField(max_digits=10, decimal_places=1)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    pharmacie = models.ForeignKey('Pharmacie', on_delete=models.CASCADE)

    def __str__(self):
        return self.nom

    @property
    def prix_total(self):
        return self.quantite_en_stock * self.prix_unitaire
    

       
class Facture(models.Model):
    date = models.DateTimeField(default=timezone.now)
    client=models.ForeignKey(Client,on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Facture #{self.id} - {self.date}"

class Transaction(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    facture = models.ForeignKey(Facture, related_name='transactions', on_delete=models.CASCADE)
    quantite = models.DecimalField(max_digits=10, decimal_places=1)
    prix = models.DecimalField(max_digits=10,decimal_places=2)  # Le prix sera défini automatiquement
    date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Définir le prix automatiquement
        if not self.prix:
            self.prix = self.produit.prix_unitaire
        super().save(*args, **kwargs)
        return self.prix

    def __str__(self):
        return f"{self.produit.nom} - {self.quantite} @ {self.prix} {self.date}"

    @property
    def total(self):
        return self.quantite * self.prix
    

class Fournisseur(models.Model): #Ce modèle représente des fournisseurs qui fournissent des produits à la pharmacie
    nom=models.CharField( max_length=100)
    prenom=models.CharField( max_length=100)
    adresse=models.CharField( max_length=150)
    telephone=models.CharField( max_length=15)
    def __str__(self):
        return self.nom + " " + self.prenom
        
class Commande(models.Model): #Ce modèle représente les commandes passées par les clients
    produit_id=models.ForeignKey(Produit,on_delete=models.CASCADE,default=1)
    quantite=models.DecimalField(max_digits=10,decimal_places=0)
    fournisseur_id=models.ForeignKey(Fournisseur,on_delete=models.CASCADE,default=1)
    date_commande=models.DateField()
    def __str__(self):
        return self.produit_id.nom 
    
# class LigneCommande(models.Model):
#     commande= models.ForeignKey(Commande,related_name='lignes',on_delete=models.CASCADE)  
#     produit= models.ForeignKey(Produit,on_delete=models.CASCADE)  
#     quantite=models.IntegerField()
    
#     def __str__(self):
#         return self.commande.client.nom + " " + self.commande.client.prenom
    

class Inventaire(models.Model): #Ce modèle peut être utilisé pour suivre les mouvements de stocks
    produit=models.ForeignKey(Produit,on_delete=models.CASCADE)
    type_mouvement=models.CharField(max_length=50)
    date_mouvement=models.DateTimeField()
    quantite=models.IntegerField()
    
    def __str__(self):
        return self.produit, self.type_mouvement, self.date_mouvement, self.quantite
class Recette(models.Model): # Ce modèle est utilisé si tu veux gérer les prescriptions médicales
    client=models.ForeignKey(Client,on_delete=models.CASCADE)
    date_recette=models.DateField()
    
   
class ProduitRecette(models.Model):
    recette=models.ForeignKey(Recette,related_name='produits',on_delete=models.CASCADE)
    produit=models.ForeignKey(Produit, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.produit
    
# # un modèle pour stocker les informations sur vos fichiers multimédias.

class MediaFile(models.Model):
    nom = models.CharField(max_length=100)
    fichier = models.ImageField(upload_to='media/')
    description = models.TextField()
    date_ajout = models.DateTimeField(auto_now_add=True)
    
# class MediaFile(models.Model):
#     title = models.CharField(max_length=255)
#     file = models.FileField(upload_to='uploads/')  # Utilisez ImageField pour les images
#     uploaded_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title
    




class Vente(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite_vendue = models.DecimalField(max_digits=10, decimal_places=1)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    prix_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date_vente = models.DateTimeField(default=timezone.now)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Vérification de la date d'expiration
        if self.produit.date_expiration:
            expiration_date = self.produit.date_expiration
            if isinstance(expiration_date, datetime):
                expiration_date = expiration_date.date()
            if expiration_date <= date.today():
                raise ValueError(f"Le produit {self.produit.nom} a expiré et ne peut pas être vendu.")
        
        # Vérification de la quantité en stock
        if self.produit.quantite_en_stock < self.quantite_vendue:
            raise ValueError(f"Quantité en stock insuffisante pour {self.produit.nom}. Disponible : {self.produit.quantite_en_stock}")
        
        # Calcul des prix
        if not self.prix_unitaire:
            self.prix_unitaire = self.produit.prix_unitaire
        self.prix_total = self.quantite_vendue * self.prix_unitaire
        
        # Sauvegarde
        super(Vente, self).save(*args, **kwargs)

        # Mise à jour du stock
        self.produit.quantite_en_stock -= self.quantite_vendue
        self.produit.save()

    def __str__(self):
        return f"Vente de {self.produit.nom} - Quantité: {self.quantite_vendue} - Prix total: {self.prix_total}"
    
# Modèle pour le Panier et les Articles du Panier

class Panier(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    termine = models.BooleanField(default=False)

    def __str__(self):
        return f"Panier de {self.client} - {'Terminé' if self.termine else 'En cours'}"


class ArticlePanier(models.Model):
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()



    
    
    
    