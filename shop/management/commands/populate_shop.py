from django.core.management.base import BaseCommand
from django.utils.text import slugify
from shop.models import Category, Product

class Command(BaseCommand):
    help = "Populate the database with sample categories and products"

    def handle(self, *args, **options):
        # Create 5 categories
        categories = ["Electronics", "Books", "Clothing", "Home & Kitchen", "Toys & Games"]
        category_objs = []
        for name in categories:
            obj, created = Category.objects.get_or_create(name=name, defaults={"slug": slugify(name)})
            category_objs.append(obj)
            self.stdout.write(f"Category '{name}' created: {created}")

        # Create 20 products (4 existing + 16 more)
        products = [
            {"name": "Wireless Headphones", "price": 59.99, "stock": 20, "category": category_objs[0]},
            {"name": "Python Programming Book", "price": 29.99, "stock": 15, "category": category_objs[1]},
            {"name": "Men's T-Shirt", "price": 19.99, "stock": 30, "category": category_objs[2]},
            {"name": "Blender 3000", "price": 89.99, "stock": 10, "category": category_objs[3]},
            {"name": "Smartphone", "price": 399.99, "stock": 25, "category": category_objs[0]},
            {"name": "Laptop", "price": 999.99, "stock": 8, "category": category_objs[0]},
            {"name": "Digital Camera", "price": 549.99, "stock": 12, "category": category_objs[0]},
            {"name": "E-reader", "price": 129.99, "stock": 20, "category": category_objs[1]},
            {"name": "Cookbook", "price": 24.99, "stock": 18, "category": category_objs[1]},
            {"name": "Jeans", "price": 49.99, "stock": 22, "category": category_objs[2]},
            {"name": "Jacket", "price": 79.99, "stock": 15, "category": category_objs[2]},
            {"name": "Sneakers", "price": 69.99, "stock": 20, "category": category_objs[2]},
            {"name": "Coffee Maker", "price": 99.99, "stock": 10, "category": category_objs[3]},
            {"name": "Vacuum Cleaner", "price": 149.99, "stock": 8, "category": category_objs[3]},
            {"name": "Desk Chair", "price": 119.99, "stock": 14, "category": category_objs[3]},
            {"name": "Action Figure", "price": 24.99, "stock": 30, "category": category_objs[4]},
            {"name": "Board Game", "price": 39.99, "stock": 25, "category": category_objs[4]},
            {"name": "Toy Train", "price": 49.99, "stock": 20, "category": category_objs[4]},
            {"name": "Puzzle Set", "price": 19.99, "stock": 28, "category": category_objs[4]},
            {"name": "Yoga Mat", "price": 29.99, "stock": 20, "category": category_objs[4]},
        ]

        for p in products:
            obj, created = Product.objects.get_or_create(
                name=p["name"],
                defaults={
                    "slug": slugify(p["name"]),
                    "description": f"This is a {p['name']}.",
                    "price": p["price"],
                    "stock": p["stock"],
                    "category": p["category"],
                    "is_active": True
                }
            )
            self.stdout.write(f"Product '{p['name']}' created: {created}")
