<script setup lang="ts">
import { ref } from 'vue';
import { collection, addDoc, getDocs, deleteDoc, writeBatch, doc, setDoc } from 'firebase/firestore';

const { $db } = useNuxtApp();
const loading = ref(false);
const status = ref('');
const error = ref('');

// Sample Data
// Consolidated Data from Project
const categories = [
  { title: 'Kahve', image: '/images/KatKahve.png' },
  { title: 'Termos', image: '/images/kategori-termos.png' },
  { title: 'Aksesuar', image: '/images/kategori-aksesuar.png' },
  { title: 'Çaylar', image: '/images/kategori-cay.png' },
  { title: 'Atıştırmalıklar', image: '/images/kategori-atistirmalik.png' }
];

const products = [
  // --- OFİS / KLASİK ÜRÜNLER (ESKİLER) ---
  { 
    name: 'Kırmızı Pipetli Mug Termos 500 ml', 
    price: 599.99, 
    imageUrl: '/images/kirmizi-termos.jpg',
    category: 'Termos',
    description: 'Hacim: 500 ml | Malzeme: Paslanmaz Çelik | Renk: Kırmızı | Özellik: Sızdırmaz Kapak, Çift Katmanlı Yalıtım'
  },
  { 
    name: 'Pratik Filtre Kahve - Colombia', 
    price: 195.00, 
    imageUrl: '/images/filtre-kahve.jpg',
    category: 'Kahve',
    description: 'Menşei: Kolombiya | Tür: %100 Arabica | Kavrum: Orta (Medium) | Nota: Fındık, Karamel'
  },

  // --- SCRAPED DATA (YENİ ÜRÜNLER) ---
  { 
    name: 'Yılbaşı Kutusu', 
    price: 899.99, 
    imageUrl: 'https://obs-espressolab.obs.tr-west-1.myhuaweicloud.com/tr/products/img/52b26a5e-d76b-433d-822d-12ddf0b3ce4a/large_portrait_6_1258x1280_20251216111704134.png', 
    category: 'Aksesuar',
    description: 'İçerik: Kahve (250g), Kupa, Yılbaşı Çikolatası | Konsept: Yeni Yıl Özel | Ambalaj: Özel Hediye Kutusu'
  },
  { 
    name: 'Christmas Roast Costa Rica Volcan Azul 250 g', 
    price: 450.00, 
    imageUrl: 'https://obs-espressolab.obs.tr-west-1.myhuaweicloud.com/tr/products/img/ac72af82-22ff-4dea-bde5-130a722768fa/large_portrait_3_1258x1280_20251216175829955.png', 
    category: 'Kahve',
    description: 'Bölge: Costa Rica (Volcan Azul) | Tadım Notları: Tarçın, Çikolata, Narenciye | İşlem: Yıkanmış | Rakım: 1500m+'
  },
  { 
    name: 'Beyaz Metal Kupa 360 ml No:90', 
    price: 320.00, 
    imageUrl: 'https://obs-espressolab.obs.tr-west-1.myhuaweicloud.com/tr/products/img/a4e1c4ec-5fa3-49e0-9f3b-e76798deabc2/large_landscape_10_1280x1011_20251014083652335.png', 
    category: 'Aksesuar',
    description: 'Hacim: 360 ml | Materyal: Emaye Kaplama Metal | Renk: Beyaz | Kullanım: Sıcak/Soğuk | Bulaşık Makinesi: Hayır'
  },
  { 
    name: 'Siyah Metal Kupa 360 ml No:91', 
    price: 320.00, 
    imageUrl: 'https://obs-espressolab.obs.tr-west-1.myhuaweicloud.com/tr/products/img/0fc9fd85-b7f9-4bf8-9ad0-95e22c42c4c9/large_landscape_13_1280x1011_20251014083855634.png', 
    category: 'Aksesuar',
    description: 'Hacim: 360 ml | Materyal: Emaye Kaplama Metal | Renk: Siyah Mat | Kullanım: Kamp, Ofis, Ev'
  },
  { 
    name: 'Kırmızı Mat Dokulu Termos 450 ml No:92', 
    price: 650.00, 
    imageUrl: 'https://obs-espressolab.obs.tr-west-1.myhuaweicloud.com/tr/products/img/e94c55cd-faef-4ce0-befe-2b3ba72eaa1f/large_landscape_27_1280x1011_20251014084140086.png', 
    category: 'Termos',
    description: 'Hacim: 450 ml | Yalıtım: Çift Duvarlı Vakum (6 Saat Sıcak/Soğuk) | Doku: Kaydırmaz Mat | Renk: Kırmızı'
  },
  { 
    name: 'Siyah Mat Dokulu Termos 450 ml No:93', 
    price: 650.00, 
    imageUrl: 'https://obs-espressolab.obs.tr-west-1.myhuaweicloud.com/tr/products/img/4c667e3f-1e1e-4a02-a0de-ca340651a368/large_landscape_25_1280x1011_20251014084434340.png', 
    category: 'Termos',
    description: 'Hacim: 450 ml | Yalıtım: Çift Duvarlı Vakum | Materyal: 304 Paslanmaz Çelik | Özellik: Sızdırmaz Kapak'
  },
  { 
    name: 'Açık Yeşil Stoneware Espresso Bardağı No:107', 
    price: 180.00, 
    imageUrl: 'https://obs-espressolab.obs.tr-west-1.myhuaweicloud.com/tr/products/img/a9d32851-19a2-4c29-9260-557fe3bd3a17/large_portrait_9_1258x1280_20251128072008976.png', 
    category: 'Aksesuar',
    description: 'Tip: Espresso Bardağı | Materyal: Stoneware (Seramik) | Renk: Açık Yeşil | Doku: Doğal Taş Hissi'
  },
  { 
    name: 'Mavi Stoneware Espresso Bardağı No:108', 
    price: 180.00, 
    imageUrl: 'https://obs-espressolab.obs.tr-west-1.myhuaweicloud.com/tr/products/img/9018bdcb-f64d-47fb-83f4-2ec66981b0d6/large_portrait_2_1258x1280_20251128072332114.png', 
    category: 'Aksesuar',
    description: 'Tip: Espresso Bardağı | Materyal: Stoneware (Seramik) | Renk: Deniz Mavisi | Temizlik: Bulaşık Makinesinde Yıkanabilir'
  },
  { 
    name: 'Kırmızı Stoneware Espresso Bardağı No:109', 
    price: 180.00, 
    imageUrl: 'https://obs-espressolab.obs.tr-west-1.myhuaweicloud.com/tr/products/img/61e589ff-2208-4890-8342-bdb0bdb35613/large_portrait_7_1258x1280_20251128072653522.png', 
    category: 'Aksesuar',
    description: 'Tip: Espresso Bardağı | Materyal: Stoneware (Seramik) | Renk: Canlı Kırmızı | Menşei: Yerli Üretim'
  },
  { 
    name: 'Siyah Stoneware Espresso Bardağı No:110', 
    price: 180.00, 
    imageUrl: 'https://obs-espressolab.obs.tr-west-1.myhuaweicloud.com/tr/products/img/ec96204f-2b70-46ee-bfda-5c99862a4f1b/large_portrait_5_1258x1280_20251128073436495.png', 
    category: 'Aksesuar',
    description: 'Tip: Espresso Bardağı | Materyal: Stoneware (Seramik) | Renk: Mat Siyah | Stil: Modern & Minimalist'
  },
  { 
    name: 'Honey Bear Latte Pin No:10', 
    price: 120.00, 
    imageUrl: 'https://obs-espressolab.obs.tr-west-1.myhuaweicloud.com/tr/products/img/8a7d3e32-263a-4cd3-b429-4dbd98c9d526/large_landscape_Honey_1280x1258_20251202180118388.png', 
    category: 'Aksesuar',
    description: 'Tip: Rozet (Pin) | Materyal: Emaye Kaplama Metal | Figür: Honey Bear Latte | Bağlantı: İğneli Klips'
  },

  // --- YENİ EKLENEN ÜRÜNLER ---
  { 
    name: 'Yeşil Şişe Termos 550 ml No:65', 
    price: 550.00, 
    imageUrl: 'C:/Users/anutk/.gemini/antigravity/brain/06636b71-f1b5-4c9e-8db3-ff7b78fad42c/yesil_termos_550ml_1766329550821.png', 
    category: 'Termos',
    description: 'Hacim: 550 ml | Tip: Şişe Termos | Renk: Yeşil | Özellik: İnce Gövde, Sızdırmaz Kapak'
  },
  { 
    name: 'Mavi Şişe Termos 550 ml No:68', 
    price: 550.00, 
    imageUrl: 'C:/Users/anutk/.gemini/antigravity/brain/06636b71-f1b5-4c9e-8db3-ff7b78fad42c/mavi_termos_550ml_1766329577687.png', 
    category: 'Termos',
    description: 'Hacim: 550 ml | Tip: Şişe Termos | Renk: Mavi | Materyal: 304 Paslanmaz Çelik'
  },
  { 
    name: 'Renk Geçişli Pipetli Mug Termos 500 ml No:79', 
    price: 599.00, 
    imageUrl: 'https://obs-espressolab.obs.tr-west-1.myhuaweicloud.com/migration_temp/tr/92743D99-B9AC-4CDC-9901-5F07B79446B2/img/fb38ca5d-d4e6-4154-a02b-3efb4a24d1c2/3870.png', 
    category: 'Termos',
    description: 'Hacim: 500 ml | Desen: Gradient (Renk Geçişli) | Özellik: Pipetli Kapak | Yalıtım: Çift Duvarlı'
  }
];


const seedDatabase = async () => {
  if (!$db) {
    error.value = 'Database connection not found. Check firebase config.';
    return;
  }
  
  loading.value = true;
  status.value = 'Seeding started...';
  error.value = '';

  try {
    // 1. Önce eski ürünleri bul ve sil (Temiz başlangıç)
    status.value = 'Cleaning existing products...';
    const productsSnapshot = await getDocs(collection($db, 'products'));
    const deletePromises = productsSnapshot.docs.map(doc => deleteDoc(doc.ref));
    await Promise.all(deletePromises);
    console.log(`🗑️ Deleted ${productsSnapshot.size} existing products.`);

    // 2. Yeni ürünleri ekle
    status.value = `Adding ${products.length} new products with descriptions...`;
    for (const prod of products) {
      await addDoc(collection($db, 'products'), prod);
    }

    status.value = 'Database Seeded Successfully! Products added. Cart will be saved per user.';
    
  } catch (e) {
    console.error(e);
    error.value = 'Error seeding database: ' + (e as Error).message;
  } finally {
    loading.value = false;
  }
};

const cleanDatabase = async () => {
  if (!$db) {
    error.value = 'Database connection not found.';
    return;
  }

  if (!confirm('Kampanya ve Kategori koleksiyonlarını silmek istediğinize emin misiniz? (Users ve Products korunacak)')) {
    return;
  }

  loading.value = true;
  status.value = 'Cleaning database...';
  error.value = '';

  try {
    // Campaigns koleksiyonunu sil
    status.value = 'Deleting Campaigns...';
    const campaignsSnapshot = await getDocs(collection($db, 'campaigns'));
    for (const doc of campaignsSnapshot.docs) {
      await deleteDoc(doc.ref);
    }

    // Categories koleksiyonunu sil
    status.value = 'Deleting Categories...';
    const categoriesSnapshot = await getDocs(collection($db, 'categories'));
    for (const doc of categoriesSnapshot.docs) {
      await deleteDoc(doc.ref);
    }

    status.value = '✅ Campaigns and Categories deleted! Users and Products are safe.';
  } catch (e) {
    console.error(e);
    error.value = 'Error cleaning database: ' + (e as Error).message;
  } finally {
    loading.value = false;
  }
};

// Favoriler için test verisi oluştur
const createFavoritesData = async () => {
  if (!$db) {
    error.value = 'Database connection not found.';
    return;
  }
  
  loading.value = true;
  status.value = 'Creating Favorites test data...';
  error.value = '';

  try {
    // Demo kullanıcı için favori oluştur (demo-uid)
    const demoUserId = 'demo-uid';
    const demoFavoriteProductIds = ['1', '2', '5']; // Örnek ürün ID'leri

    await setDoc(doc($db, 'favorites', demoUserId), {
      items: demoFavoriteProductIds,
      updatedAt: new Date().toISOString()
    });

    status.value = '✅ Favorites collection created with demo data! Check Firebase Console.';
    console.log('✅ Favorites created for demo-uid with products:', demoFavoriteProductIds);
  } catch (e) {
    console.error(e);
    error.value = 'Error creating favorites: ' + (e as Error).message;
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="seed-container">
    <h1>Database Seeder</h1>
    <p>Use this page to populate your empty Firestore database with sample data.</p>
    
    <div class="actions">
      <button @click="seedDatabase" :disabled="loading" class="seed-btn">
        {{ loading ? 'Seeding...' : 'Populate Database' }}
      </button>
      <button @click="cleanDatabase" :disabled="loading" class="clean-btn">
        {{ loading ? 'Cleaning...' : 'Clean Campaigns & Categories' }}
      </button>
      <button @click="createFavoritesData" :disabled="loading" class="fav-btn">
        {{ loading ? 'Creating...' : 'Create Favorites Test Data' }}
      </button>
    </div>

    <div v-if="status" class="status success">{{ status }}</div>
    <div v-if="error" class="status error">{{ error }}</div>
    
    <div class="back-link">
      <NuxtLink to="/">Go to Home</NuxtLink>
    </div>
  </div>
</template>

<style scoped>
.seed-container {
  max-width: 600px;
  margin: 50px auto;
  padding: 40px;
  background: #f9f9f9;
  border-radius: 10px;
  text-align: center;
  font-family: sans-serif;
}
.seed-btn {
  background-color: #c00a00;
  color: white;
  border: none;
  padding: 15px 30px;
  font-size: 1.2rem;
  border-radius: 5px;
  cursor: pointer;
  margin: 20px 0;
}
.seed-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
.status {
  padding: 15px;
  margin: 10px 0;
  border-radius: 5px;
}
.success {
  background-color: #d4edda;
  color: #155724;
}
.error {
  background-color: #f8d7da;
  color: #721c24;
}
.back-link {
  margin-top: 20px;
}
</style>
