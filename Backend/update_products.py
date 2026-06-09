from database import SessionLocal
from models import Product

db = SessionLocal()

updates = {
    "Filtre Kahve": {"image_url": "/images/filtre-kahve.jpg", "category": "Kahve"},
    "Espresso Blend": {"image_url": "/images/espresso-blend.jpg", "category": "Kahve"},
    "Fındıklı Kurabiye": {"image_url": "/images/findikli-kurabiye.jpg", "category": "Atistirmaliklar"},
    "Kırmızı Termos": {"image_url": "/images/kirmizi-termos.jpg", "category": "Termos"},
    "Siyah Mug": {"image_url": "/images/siyah-mug.jpg", "category": "Aksesuar"},
    "Kahve Öğütücü": {"image_url": "/images/kahve-ogutucusu.jpg", "category": "Aksesuar"},
    "V60 Dripper": {"image_url": "/images/v60-dripper.jpg", "category": "Aksesuar"},
    "Earl Grey Çay": {"image_url": "/images/earl-grey.jpg", "category": "Caylar"}
}

for product in db.query(Product).all():
    if product.name in updates:
        product.image_url = updates[product.name]["image_url"]
        product.category = updates[product.name]["category"]

db.commit()
print("Products updated successfully!")
db.close()
