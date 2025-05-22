from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session
from models.product import Product

class ProductRepository:
    """Repository class for handling product database operations."""

    def __init__(self, db: Session):
        self.db = db

    def create_product(self, product_data: dict) -> Product:
        """Create a new product."""
        new_product = Product(
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'],
            stock=product_data['stock'],
            category=product_data['category']
        )
        self.db.add(new_product)
        self.db.commit()
        self.db.refresh(new_product)
        return new_product

    def delete_product(self, product_id: int) -> bool:
        """Delete a product by ID."""
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if product:
            self.db.delete(product)
            self.db.commit()
            return True
        return False

    def update_product(self, product_id: int, update_data: dict) -> Optional[Product]:
        """Update a product by ID."""
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if product:
            for key, value in update_data.items():
                if key != 'id':  # Skip the id field
                    setattr(product, key, value)
            product.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(product)
            return product
        return None

    def get_product(self, product_id: int) -> Optional[Product]:
        """Get a product by ID."""
        return self.db.query(Product).filter(Product.id == product_id).first()

    def get_all_products(self) -> List[Product]:
        """Get all products."""
        return self.db.query(Product).all() 