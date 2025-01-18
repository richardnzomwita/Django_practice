from django.shortcuts import render, redirect
from .forms import *
from.models import *
from django.contrib import messages
from Pharmacie_managment.models import *
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.serializers.json import DjangoJSONEncoder
from .models import Produit, Vente, Panier, ArticlePanier
from django.core.exceptions import ObjectDoesNotExist
import json
from datetime import date
from django.db import transaction
# Créer une vue pour un formulaire d'inscription
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

# Créer la vue pour l'inscription

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


# Créer les Vues pour la Connexion, la Déconnexion et l'Accueil
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Afficher un message d'erreur
            messages.error(request,'Nom d\'utilisateur ou mot de passe incorrect')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

# @login_required
# def home(request):
#     return render(request, 'home.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

def home(request):
    return render(request,'base_temp.html')
def acceuil(request):
    return render(request, 'index.html')

# Creation de la vue de création de la Pharmacie
def create_pharmacie(request):
    pharma_form_creation = PharmacieForms()
    if request.method == "POST":
        # Eviter les doublons dans le formulaire. A le copier dans toutes les vieuws du formulaire
        pharma_form_creation = PharmacieForms (request.POST)
        pharmacy = request.POST.get('nom')
        adresse = request.POST.get('adresse')
        telephone = request.POST.get('telephone')
        get_all_pharmacies = Pharmacie.objects.filter(nom = pharmacy,adresse = adresse,telephone = telephone)
        if pharma_form_creation.is_valid():
            if get_all_pharmacies.exists():
                messages.error(request,'Les donnees saisies existent déjà. Veuillez réessayer!')
                return redirect('create_pharmacie')
                # Fin de verification des doublons
            else:
                try:
                    pharma_form_creation.save()
                    messages.success(request, "Insertion réussie")
                    pharma_form_creation = PharmacieForms ()
                except Exception as e:
                    messages.error(request, f"Une erreur est survenue : {e}")
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire")
    
    pharma_creations = Pharmacie.objects.all()
    return render(request, "create_pharmacie.html", {"pharma_form_creation": pharma_form_creation, 'inscriptions': pharma_creations})

# Création de la vue d'édition de la pharmacie.
def edit_pharmacie(request, id):
    pharmacie = get_object_or_404(Pharmacie, id=id)
    if request.method == "POST":
        # Pré-remplir le formulaire avec les données POST pour mise à jour
        product_form_creation = PharmacieForms(request.POST, instance=pharmacie)

        if product_form_creation.is_valid():
            try:
                product_form_creation.save()
                messages.success(request, "Mise à jour réussie")
                return redirect("create_pharmacie")  # Rediriger après succès
            except Exception as e:
                messages.error(request, f"Une erreur est survenue : {e}")
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire")
    else:
        # Pré-remplir le formulaire avec les données existantes de l'étudiant
        product_form_creation = PharmacieForms(instance=pharmacie)
        
    return render(request,"edit_pharmacie.html", {"product_form_creation": product_form_creation, "pharmacie": pharmacie})

# suppression d'une pharmacie
# def delete_pharmacie(request,id):
#     get_pharmacie = Pharmacie.objects.get(pk = id)
#     get_pharmacie.delete()
#     messages.success(request,'Suppression reussie')
#     return redirect('create_pharmacie')

def delete_pharmacie(request, id): 
    pharmacie = get_object_or_404(Pharmacie, pk=id) 
    if request.method == 'POST': 
        pharmacie.delete() 
        messages.success(request, 'Suppression réussie') 
        return redirect('create_pharmacie') 
    return render(request, 'pharmacie_confirm_delete.html', {'pharmacie':Pharmacie})


def confirmer_suppression_pharmacie(request, pharmacie_id):
    pharmacie = get_object_or_404(Pharmacie, id=pharmacie_id)
    
    if request.method == 'POST':
        pharmacie.delete()
        messages.success(request, 'Pharmacie supprimée avec succès.')
        return redirect('create_pharmacie')  # Rediriger vers la liste des pharmacies

    return render(request, 'pharmacie_confirm_delete.html', {'pharmacie': pharmacie})


def create_product(request):
    product_form_creation = ProductForms()
    if request.method == "POST":
        product_form_creation = ProductForms(request.POST)
        # Eviter les doublons dans le formulaire. A le copier dans toutes les vieuws du formulaire
        product_form_creation = ProductForms(request.POST)
        product = request.POST.get('nom')
        lot = request.POST.get('lot')
        get_all_products = Produit.objects.filter(nom=product,lot = lot)
        if product_form_creation.is_valid():
            if get_all_products.exists():
                messages.error(request,'Les donnees saisies existent déjà. Veuillez réessayer!')
                return redirect('create_product')
            else:
                # Fin de verification des doublons
                try:
                    product_form_creation.save()
                    messages.success(request, "Insertion réussie")
                    return redirect('create_product')  # Redirige pour vider le formulaire après enregistrement
                except Exception as e:
                    messages.error(request, f"Une erreur est survenue : {e}")
                
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire")
    
    product_form_creation = ProductForms()
    product_creations = Produit.objects.all()
    return render(request, "create_product.html", {"product_form_creation": product_form_creation, 'inscriptions': product_creations})  


def list_produit(request):
    product_form_creation = ProductForms()
    query = request.GET.get('q')
    if query:
        product_creations = Produit.objects.filter(nom__icontains=query)
    else:
        product_creations = Produit.objects.all()
    return render(request, "my_products.html", {"product_form_creation": product_form_creation, 'inscriptions': product_creations})


# Création de la vue d'édition des produits.
def edit_product(request, id):
    # Récupérer l'objet étudiant correspondant à l'ID
    produit = get_object_or_404(Produit, id=id)
    
    if request.method == "POST":
        # Pré-remplir le formulaire avec les données POST pour mise à jour
        product_form_creation = ProductForms(request.POST, instance=produit)
        if product_form_creation.is_valid():
            try:
                product_form_creation.save()
                messages.success(request, "Mise à jour réussie")
                return redirect("create_product")  # Rediriger après succès
            except Exception as e:
                messages.error(request, f"Une erreur est survenue : {e}")
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire")
    else:
        # Pré-remplir le formulaire avec les données existantes de l'étudiant
        product_form_creation = ProductForms(instance=produit)

    return render(request, "my_products.html", {"product_form_creation": product_form_creation, "produit": produit})

# suppression d'un produit
def delete_product(request,id):
    get_product = Produit.objects.get(pk = id)
    get_product.delete()
    messages.success(request,'Suppression reussie')
    return redirect('create_product')

# Vue pour la gestion des ventes des médicaments

def create_sale(request):
    vente_form_creation = VenteForm()
    produits = Produit.objects.all()

    # Récupérer le client à partir de la requête POST
    client_id = request.POST.get('client')
    client = Client.objects.get(id=client_id) if client_id else None

    if client:
        # Récupérer le panier du client ou en créer un nouveau
        panier, _ = Panier.objects.get_or_create(client=client, termine=False)
        # Récupérer les articles du panier, ou une liste vide si le panier n'existe pas
        articles_panier = ArticlePanier.objects.filter(panier=panier)
    else:
        panier, articles_panier = None, []

    # Préparer les données des produits pour le JavaScript
    produit_info = {
        produit.id: {
            "quantite_disponible": float(produit.quantite_en_stock),
            "prix_unitaire": float(produit.prix_unitaire),
            "date_expiration": produit.date_expiration.isoformat() if produit.date_expiration else None,
        }
        for produit in produits
    }

    if request.method == "POST":
        if 'add_to_cart' in request.POST:
            if not client:
                messages.error(request, "Veuillez sélectionner un client avant d'ajouter des produits au panier.")
                return redirect('create_sale')

            produit_id = request.POST.get("produit_id")
            quantite = int(request.POST.get("quantite_vendue", 0))

            try:
                produit = Produit.objects.get(id=produit_id)

                if quantite <= 0:
                    raise ValueError("La quantité doit être supérieure à zéro.")

                if produit.quantite_en_stock < quantite:
                    raise ValueError(f"Quantité insuffisante pour {produit.nom}. Disponible : {produit.quantite_en_stock}")

                article_panier, created = ArticlePanier.objects.get_or_create(panier=panier, produit=produit)
                article_panier.quantite += quantite
                article_panier.save()

                messages.success(request, f"{produit.nom} ajouté au panier.")
            except ObjectDoesNotExist:
                messages.error(request, "Le produit sélectionné n'existe pas.")
            except ValueError as e:
                messages.error(request, str(e))
            return redirect('create_sale')

        elif 'deliver_cart' in request.POST:
            if not client:
                messages.error(request, "Veuillez sélectionner un client avant de livrer le panier.")
                return redirect('create_sale')

            try:
                for article in articles_panier:
                    produit = article.produit
                    if produit.quantite_en_stock < article.quantite:
                        raise ValueError(f"Quantité insuffisante pour {produit.nom}")

                for article in articles_panier:
                    produit = article.produit
                    produit.quantite_en_stock -= article.quantite
                    produit.save()

                    # Créer une vente
                    vente = Vente(
                        produit=produit,
                        quantite_vendue=article.quantite,
                        prix_unitaire=produit.prix_unitaire,
                        client=panier.client,
                        prix_total=article.quantite * produit.prix_unitaire
                    )
                    vente.save()

                panier.termine = True
                panier.save()

                messages.success(request, "Produits livrés avec succès.")
            except ValueError as e:
                messages.error(request, str(e))
            return redirect('create_sale')

        elif 'create_sale' in request.POST:
            vente_form_creation = VenteForm(request.POST)
            if vente_form_creation.is_valid():
                try:
                    vente = vente_form_creation.save(commit=False)
                    produit = vente.produit

                    if produit.date_expiration and produit.date_expiration.date() <= date.today():
                        raise ValueError(f"Le produit {produit.nom} a expiré et ne peut pas être vendu.")

                    if produit.quantite_en_stock < vente.quantite_vendue:
                        raise ValueError(f"Quantité en stock insuffisante pour {produit.nom}. Disponible : {produit.quantite_en_stock}")

                    vente.prix_unitaire = produit.prix_unitaire
                    vente.prix_total = vente.quantite_vendue * vente.prix_unitaire

                    vente.save()

                    produit.quantite_en_stock -= vente.quantite_vendue
                    produit.save()

                    messages.success(request, "Vente enregistrée avec succès.")
                    return redirect('create_sale')
                except ValueError as e:
                    messages.error(request, f"Erreur lors de l'enregistrement de la vente : {e}")
            else:
                messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")

    vente_creations = Vente.objects.all()
    return render(request, "create_sale.html", {
        "vente_form_creation": vente_form_creation,
        "produit_info": json.dumps(produit_info, cls=DjangoJSONEncoder),
        "articles_panier": articles_panier,  # Assurez-vous que c'est toujours une liste, même vide
        "inscriptions": vente_creations,
        "clients": Client.objects.all(),
    })

# Vue pour ajouter des produits au panier

def ajouter_au_panier(request, id):
    try:
        # Affichage de l'ID du produit pour vérifier ce qui est reçu
        print(f"Produit ID reçu : {id}")

        # Tentative de récupération du produit
        produit = get_object_or_404(Produit, id=id)

        # Vérifier si un panier existe déjà dans la session
        panier_id = request.session.get('panier_id')
        if panier_id:
            panier = get_object_or_404(Panier, id=panier_id, termine=False)
        else:
            panier = Panier.objects.create(termine=False)  # Créer un panier temporaire
            request.session['panier_id'] = panier.id  # Enregistrer l'ID du panier dans la session

        # Vérifier la disponibilité en stock
        if produit.quantite_en_stock <= 0:
            messages.error(request, f"Le produit {produit.nom} est en rupture de stock.")
            return redirect('view_produits')

        # Obtenir ou créer un article dans le panier
        article_panier, created = ArticlePanier.objects.get_or_create(panier=panier, produit=produit)

        if produit.quantite_en_stock < article_panier.quantite + 1:
            messages.error(request, f"Quantité insuffisante pour {produit.nom}. Disponible : {produit.quantite_en_stock}.")
            return redirect('view_produits')

        # Ajouter une unité au panier
        article_panier.quantite += 1
        article_panier.save()

        messages.success(request, f"{produit.nom} ajouté au panier.")
        return redirect('view_produits')

    except Produit.DoesNotExist:
        # Message d'erreur si le produit n'existe pas
        messages.error(request, f"Le produit avec l'ID {id} n'existe pas.")
        return redirect('view_produits')

    except Exception as e:
        # Message d'erreur générique en cas de problème
        messages.error(request, f"Une erreur s'est produite : {str(e)}")
        return redirect('view_produits')


# Vue pour afficher le panier et livrer les produits

def view_panier(request):
    client = request.client
    panier = Panier.objects.get(client=client, termine=False)
    articles_panier = ArticlePanier.objects.filter(panier=panier)

    if request.method == "POST":
        # Vérification des stocks
        insuffisances = []
        for article in articles_panier:
            produit = article.produit
            if produit.quantite_en_stock < article.quantite:
                insuffisances.append(f"{produit.nom} (disponible : {produit.quantite_en_stock}, demandé : {article.quantite})")

        if insuffisances:
            messages.error(request, f"Quantité insuffisante pour : {', '.join(insuffisances)}")
            return redirect('view_panier')

        # Si tous les stocks sont disponibles, effectuer les opérations dans une transaction
        try:
            with transaction.atomic():
                for article in articles_panier:
                    produit = article.produit
                    # Mise à jour des stocks
                    produit.quantite_en_stock -= article.quantite
                    produit.save()

                    # Création de la vente
                    vente = Vente(
                        produit=produit,
                        quantite_vendue=article.quantite,
                        prix_unitaire=produit.prix_unitaire,
                        prix_total=article.quantite * produit.prix_unitaire,
                        client=client,
                        date_vente=timezone.now()
                    )
                    vente.save()

                # Marquer le panier comme terminé
                panier.termine = True
                panier.date_fermeture = timezone.now()
                panier.save()

            messages.success(request, "Produits livrés avec succès.")
            return redirect('view_produits')
        except Exception as e:
            messages.error(request, f"Une erreur est survenue lors de la livraison : {str(e)}")
            return redirect('view_panier')

    return render(request, "view_panier.html", {"panier": panier, "articles_panier": articles_panier})


# Vue pour supprimer un article du panier

def remove_from_cart(request, article_id):
    article = ArticlePanier.objects.get(id=article_id)
    article.delete()
    messages.success(request, "Article retiré du panier avec succès.")
    return redirect('view_panier')
 
  
# Création de la vue d'édition des ventes

def edit_sale(request, sale_id):
    # Récupérer la vente à modifier
    vente = get_object_or_404(Vente, id=sale_id)
    vente_form = VenteForm(instance=vente)

    if request.method == "POST":
        vente_form = VenteForm(request.POST, instance=vente)
        if vente_form.is_valid():
            try:
                updated_vente = vente_form.save(commit=False)
                produit = updated_vente.produit

                # Vérifier la date d'expiration du produit
                expiration_date = produit.date_expiration
                if expiration_date and expiration_date.date() <= date.today():
                    raise ValueError(f"Le produit {produit.nom} a expiré et ne peut pas être vendu.")

                # Vérifier la quantité en stock (en tenant compte de la quantité précédemment vendue)
                quantite_difference = updated_vente.quantite_vendue - vente.quantite_vendue
                if produit.quantite_en_stock < quantite_difference:
                    raise ValueError(f"Quantité en stock insuffisante pour {produit.nom}. Disponible : {produit.quantite_en_stock}")

                # Mettre à jour le stock
                produit.quantite_en_stock -= quantite_difference
                produit.save()

                # Calculer le prix unitaire et le prix total
                updated_vente.prix_unitaire = produit.prix_unitaire
                updated_vente.prix_total = updated_vente.quantite_vendue * updated_vente.prix_unitaire

                # Sauvegarder les modifications
                updated_vente.save()

                messages.success(request, "Vente mise à jour avec succès.")
                return redirect("create_sale")

            except ValueError as e:
                messages.error(request, f"Erreur lors de la mise à jour de la vente : {e}")

    return render(request, "edit_sale.html", {
        "vente_form": vente_form,
        "vente": vente,
    })

# suppression d'un client
def delete_sale(request,id):
    get_sale = Vente.objects.get(pk = id)
    get_sale.delete()
    messages.success(request,'Suppression réussie')
    return redirect('create_sale')

# Creation de la vue du Client

def create_client(request):
    client_form_creation = ClientForms()
    if request.method == "POST":
        client_form_creation = ClientForms (request.POST,request.FILES)
         # Eviter les doublons dans le formulaire. A le copier dans toutes les vieuws du formulaire
        identite = request.POST.get('identite')
        get_all_clients = Client.objects.filter(identite=identite)
        if client_form_creation.is_valid():
            if get_all_clients.exists():
                messages.error(request,'Le client avec ce numéro d\'identité existent déjà. Veuillez réessayer!')
                return redirect('create_client')
                # Fin de verification des doublons
            else:
                try:
                    client_form_creation.save()
                    messages.success(request, "Insertion réussie")
                    client_form_creation = ClientForms ()
                except Exception as e:
                    messages.error(request, f"Une erreur est survenue : {e}")
        else:
            print(client_form_creation.errors)
            messages.error(request, "Veuillez corriger les erreurs du formulaire")
    
    client_creations = Client.objects.all()
    return render(request, "create_client.html", {"client_form_creation": client_form_creation, 'inscriptions': client_creations})

# def create_client(request):
#     product_form_creation = ClientForms()
#     if request.method == "POST":
#         print(request.POST)
#         product_form_creation = ClientForms(request.POST,request.FILES)
        
#         if product_form_creation.is_valid():
#             try:
#                 instance = product_form_creation.save()
               
#                 messages.success(request, "Insertion réussie")
#                 product_form_creation = ClientForms()
#             except Exception as e:
#                 messages.error(request, f"Une erreur est survenue : {e}")
#         else:
#             messages.error(request, "Veuillez corriger les erreurs du formulaire")
    
#     product_form_creation = ClientForms()
#     client_creations = Client.objects.all()
#     return render(request, "create_client.html", {"product_form_creation": product_form_creation, 'inscriptions': client_creations})

# Liste des clients:
def list_client(request):
    client_form_creation = ClientForms()
    query = request.GET.get('q')
    if query:
        client_creations = Client.objects.filter(nom__icontains=query)
    else:
        client_creations = Client.objects.all()
    return render(request, "mes_clients.html", {"client_form_creation": client_form_creation, 'inscriptions': client_creations})


# Création de la vue d'édition des clients
def edit_client(request, id):
    # Récupérer l'objet étudiant correspondant à l'ID
    client = get_object_or_404(Client, id=id)
    
    if request.method == "POST":
        # Pré-remplir le formulaire avec les données POST pour mise à jour
        client_form_creation = ClientForms(request.POST, instance=client)

        if client_form_creation.is_valid():
            try:
                client_form_creation.save()
                messages.success(request, "Mise à jour réussie")
                return redirect("create_client")  # Rediriger après succès
            except Exception as e:
                messages.error(request, f"Une erreur est survenue : {e}")
        else:
            messages.error(request, " Le formulaire n'est pas bien rempli!")
    else:
        # Pré-remplir le formulaire avec les données existantes de l'étudiant
        client_form_creation = ClientForms(instance=client)

    return render(request, "edit_client.html", {"client_form_creation": client_form_creation, "client": client})

# suppression d'un client
def delete_client(request,id):
    get_client = Client.objects.get(pk = id)
    get_client.delete()
    messages.success(request,'Suppression reussie')
    return redirect('mes_clients')


#Liste des clients: 

# Vue pour la géneration des factures

def create_invoice(request):
    if request.method == "POST":
        facture_form = FactureForm(request.POST)
        if facture_form.is_valid():
            facture = facture_form.save()
            return redirect('invoice_detail', facture_id=facture.id)
    else:
        facture_form = FactureForm()
    return render(request, 'create_invoice.html', {'facture_form': facture_form})

def invoice_detail(request, facture_id):
    facture = get_object_or_404(Facture, id=facture_id)
    transactions = facture.transactions.all()
    return render(request, 'invoice_detail.html', {'facture': facture, 'transactions': transactions})

def create_transaction(request, facture_id):
    facture = get_object_or_404(Facture, id=facture_id)
    if request.method == "POST":
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            transaction = transaction_form.save(commit=False)
            transaction.facture = facture
            transaction.save()
            produit = transaction.produit
            produit.quantite_en_stock -= transaction.quantite
            produit.save()
            return redirect('invoice_detail', facture_id=facture.id)
    else:
        transaction_form = TransactionForm()
    return render(request, 'create_transaction.html', {'transaction_form': transaction_form, 'facture': facture})


# Vue pour la génération du rapport

def generate_report(request):
    if request.method == "POST":
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        transactions = Transaction.objects.filter(date__range=[start_date, end_date])
        total_amount = transactions.aggregate(total=models.Sum('total'))['total']
        return render(request, 'report.html', {'transactions': transactions, 'total_amount': total_amount, 'start_date': start_date, 'end_date': end_date})
    return render(request, 'report_form.html')


# Fin de facture

# Création de la vue d'enregistrement des commandes
def create_commande(request):
    commande_form_creation = CommandeForms()
    if request.method == "POST":
        commande_form_creation = CommandeForms(request.POST)
        if commande_form_creation.is_valid():
            try:
                commande_form_creation.save()
                messages.success(request, "Insertion réussie")
                commande_form_creation = CommandeForms ()
            except Exception as e:
                messages.error(request, f"Une erreur est survenue : {e}")
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire")
    
    commande_creations = Commande.objects.all()
    return render(request, "create_commande.html", {"commande_form_creation": commande_form_creation, 'inscriptions': commande_creations})

# Création de la vue d'édition des clients
def edit_commande(request, id):
    # Récupérer l'objet étudiant correspondant à l'ID
    commande = get_object_or_404(Commande, id=id)
    
    if request.method == "POST":
        # Pré-remplir le formulaire avec les données POST pour mise à jour
        product_form_creation = CommandeForms(request.POST, instance=commande)

        if product_form_creation.is_valid():
            try:
                product_form_creation.save()
                messages.success(request, "Mise à jour réussie")
                return redirect("create_commande")  # Rediriger après succès
            except Exception as e:
                messages.error(request, f"Une erreur est survenue : {e}")
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire")
    else:
        # Pré-remplir le formulaire avec les données existantes de notre commande
        product_form_creation = CommandeForms(instance=commande)

    return render(request, "edit_commande.html", {"product_form_creation": product_form_creation, "commande": commande})

# suppression d'une commande
def delete_commande(request,id):
    get_commande = Commande.objects.get(pk = id)
    get_commande.delete()
    messages.success(request,'Suppression reussie')
    return redirect('create_commande')


# Création de vue de ligne de commande
# def create_ligne_commande(request):
    ligne_commande_form_creation = LigneCommandeForms()
    if request.method == "POST":
        ligne_commande_form_creation = LigneCommandeForms (request.POST)
        if ligne_commande_form_creation.is_valid():
            try:
                ligne_commande_form_creation.save()
                messages.success(request, "Insertion réussie")
                ligne_commande_form_creation = LigneCommandeForms ()
            except Exception as e:
                messages.error(request, f"Une erreur est survenue : {e}")
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire")
    
    ligne_commande_form_creations = LigneCommande.objects.all()
    return render(request, "create_ligne_commande.html", {"ligne_commande_form_creation": ligne_commande_form_creation, 'inscriptions': ligne_commande_form_creations})

# Création de la vue d'édition de ligne de commande
# def edit_ligne_commande(request, id):
    # Récupérer l'objet étudiant correspondant à l'ID
    ligne_commande = get_object_or_404(LigneCommande, id=id)
    
    if request.method == "POST":
        # Pré-remplir le formulaire avec les données POST pour mise à jour
        product_form_creation = LigneCommandeForms(request.POST, instance=ligne_commande)

        if product_form_creation.is_valid():
            try:
                product_form_creation.save()
                messages.success(request, "Mise à jour réussie")
                return redirect("create_ligne_commande")  # Rediriger après succès
            except Exception as e:
                messages.error(request, f"Une erreur est survenue : {e}")
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire")
    else:
        # Pré-remplir le formulaire avec les données existantes de notre commande
        product_form_creation = LigneCommandeForms(instance=ligne_commande)

    return render(request, "edit_ligne_commande.html", {"product_form_creation": product_form_creation, "ligne_commande": ligne_commande})

# suppression d'une ligne de commande
# def delete_ligne_commande(request,id):
    get_ligne_commande = LigneCommande.objects.get(pk = id)
    get_ligne_commande.delete()
    messages.success(request,'Suppression reussie')
    return redirect('create_ligne_commande')


# Creation de la vue de création des fournisseurs

def create_fournisseur(request):
    fournisseur_form_creation = FournisseurForms()
    if request.method == "POST":
        fournisseur_form_creation = FournisseurForms (request.POST)
        if fournisseur_form_creation.is_valid():
            try:
                fournisseur_form_creation.save()
                messages.success(request, "Insertion réussie")
                fournisseur_form_creation = FournisseurForms ()
            except Exception as e:
                messages.error(request, f"Une erreur est survenue : {e}")
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire")
    
    fournisseur_form_creations = Fournisseur.objects.all()
    return render(request, "create_fournisseur.html", {"fournisseur_form_creation": fournisseur_form_creation, 'inscriptions': fournisseur_form_creations})

# Création de la vue d'édition des fournisseurs
def edit_fournisseur(request, id):
    # Récupérer l'objet étudiant correspondant à l'ID
    fournisseur = get_object_or_404(Fournisseur, id=id)
    
    if request.method == "POST":
        # Pré-remplir le formulaire avec les données POST pour mise à jour
        product_form_creation = FournisseurForms(request.POST, instance=fournisseur)

        if product_form_creation.is_valid():
            try:
                product_form_creation.save()
                messages.success(request, "Mise à jour réussie")
                return redirect("create_fournisseur")  # Rediriger après succès
            except Exception as e:
                messages.error(request, f"Une erreur est survenue : {e}")
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire")
    else:
        # Pré-remplir le formulaire avec les données existantes de notre commande
        product_form_creation = FournisseurForms(instance=fournisseur)

    return render(request, "edit_fournisseur.html", {"product_form_creation": product_form_creation, "ligne_commande": fournisseur})

# suppression d'un fournisseur
def delete_fournisseur(request,id):
    get_fournisseur = Fournisseur.objects.get(pk = id)
    get_fournisseur.delete()
    messages.success(request,'Suppression reussie')
    return redirect('create_fournisseur')


# Vue de création des inventaires 

def create_inventaire(request):
    inventaire_form_creation = InventaireForms()
    if request.method == "POST":
        inventaire_form_creation = InventaireForms (request.POST)
        if inventaire_form_creation.is_valid():
            try:
                inventaire_form_creation.save()
                messages.success(request, "Insertion réussie")
                inventaire_form_creation = InventaireForms()
            except Exception as e:
                messages.error(request, f"Une erreur est survenue : {e}")
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire")
    
    inventaire_form_creations = Inventaire.objects.all()
    return render(request, "inventaire.html", {"inventaire_form_creation": inventaire_form_creation, 'inscriptions': inventaire_form_creations})

# Création de la vue d'édition des inventaires
def edit_inventaire(request, id):
    # Récupérer l'objet étudiant correspondant à l'ID
    inventaire = get_object_or_404(Inventaire, id=id)
    
    if request.method == "POST":
        # Pré-remplir le formulaire avec les données POST pour mise à jour
        product_form_creation =InventaireForms(request.POST, instance=inventaire)

        if product_form_creation.is_valid():
            try:
                product_form_creation.save()
                messages.success(request, "Mise à jour réussie")
                return redirect("create_inventaire")  # Rediriger après succès
            except Exception as e:
                messages.error(request, f"Une erreur est survenue : {e}")
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire")
    else:
        # Pré-remplir le formulaire avec les données existantes de notre commande
        product_form_creation = InventaireForms(instance=inventaire)

    return render(request, "edit_inventaire.html", {"product_form_creation": product_form_creation, "ligne_commande": inventaire})

# suppression d'inventaire
def delete_inventaire(request,id):
    get_inventaire = Inventaire.objects.get(pk = id)
    get_inventaire.delete()
    messages.success(request,'Suppression reussie')
    return redirect('create_inventaire')


# Vue pour la création des ordonances 
def create_recette(request):
    recette_form_creation = RecetteForms()
    if request.method == "POST":
        recette_form_creation = RecetteForms(request.POST)
        if recette_form_creation.is_valid():
            try:
                recette_form_creation.save()
                messages.success(request, "Insertion réussie")
                recette_form_creation = RecetteForms()
            except Exception as e:
                messages.error(request, f"Une erreur est survenue : {e}")
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire")
    
    recette_form_creations = Recette.objects.all()
    return render(request, "create_recette.html", {"recette_form_creation": recette_form_creation, 'inscriptions': recette_form_creations})

# Vue pour l'édition/modification de recette
def edit_recette(request, id):
    # Récupérer l'objet étudiant correspondant à l'ID
    recette = get_object_or_404(Recette, id=id)
    
    if request.method == "POST":
        # Pré-remplir le formulaire avec les données POST pour mise à jour
        product_form_creation =RecetteForms(request.POST, instance=recette)

        if product_form_creation.is_valid():
            try:
                product_form_creation.save()
                messages.success(request, "Mise à jour réussie")
                return redirect("create_recette")  # Rediriger après succès
            except Exception as e:
                messages.error(request, f"Une erreur est survenue : {e}")
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire")
    else:
        # Pré-remplir le formulaire avec les données existantes de notre commande
        product_form_creation = RecetteForms(instance=recette)

    return render(request, "edit_recette.html", {"product_form_creation": product_form_creation, "ligne_commande": recette})

# suppression d'une recette
def delete_recette(request,id):
    get_recette = Recette.objects.get(pk = id)
    get_recette.delete()
    messages.success(request,'Suppression reussie')
    return redirect('create_recette')


# Vue de création des produits à presrire
def create_recette_product(request):
    recette_product_form_creation = ProduitRecetteForms()
    if request.method == "POST":
        recette_product_form_creation = ProduitRecetteForms(request.POST)
        if recette_product_form_creation.is_valid():
            try:
                recette_product_form_creation.save()
                messages.success(request, "Insertion réussie")
                recette_product_form_creation = ProduitRecetteForms()
            except Exception as e:
                messages.error(request, f"Une erreur est survenue : {e}")
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire")
    
    recette_product_form_creations = ProduitRecette.objects.all()
    return render(request, "create_recette_product.html", {"recette_product_form_creation": recette_product_form_creation, 'inscriptions': recette_product_form_creations})
# Vue pour l'édition/modification 
def edit_recette_produit(request, id):
    # Récupérer l'objet étudiant correspondant à l'ID
    recette_produit = get_object_or_404(ProduitRecetteForms, id=id)
    
    if request.method == "POST":
        # Pré-remplir le formulaire avec les données POST pour mise à jour
        product_form_creation =ProduitRecetteForms(request.POST, instance=recette_produit)

        if product_form_creation.is_valid():
            try:
                product_form_creation.save()
                messages.success(request, "Mise à jour réussie")
                return redirect("create_recette")  # Rediriger après succès
            except Exception as e:
                messages.error(request, f"Une erreur est survenue : {e}")
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire")
    else:
        # Pré-remplir le formulaire avec les données existantes de notre commande
        product_form_creation = ProduitRecetteForms(instance=recette_produit)

    return render(request, "edit_produit_recette.html", {"product_form_creation": product_form_creation, "produit_recette": recette_produit})


# suppression d'un produit recette
def delete_recette_produit(request,id):
    get_recette_produit = ProduitRecette.objects.get(pk = id)
    get_recette_produit.delete()
    messages.success(request,'Suppression reussie')
    return redirect('create_recette_produit')

# # vue pour gérer le téléchargement :
# from .forms import MediaFileForm

# def upload_file(request):
#     if request.method == 'POST':
#         form = MediaFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('file_list')  # Redirige vers une vue qui liste les fichiers
#     else:
#         form = MediaFileForm()
#     return render(request, 'upload.html', {'form': form})

# # Vue pour Afficher les fichiers téléchargés 
# def file_list(request):
#     files = MediaFile.objects.all()
#     return render(request, 'file_list.html', {'files': files})

