from django import forms
from .models import *
from django.contrib import messages
from .models import MediaFile

class DataInput(forms.DateInput):
    input_type = 'date'
class PharmacieForms(forms.ModelForm):
    class Meta:
        model = Pharmacie
        fields = '__all__'
        widgets = {
            # 'date_naissance':DataInput,
    
        }
# La méthode clean est surchargée pour vérifier si un produit avec le même nom et lot existe déjà dans la base de données.

# Si un tel produit existe, une erreur de validation est levée avec un message approprié.
    # def clean(self):
    #     cleaned_data = super().clean()
    #     nom = cleaned_data.get('nom')
    #     telephone = cleaned_data.get('telephone')

    #     if Pharmacie.objects.filter(nom=nom, telephone=telephone).exists():
    #         messages.error(request, "Cette pharmacie existe déjà avec le même numero de téléphone.")
    #     # comment afficher ce message?????

    #     return cleaned_data

class ProductForms(forms.ModelForm):
    class Meta:
        model = Produit
        fields = '__all__'
        widgets = {
            'date_expiration':DataInput,
    
        }
        
class VenteForm(forms.ModelForm):
    class Meta:
        model = Vente
        fields = '__all__'

    def init(self, *args, **kwargs):
        super().init(*args, **kwargs)
        self.fields['produit'].queryset = Produit.objects.filter(quantite_en_stock__gt=0)  # Affiche seulement les produits en stock


# La méthode clean est surchargée pour vérifier si un produit avec le même nom et lot existe déjà dans la base de données.

# Si un tel produit existe, une erreur de validation est levée avec un message approprié.
    def clean(self):
        cleaned_data = super().clean()
        nom = cleaned_data.get('nom')
        lot = cleaned_data.get('lot')

        if Produit.objects.filter(nom=nom, lot=lot).exists():
            raise forms.ValidationError("Ce produit existe déjà avec le même lot.")

        return cleaned_data
    


        
class ClientForms(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        # Si un tel client existe, une erreur de validation est levée avec un message approprié.
    def clean(self):
        cleaned_data = super().clean()
        identite = cleaned_data.get('identite')
       

        if Client.objects.filter(identite=identite).exists():
            raise forms.ValidationError("Ce client existe déjà avec le même N° d'identité.")

        return cleaned_data
 
class FactureForm(forms.ModelForm):
    class Meta:
        model=Facture
        fields='__all__'     
        
class TransactionForm(forms.ModelForm):
    class Meta:
        model=Transaction
        fields='__all__'     
        
class CommandeForms(forms.ModelForm):
    class Meta:
        model = Commande
        fields = '__all__'
        widgets = {
            'date_commande':DataInput,
    
        }

# class LigneCommandeForms(forms.ModelForm):
#     class Meta:
#         model = LigneCommande
#         fields = '__all__'
#         widgets = {
#             # 'date_commande':DataInput,
            
#         }
        
class FournisseurForms(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = '__all__'
        
    
class InventaireForms(forms.ModelForm):
    class Meta:
        model = Inventaire
        fields = '__all__'
        widgets = {
            'date_mouvement':DataInput,
    
        }

# class InventaireForms(forms.ModelForm):
#     class Meta:
#         model = Inventaire
#         fields = '__all__'
#         widgets = {
#             'date_mouvement':DataInput,
    
#         }
# class InventaireForms(forms.ModelForm):
#     class Meta:
#         model = Inventaire
#         fields = '__all__'
#         widgets = {
#             'date_mouvement':DataInput,
    
#         }

class RecetteForms(forms.ModelForm):
    class Meta:
        model = Recette
        fields = '__all__'
        widgets = {
            'date_recette':DataInput,
    
        }
        
class ProduitRecetteForms(forms.ModelForm):
    class Meta:
        model = ProduitRecette
        fields = '__all__'
        widgets = {
            # 'date_recette':DataInput,
    
        }
        
# formulaire pour télécharger des fichiers :
class MediaFileForm(forms.ModelForm):
    class Meta:
        model = MediaFile
        fields = '__all__'