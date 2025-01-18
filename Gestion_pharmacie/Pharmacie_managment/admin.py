from django.contrib import admin
from Pharmacie_managment.models import Client,Commande,Produit,Fournisseur
# # Register your models here.


admin.site.register(Client)
admin.site.register(Commande)
admin.site.register(Produit)
admin.site.register(Fournisseur)