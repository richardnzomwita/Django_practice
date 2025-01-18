from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home,name='home'),
    # path('', views.acceuil),
    path('create_pharmacie/', views.create_pharmacie, name='create_pharmacie'),
    path('edit_pharmacie/<int:id>',views.edit_pharmacie,name="edit_pharmacie"),
    path('delete_pharmacie/<int:id>',views.delete_pharmacie,name="delete_pharmacie"), 
    # path('pharmacie/supprimer/<int:id>/', views.delete_pharmacie, name='delete_pharmacie'), 
    path('pharmacie/supprimer/<int:pharmacie_id>/', views.confirmer_suppression_pharmacie, name='confirmer_suppression_pharmacie'),
     
    path('create_product/', views.create_product, name='create_product'),
    path('edit_product/<int:id>',views.edit_product,name="edit_product"),  
    path('delete_product/<int:id>',views.delete_product,name="delete_product"),
    path('my_products',views.list_produit,name="my_products"),
    path('create_sale/',views.create_sale,name="create_sale"),
    path('edit_sale/<int:id>',views.edit_sale,name="edit_sale"),
    path('delete_sale/<int:id>',views.delete_sale,name="delete_sale"),
    path('create_client/', views.create_client, name='create_client'),
    path('mes_clients/', views.list_client, name='mes_clients'),
    path('edit_client/<int:id>',views.edit_client,name="edit_client"),
    path('delete_client/<int:id>',views.delete_client,name="delete_client"),
    
    path('add_to_cart/<int:produit_id>/', views.ajouter_au_panier, name='add_to_cart'),
    path('view_panier/', views.view_panier, name='view_panier'),
    path('remove_from_cart/<int:article_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('create_sale/', views.create_sale, name='create_sale'),

    # path('create_invoice/', views.create_invoice, name='create_invoice'),
    # path('invoice/<int:facture_id>/', views.invoice_detail, name='invoice_detail'),
    # path('invoice/<int:facture_id>/create_transaction/', views.create_transaction, name='create_transaction'),
    # path('generate_report/', views.generate_report, name='generate_report'),

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),#Displays the form to enter the email address for password reset.
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),#Displays a message indicating that a password reset link has been sent.
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),#Displays the form to reset the password, using the token from the email.
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),#Displays a success message once the password has been successfully changed.
    
    # path('home/', views.home, name='home'),
    path('create_invoice/', views.create_invoice, name='create_invoice'),
    path('invoice/<int:facture_id>/', views.invoice_detail, name='invoice_detail'),
    path('invoice/<int:facture_id>/create_transaction/', views.create_transaction, name='create_transaction'),
    path('generate_report/', views.generate_report, name='generate_report'),
        
    path('create_commande/', views.create_commande, name='create_commande'),
    path('edit_commande/<int:id>',views.edit_commande,name="edit_commande"),  
    path('delete_commande/<int:id>',views.delete_commande,name="delete_commande"),   
    # path('create_ligne_commande/', views.create_ligne_commande, name='create_ligne_commande'),
    # path('edit_ligne_commande/<int:id>',views.edit_ligne_commande,name="edit_ligne_commande"),  
    # path('delete_ligne_commande/<int:id>',views.delete_ligne_commande,name="delete_ligne_commande"),      
    path('create_fournisseur/', views.create_fournisseur, name='create_fournisseur'),
    path('edit_fournisseur/<int:id>',views.edit_fournisseur,name="edit_fournisseur"), 
    path('delete_fournisseur/<int:id>',views.delete_fournisseur,name="delete_fournisseur"),       
    path('create_inventaire/', views.create_inventaire, name='create_inventaire'),
    path('edit_inventaire/<int:id>',views.edit_inventaire,name="edit_inventaire"),  
    path('delete_inventaire/<int:id>',views.delete_inventaire,name="delete_inventaire"),     
    path('create_recette/', views.create_recette, name='create_recette'),
    path('edit_recette/<int:id>',views.edit_recette,name="edit_recette"),   
    path('delete_recette/<int:id>',views.delete_recette,name="delete_recette"),     
    path('create_produit_recette/', views.create_recette_product, name='create_produit_recette'),
    path('edit_produit_recette/<int:id>',views.edit_recette,name="edit_produit_recette"), 
    path('delete_product_recette/<int:id>',views.delete_recette_produit,name="delete_product_recette"),
    
    ]
