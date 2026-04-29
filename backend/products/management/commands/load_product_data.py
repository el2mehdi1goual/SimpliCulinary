import shutil
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from products.data import products as PRODUCTS_DATA
from products.models import Category, Product


class Command(BaseCommand):
    help = "Charge la table Product (et les catégories) à partir de products/data.py."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Supprime tous les produits et toutes les catégories avant import.",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            deleted_p, _ = Product.objects.all().delete()
            deleted_c, _ = Category.objects.all().delete()
            self.stdout.write(
                self.style.WARNING(
                    f"Purge: {deleted_p} produit(s), {deleted_c} categorie(s) supprimes."
                )
            )

        static_root = Path(settings.BASE_DIR) / "Static"
        media_products = Path(settings.MEDIA_ROOT) / "products"
        media_products.mkdir(parents=True, exist_ok=True)

        for item in PRODUCTS_DATA:
            cat_name = (item.get("category") or "Sans catégorie").strip()[:250]
            slug_base = slugify(cat_name) or "categorie"
            slug = slug_base[:50]
            category, _ = Category.objects.get_or_create(
                name=cat_name,
                defaults={"slug": slug},
            )

            name = item["name"][:250]
            product, created = Product.objects.update_or_create(
                name=name,
                defaults={
                    "description": item.get("description") or "",
                    "price": item["price"],
                    "stock": max(0, int(item.get("countInStock") or 0)),
                    "category": category,
                },
            )

            rel_img = (item.get("image") or "").strip().lstrip("/").replace("\\", "/")
            if rel_img:
                src = static_root / Path(rel_img)
                if src.is_file():
                    dest_name = src.name
                    dest_path = media_products / dest_name
                    shutil.copy2(src, dest_path)
                    with dest_path.open("rb") as fh:
                        product.image.save(dest_name, File(fh), save=True)
                    self.stdout.write(f"  Image OK: {name} <- {rel_img}")
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"  Image manquante (ignoree): {src}"
                        )
                    )

            verb = "Cree" if created else "MAJ"
            self.stdout.write(self.style.SUCCESS(f"{verb}: {name}"))

        self.stdout.write(self.style.SUCCESS("Import termine."))
