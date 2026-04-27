from django.core.management.base import BaseCommand
from products.models import Category, Product
import random

class Command(BaseCommand):
    help = 'Génère les données fictives pour les produits'
    
    def handle(self, *args, **options):
        # Données statiques
        category_names = ['Pizza', 'Pasta', 'Desserts', 'Boissons', 'Salades']
        product_names = [
            'Margherita', 'Carbonara', 'Tiramisu', 'Coca Cola', 'Salade César',
            'Quattro Formaggi', 'Bolognese', 'Panna Cotta', 'Fanta Orange', 'Salade Tomate'
        ]
        descriptions = [
            'Un délicieux plat savoureux',
            'Parfait pour le repas du jour',
            'Une spécialité maison authentique',
            'Préparé avec les meilleurs ingrédients',
            'Un incontournable de notre menu'
        ]
        
        categories = []
        
        # Créer les catégories
        for name in category_names:
            slug = name.lower().replace(' ', '-')
            categorie, created = Category.objects.get_or_create(
                name=name,
                defaults={'slug': slug}
            )
            if created:
                categories.append(categorie)
                self.stdout.write(f'✓ Catégorie créée: {name}')
            else:
                categories.append(categorie)
        
        # Créer les produits
        for i, product_name in enumerate(product_names):
            product, created = Product.objects.get_or_create(
                name=product_name,
                defaults={
                    'description': descriptions[i % len(descriptions)],
                    'price': random.randint(5, 30),
                    'stock': random.randint(10, 100),
                    'category': random.choice(categories)
                }
            )
            if created:
                self.stdout.write(f'✓ Produit {i+1} créé: {product_name}')
            else:
                self.stdout.write(f'~ Produit déjà existant: {product_name}')
        
        self.stdout.write(self.style.SUCCESS('✓ Données chargées avec succès!'))
