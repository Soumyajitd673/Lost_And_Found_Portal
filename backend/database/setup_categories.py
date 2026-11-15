from sqlalchemy import select
from backend.database.db import SessionLocal
from backend.models.category import Category

categories = [
    'Electronics & Gadgets',
    'Documents & IDs',
    'Wallets, money and cards',
    'Bags and carriers',
    'Keys and access items',
    'Clothing & Footwear',
    'Academic & Lab Items',
    'Accessories and jewelleries',
    'Sports and fitness gear',
    'Vehicles and vehicle accessories',
    'Personal Care & Health items',
    'Food, drink and utensils',
    'Others'
]

def setup_categories():
    with SessionLocal() as db:
        for name in categories:
            existing = db.scalar(
                select(Category).where(Category.name == name)
            )

            if not existing:
                db.add(Category(name=name))

        db.commit()