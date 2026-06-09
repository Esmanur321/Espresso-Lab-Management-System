/**
 * ============================================
 * TypeScript Veri Tipleri (Interfaces)
 * ============================================
 * 
 * Bu dosya, projede kullanılan tüm veri yapılarını tanımlar.
 * TypeScript'in "interface" özelliği sayesinde:
 * - Kod yazarken otomatik tamamlama (IntelliSense) çalışır
 * - Yanlış veri tipi kullanıldığında derleme hatası verir
 * - Kodun okunabilirliği ve bakımı kolaylaşır
 * 
 * Proje Gereksinimi: "En az 4 adet TypeScript veri tipi tanımlanmalı"
 * Bu dosyada 4 adet interface tanımlanmıştır: IProduct, ICartItem, IUser, IAddress
 */

/**
 * IProduct - Ürün Veri Yapısı
 * 
 * Online mağazada satılan her ürünün sahip olduğu özellikleri tanımlar.
 * Firestore 'products' koleksiyonundaki dokümanlar bu yapıya uyar.
 */
export interface IProduct {
  id: string;              // Firestore doküman ID'si (benzersiz tanımlayıcı)
  name: string;            // Ürün adı (örn: "Kırmızı Termos 500ml")
  price: number;           // Satış fiyatı (TL cinsinden, örn: 599.99)
  originalPrice?: number;  // İndirimden önceki fiyat (opsiyonel, ? işareti)
  imageUrl: string;        // Ürün görseli URL'i
  description?: string;    // Ürün açıklaması (opsiyonel)
  categoryId?: string;     // Ait olduğu kategori ID'si (opsiyonel)
}

/**
 * ICartItem - Sepet Ürünü Veri Yapısı
 * 
 * IProduct'ı genişletir (extends) ve "quantity" (adet) özelliğini ekler.
 * Bu sayede sepetteki her ürün, hem ürün bilgilerini hem de kaç adet olduğunu tutar.
 * 
 * "extends" kullanımı: Kalıtım (inheritance) ile kod tekrarı önlenir.
 */
export interface ICartItem extends IProduct {
  quantity: number;  // Sepetteki adet sayısı (örn: 2 adet termos)
}

/**
 * IUser - Kullanıcı Veri Yapısı
 * 
 * Sisteme kayıt olan veya giriş yapan kullanıcının bilgilerini tutar.
 * Firebase Authentication ile oluşturulan kullanıcının ek bilgileri
 * Firestore 'users' koleksiyonunda bu yapıda saklanır.
 */
export interface IUser {
  uid: string;             // Firebase Authentication tarafından verilen benzersiz ID
  name: string;            // Kullanıcının adı
  surname: string;         // Kullanıcının soyadı
  email: string;           // E-posta adresi
  phone?: string;          // Telefon numarası (opsiyonel)
  birthDate?: string;      // Doğum tarihi (opsiyonel, "YYYY-MM-DD" formatında)
  role?: 'user' | 'admin'; // Kullanıcı rolü (opsiyonel, varsayılan: user)
}

/**
 * IAddress - Adres Veri Yapısı
 * 
 * Kullanıcının kayıtlı teslimat adreslerini tanımlar.
 * Profil sayfasındaki "Adreslerim" bölümünde kullanılır.
 */
export interface IAddress {
  id: string;          // Adres ID'si (benzersiz)
  title: string;       // Adres başlığı (örn: "Ev", "İş")
  fullAddress: string; // Tam adres metni
  city: string;        // Şehir
  district: string;    // İlçe
  phone: string;       // Bu adres için iletişim numarası
}
