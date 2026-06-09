from database import SessionLocal
from models import Product

products = [
    {"name": "Filtre Kahve", "price": 50.0, "original_price": 60.0, "image_url": "/images/FiltreKahve.png", "category": "kahve", "description": "Taze demlenmiş filtre kahve."},
    {"name": "Espresso Blend", "price": 80.0, "original_price": None, "image_url": "/images/EspressoBlend.png", "category": "kahve", "description": "Yoğun espresso blend."},
    {"name": "Fındıklı Kurabiye", "price": 40.0, "original_price": None, "image_url": "/images/FindikliKurabiye.png", "category": "tatli", "description": "Taze fındıklı kurabiye."},
    {"name": "Kırmızı Termos", "price": 250.0, "original_price": 300.0, "image_url": "/images/KirmiziTermos.png", "category": "aksesuar", "description": "Sıcak tutan kırmızı termos."},
    {"name": "Siyah Mug", "price": 150.0, "original_price": None, "image_url": "/images/SiyahMug.png", "category": "aksesuar", "description": "Şık siyah mug."},
    {"name": "Kahve Öğütücü", "price": 450.0, "original_price": 500.0, "image_url": "/images/KahveOgutucu.png", "category": "ekipman", "description": "Profesyonel kahve öğütücü."},
    {"name": "V60 Dripper", "price": 180.0, "original_price": 200.0, "image_url": "/images/V60Dripper.png", "category": "ekipman", "description": "Seramik V60 dripper."},
    {"name": "Earl Grey Çay", "price": 45.0, "original_price": None, "image_url": "/images/EarlGrey.png", "category": "cay", "description": "Klasik Earl Grey çayı."}
]

db = SessionLocal()
for p in products:
    db.add(Product(**p))
db.commit()
print("Database seeded directly via SQLAlchemy!")
db.close()
