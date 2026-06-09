<script setup lang="ts">
import FooterLinkList from '@/components/molecules/FooterLinkList.vue';
import ContactInfo from '@/components/molecules/ContactInfo.vue';
import FooterLogoSocials from '@/components/molecules/FooterLogoSocials.vue';

interface FooterLink {
  text: string;
  href: string;
}

interface ContactInfoType {
  address: string;
  phone: string;
  email: string;
}

interface SocialLink {
  platform: string;
  url: string;
  icon?: string;
}

const props = withDefaults(defineProps<{
  helpLinks?: FooterLink[];
  categoryLinks?: FooterLink[];
  contactInfo?: ContactInfoType;
  socialLinks?: SocialLink[];
  copyrightText?: string;
}>(), {
  helpLinks: () => [],
  categoryLinks: () => [],
  contactInfo: () => ({ address: '', phone: '', email: '' }),
  socialLinks: () => [],
  copyrightText: ''
});
</script>

<template>
  <footer class="the-footer">
    <div class="footer-container">
      
      <div class="footer-top">
        <FooterLogoSocials :socials="socialLinks" />
      </div>

      <hr class="divider" />

      <div class="footer-middle">
        <div class="col">
          <FooterLinkList :title="$t('footer.help')" :links="helpLinks" />
        </div>
        <div class="col">
          <FooterLinkList :title="$t('footer.categories')" :links="categoryLinks" />
        </div>
        <div class="col contact-col">
          <ContactInfo 
            :address="contactInfo.address" 
            :phone="contactInfo.phone" 
            :email="contactInfo.email"
          />
        </div>
      </div>

      <hr class="divider" />

      <div class="footer-bottom">
        <p class="copyright">{{ copyrightText }}</p>
      </div>

    </div>
  </footer>
</template>

<style scoped>
/* --- GÜNCELLEME: Footer Dark/Light Mode Uyumu --- */
.the-footer {
  /* Arka plan ve metin rengini tema değişkenlerinden alıyoruz. Yoksa varsayılan atanır. */
  background-color: var(--bg-color, #F2F2F2);
  color: var(--text-color, #333);
  padding: 50px 0 20px 0;
  font-family: 'Inter', sans-serif;
  width: 100%;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.footer-top { margin-bottom: 30px; }

.divider { border: 0; height: 1px; background-color: var(--text-color, #E0E0E0); opacity: 0.2; margin: 0; }

/* --- SÜTUN AYARLARI --- */
.footer-middle {
  display: grid;
  /* Sütun genişlikleri */
  grid-template-columns: 150px 150px 1fr; 
  /* GÜNCELLEME: Sütunlar arası boşluk azaltıldı (40px -> 20px) */
  gap: 20px; 
  padding: 30px 0;
}

/* BAŞLIKLAR */
:deep(.list-title) {
  /* GÜNCELLEME: Yazı boyutu küçültüldü */
  font-size: 12px; 
  font-weight: 700;
  color: var(--text-color, #222);
  margin-bottom: 12px;
  display: block;
}

/* LİNKLER */
:deep(.footer-link) {
  /* GÜNCELLEME: Yazı boyutu küçültüldü */
  font-size: 11px; 
  color: var(--text-color, #555);
  opacity: 0.8;
  line-height: 2; /* Satır aralığı */
  text-decoration: none;
}
:deep(.footer-link:hover) { opacity: 1; color: var(--text-color, #000); }

/* İLETİŞİM */
.contact-col {
  display: flex;
  justify-content: flex-end;
}

:deep(.contact-info) {
  text-align: left;
  max-width: 300px;
  /* GÜNCELLEME: İletişim yazı boyutu küçültüldü */
  font-size: 11px; 
  color: var(--text-color, #555);
  opacity: 0.9;
  line-height: 1.5;
}
:deep(.contact-line) {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 12px;
}

.footer-bottom {
  padding-top: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.copyright {
  font-size: 10px; /* Telif yazısı küçültüldü */
  color: #888;
  text-transform: uppercase;
}

.payment-img { height: 20px; }

@media (max-width: 768px) {
  .footer-middle { grid-template-columns: 1fr; gap: 20px; }
  .contact-col { justify-content: flex-start; }
  .footer-bottom { flex-direction: column; align-items: flex-start; }
}
</style>