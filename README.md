# ☕ Espressolab Enterprise E-Commerce & Management System

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg?style=flat-square&logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Backend-Django%20%2F%20FastAPI-green.svg?style=flat-square&logo=django)](https://djangoproject.com/)
[![Vue.js](https://img.shields.io/badge/Frontend-Vue.js%20%2F%20Nuxt%203-4fc08d.svg?style=flat-square&logo=vue.js)](https://vuejs.org/)
[![RabbitMQ](https://img.shields.io/badge/Message%20Queue-RabbitMQ-orange.svg?style=flat-square&logo=rabbitmq)](https://www.rabbitmq.com/)
[![Stripe](https://img.shields.io/badge/Payment-Stripe%20API-blueviolet.svg?style=flat-square&logo=stripe)](https://stripe.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003b57.svg?style=flat-square&logo=sqlite)](https://www.sqlite.org/)

Bu proje, Türkiye’nin en büyük üçüncü nesil kahve zincirlerinden biri olan **Espressolab**’in kurumsal operasyonlarını, B2C satış kanallarını, müşteri sipariş süreçlerini ve bayi (Franchising) yönetim süreçlerini dijitalleştirmek amacıyla geliştirilmiş kapsamlı bir **Kurumsal E-Ticaret Otomasyon ve Bilgi Yönetim Sistemi**dir. 

Sistem; son kullanıcıların üyelik oluşturup alışveriş yapabildikleri, online/offline ödemelerle sipariş verebildikleri, ürünlere puan ve yorum bırakabildikleri **Satış Modülleri** ile yöneticilerin tüm bu süreçleri denetleyebildikleri kapsamlı bir **Admin Yönetim Paneli** içerir.

---

## 🛠️ Teknik Yığın (Tech Stack)

Proje, modern yazılım mimarisi prensiplerine uygun olarak **Thin Client (Frontend)** ve **RESTful API (Backend)** mimarisiyle iki bağımsız katmanda yapılandırılmıştır:

*   **Backend (Sunucu Katmanı):** Core iş mantığı, veritabanı ilişkileri ve yönetim servisleri **Python (Django)** altyapısı ve **FastAPI** RESTful API entegrasyonu kullanılarak geliştirilmiştir. API uç noktaları Pydantic şemaları ile doğrulanmakta ve SQLAlchemy ORM ile veritabanına yansıtılmaktadır.
*   **Frontend (İstemci Katmanı):** Kullanıcı arayüzü ve reaktif durum yönetimi **Vue.js** (Nuxt 3 framework'ü) kullanılarak oluşturulmuştur. Durum yönetimi için **Pinia**, form doğrulamaları için **Vee-Validate & Yup** ve sosyal oturum açma (Google/Facebook OAuth2) entegrasyonları için **Firebase SDK** tercih edilmiştir.
*   **Asenkron İşlemler:** Sipariş ve ödeme sonrası fatura oluşturma, bildirim gönderme ve e-posta kuyruk yönetimi gibi arkaplan işlemleri için **RabbitMQ** (AMQP protokolü, `pika` kütüphanesi) kullanılmıştır.
*   **Veritabanı:** Taşınabilir, ilişkisel bütünlüğe sahip ve yüksek performanslı **SQLite** veritabanı kullanılmıştır.

---

## ✨ Temel Özellikler (Features)

1.  **Kimlik Doğrulama & Yetkilendirme (Auth):**
    *   E-posta ve şifreli güvenli giriş (`bcrypt` tuzlanmış hash altyapısı).
    *   Firebase SDK tabanlı Google ve Facebook OAuth2 sosyal oturum entegrasyonu.
    *   Rol Tabanlı Erişim Kontrolü (RBAC) ile normal kullanıcı ve Admin sayfalarının ayrılması.
2.  **Katalog & Ürün Yönetimi:**
    *   Kategori bazlı filtreleme, arama ve detaylı ürün listeleme.
    *   İlişkisel bütünlüğü korumak amacıyla ürün kaldırma işlemlerinde soft-delete (`is_active = False`) mekanizması.
3.  **Sepet & Sipariş İşlemleri:**
    *   Gerçek zamanlı stok kontrolü (stok sınırını aşan sepet eklemelerinin engellenmesi).
    *   Sipariş esnasında stokların rezerve edilmesi ve sepetin boşaltılması.
    *   Ödeme iptallerinde veya Admin tarafından sipariş reddinde rezerve edilen stokların otomatik iade edilmesi.
4.  **Ödeme Entegrasyonları:**
    *   **Çevrimiçi Ödeme:** Stripe API Sandbox kart doğrulama ve anlık ödeme provizyonu.
    *   **Çevrimdışı Ödeme (Havale/EFT):** Banka transferi bildirimleri. Siparişler Admin onayına düşer ve onaylandığında durumları güncellenir.
5.  **Yorum & Değerlendirme Sistemi:**
    *   Ürünlere 1-5 arası yıldızlı puan ve yorum bırakabilme.
    *   Güvenlik ve kalite standartları gereği yorumlar varsayılan olarak onay bekler (`is_approved = False`). Admin onayından sonra storefront'ta listelenir ve ürünün ortalama puanını reaktif günceller.
6.  **Geri Bildirim Kutusu (Feedback):**
    *   Kullanıcıların öneri, şikayet ve bilgi talebi gönderebilmesi.
    *   Geri bildirimlerin Admin panelinde listelenmesi ve okunmuş olarak işaretlenebilmesi.

---

## 📐 Sistem Mimarisi ve UML Diyagramları

### 1. Genel Bileşen Mimarisi (3-Tier Architecture)

Uygulamanın mantıksal katmanları ve veri akışları aşağıdaki gibidir:

```mermaid
graph TD
    subgraph Frontend [Frontend - Vue.js / Nuxt 3]
        UI[Kullanıcı Arayüzü - Bileşenler]
        Pinia[Pinia Sepet & Auth Store]
        FirebaseSDK[Firebase Auth SDK]
    end

    subgraph Backend [Backend - Python / Django / FastAPI]
        API[REST API Routers & Controllers]
        SQLA[SQLAlchemy ORM]
        QueuePub[Queue Publisher Service]
    end

    subgraph Broker [Mesaj Kuyruğu]
        RMQ[RabbitMQ Broker Server]
    end

    subgraph Workers [Asenkron Süreçler]
        Consumer[Queue Consumer Worker Process]
    end

    subgraph DB [Veri Katmanı]
        SQLite[(SQLite Database)]
    end

    subgraph External [Dış Servisler]
        Stripe[Stripe API Sandbox]
        FBAuth[Google/FB Auth]
    end

    UI --> Pinia
    Pinia --> API
    FirebaseSDK --> FBAuth
    API --> SQLA
    SQLA --> SQLite
    API --> QueuePub
    QueuePub --> RMQ
    RMQ --> Consumer
    API --> Stripe
```

### 2. Sipariş ve Ödeme Akış Şeması (Sequence Diagram)

```mermaid
sequenceDiagram
    autonumber
    actor User as Tarayıcı (Müşteri)
    participant FE as Frontend (Vue/Nuxt)
    participant BE as Backend (Python)
    participant DB as Veritabanı (SQLite)
    participant Stripe as Stripe Gateway
    participant MQ as RabbitMQ
    participant Worker as Consumer Worker

    User->>FE: "Siparişi Tamamla" butonuna tıklar
    FE->>BE: POST /orders/ (user_id, items)
    Note over BE: Stok kontrolleri yapılır
    BE->>DB: Ürün Stoklarını Sorgula
    DB-->>BE: Stok Yeterli
    BE->>DB: Sipariş Oluştur (status: pending)
    BE->>DB: Stokları Düş (stock = stock - miktar)
    BE->>DB: Kullanıcı Sepetini Boşalt
    BE-->>FE: Sipariş ID ve Detaylarını Döner
    FE->>BE: POST /payments/online (order_id, token)
    BE->>Stripe: stripe.Charge.create(miktar, token)
    alt Stripe Başarılı
        Stripe-->>BE: Onaylandı (charge_id)
        BE->>DB: Sipariş Durumunu "confirmed" yap
        BE->>MQ: "payment_processed" olayı yayınla
        BE-->>FE: Başarılı Yanıtı Dön
        FE->>User: Sipariş Başarılı Toast Bildirimi & Profil Yönlendirmesi
    else Stripe Başarısız / Kart Hatası
        Stripe-->>BE: Kart Reddedildi / Limit Yetersiz
        BE->>DB: Sipariş Durumunu "cancelled" yap
        BE->>DB: Ürün Stoklarını Geri Yükle (stock = stock + miktar)
        BE->>MQ: "payment_failed" olayı yayınla
        BE-->>FE: Hata Kodu Dön (402)
        FE->>User: Ödeme Başarısız Uyarısı Göster
    end

    opt Kuyruk Tüketici Süreci (Async Worker)
        MQ->>Worker: Olayı Al ve Tüket
        Worker->>Worker: Fatura Oluştur / Log Kaydı Yaz
        Worker->>MQ: Acknowledge (ACK) Mesajı Gönder
    end
```

---

## 🗄️ Veritabanı Modeli (ERD)

Sistem ilişkisel veri bütünlüğünü 7 tablo üzerinden sağlar. Cascading kuralları veritabanı seviyesinde aktiftir:

```mermaid
erDiagram
    users ||--o{ cart_items : "sepetinde tutar"
    users ||--o{ orders : "sipariş verir"
    users ||--o{ comments : "yorum yapar"
    users ||--o{ feedbacks : "geri bildirim gönderir"
    products ||--o{ cart_items : "sepete eklenir"
    products ||--o{ order_items : "sipariş edilir"
    products ||--o{ comments : "yorumlanır"
    orders ||--o{ order_items : "sipariş satırlarını içerir"

    users {
        int id PK
        string name "Ad"
        string surname "Soyad"
        string email UK "E-posta"
        string password_hash "Şifre Hash"
        string phone "Telefon"
        string gender "Cinsiyet"
        string birth_date "Doğum Tarihi"
        boolean is_admin "Yönetici Yetkisi"
        datetime created_at "Kayıt Tarihi"
    }

    products {
        int id PK
        string name "Ürün Adı"
        float price "Satış Fiyatı"
        float original_price "İndirimsiz Fiyat"
        string image_url "Ürün Görseli URL"
        string description "Ürün Açıklaması"
        string category "Kategori"
        int stock "Stok Miktarı"
        boolean is_active "Aktif mi (Soft-Delete)"
        datetime created_at "Eklenme Tarihi"
    }

    cart_items {
        int id PK
        int user_id FK "users.id"
        int product_id FK "products.id"
        int quantity "Miktar"
        datetime added_at "Ekleme Zamanı"
    }

    orders {
        int id PK
        int user_id FK "users.id"
        float total "Toplam Tutar"
        string status "Sipariş Durumu (pending, confirmed, shipped, delivered, cancelled)"
        string payment_method "Ödeme Tipi (online, offline)"
        string payment_status "Ödeme Durumu (pending, approved, rejected)"
        datetime created_at "Sipariş Zamanı"
    }

    order_items {
        int id PK
        int order_id FK "orders.id"
        int product_id FK "products.id"
        int quantity "Miktar"
        float unit_price "Birim Fiyat"
    }

    comments {
        int id PK
        int product_id FK "products.id"
        int user_id FK "users.id"
        int rating "Yıldız Puanı (1-5)"
        string content "Yorum İçeriği"
        boolean is_approved "Onay Durumu"
        datetime created_at "Yazılma Zamanı"
    }

    feedbacks {
        int id PK
        int user_id FK "users.id"
        string type "Geri Bildirim Tipi (sikayet, oneri, siparis, bilgi)"
        string message "Geri Bildirim Mesajı"
        boolean is_read "Okundu Bilgisi"
        datetime created_at "Gönderilme Zamanı"
    }
```

---

## 📁 Proje Dizin Yapısı

```text
Espressolab_Final_Project/
│
├── Backend/                      # Python API & Sunucu Katmanı
│   ├── main.py                   # API Giriş Noktası & Sunucu Başlatma
│   ├── database.py               # SQLAlchemy Bağlantısı & Session Yapılandırması
│   ├── models.py                 # Veritabanı Modelleri
│   ├── schemas.py                # Pydantic Şemaları
│   ├── queue_service.py          # RabbitMQ Producer (Yayıncı)
│   ├── queue_consumer.py         # RabbitMQ Consumer (Arka Plan Worker)
│   ├── seed_data.py              # Mock Veri Ekleme Scripti
│   ├── routers/                  # API Endpoint Modülleri (auth, orders, cart vb.)
│   └── tests/                    # Pytest Entegrasyon Testleri
│
└── Frontend/                     # Vue.js / Nuxt 3 İstemci Katmanı
    ├── app.vue                   # Kök Vue Bileşeni & Global CSS
    ├── nuxt.config.ts            # Nuxt Modül ve Eklenti Konfigürasyonu
    ├── components/               # Atomik Tasarıma Göre Ayrılmış Bileşenler (atoms, molecules, organisms)
    ├── pages/                    # Dosya Tabanlı Sayfalar ve Yönlendirmeler
    ├── stores/                   # Pinia Global State Yönetimi (auth, cart, products)
    └── utils/                    # Dil Paketleri (TR/EN i18n Sözlükleri)
```

---

## ⚙️ Kurulum ve Çalıştırma Kılavuzu

Uygulamayı yerel ortamda çalıştırmak için aşağıdaki adımları sırasıyla uygulayınız:

### 1. Backend Kurulumu ve Başlatılması

1.  **Gerekli dizine geçiş yapın:**
    ```bash
    cd Backend
    ```
2.  **Sanal ortam (virtualenv) oluşturun ve aktifleştirin:**
    ```bash
    python -m venv .venv
    # Windows için:
    .\.venv\Scripts\activate
    # Linux / macOS için:
    source .venv/bin/activate
    ```
3.  **Gerekli kütüphaneleri yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Veritabanını oluşturun ve varsayılan verileri yükleyin (Seeding):**
    ```bash
    python seed_data.py
    ```
5.  **FastAPI Sunucusunu başlatın:**
    ```bash
    python -m uvicorn main:app --reload
    ```
    *API Swagger dokümantasyonuna [http://localhost:8000/docs](http://localhost:8000/docs) adresinden erişebilirsiniz.*
6.  **Asenkron RabbitMQ İşleyicisini (Worker) başlatın:**
    *(RabbitMQ servisinin yerel makinenizde çalıştığından emin olunuz)*
    ```bash
    python queue_consumer.py
    ```

### 2. Frontend Kurulumu ve Başlatılması

1.  **Gerekli dizine geçiş yapın:**
    ```bash
    cd ../Frontend
    ```
2.  **Bağımlılıkları (NPM Paketleri) yükleyin:**
    ```bash
    npm install
    ```
3.  **Geliştirici Sunucusunu (Development Server) başlatın:**
    ```bash
    npm run dev
    ```
    *Kullanıcı arayüzüne tarayıcınızdan [http://localhost:3000](http://localhost:3000) adresinden erişebilirsiniz.*

---

## 🧪 Testlerin Çalıştırılması

Sistem kararlılığını test etmek için geliştirilen birim ve entegrasyon testlerini çalıştırmak için:

*   **Backend Testleri (Pytest):**
    ```bash
    cd Backend
    pytest
    ```
*   **Frontend Testleri (Vitest):**
    ```bash
    cd Frontend
    npm run test
    ```

---

## 📸 Arayüz Ekran Görüntüleri (UI Showcase)

Aşağıda uygulamanın modern, koyu temalı (dark brand) tasarımını gösteren üretim ortamı ekran görüntüleri yer almaktadır:

### 1. Mağaza Arayüzü (Storefront Grid)
![Storefront](./screenshot_1.png)

### 2. Ürün Detay & Yorum Alanı
![Product Details](./screenshot_2.png)
![Reviews Form](./screenshot_3.png)

### 3. Yönetici Kontrol Paneli (Admin Dashboard)
![Admin Panel](./screenshot_4.png)
