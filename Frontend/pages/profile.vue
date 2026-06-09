<script setup lang="ts">
// WEEK 8 - Navigation Guard: Giriş yapmadan bu sayfaya erişilemez
// 'auth' middleware'i middleware/auth.ts dosyasında tanımlı
definePageMeta({
  middleware: 'auth' as any
});

import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '~/stores/auth';
import { useFavoritesStore } from '~/stores/favorites';
import { useCartStore } from '~/stores/cart';
import { useRouter } from 'vue-router';
import { useNuxtApp } from '#app';
import { useToast } from '~/composables/useToast';
import type { IProduct } from '~/types';

// --- İMPORTLAR ---
import Breadcrumbs from '@/components/molecules/Breadcrumbs.vue';
import ProfileSideNav from '@/components/organisms/ProfileSideNav.vue';
import ProductCard from '@/components/molecules/ProductCard.vue';

// Adres tipi tanımı
interface AddressData {
  id: number | null;
  title: string;
  name: string;
  phone: string;
  identity: string;
  city: string;
  district: string;
  fullAddress: string;
  isDefault: boolean;
  type?: string;
}

const store = useAuthStore();
const favoritesStore = useFavoritesStore();
const cartStore = useCartStore();
const router = useRouter();
const { $t, $api } = useNuxtApp() as any;
const { showToast } = useToast();
const activeTab = ref('gorus-bildir'); // Varsayılanı görüş bildir yaptım

// --- MODAL KONTROLLERİ ---
const showAddressModal = ref(false); 
const showDeleteModal = ref(false); 
const showLogoutModal = ref(false);
const editingAddressId = ref<number | null>(null);

// --- ADRESLER ---
const addresses = ref<AddressData[]>([]); 
const newAddressData = ref<AddressData>({
  title: '', name: '', phone: '', identity: '', city: '', district: '', fullAddress: '', isDefault: false, id: null, type: 'bireysel'
});

// --- DİĞER VERİLER ---
const userInfo = ref({ name: '', surname: '', phone: '', email: '', birthDate: '' });
const favoriteProducts = computed(() => favoritesStore.items);
const feedback = ref({ type: 'sikayet', message: '' });

// Siparişler
const orders = ref<any[]>([]);
const isOrdersLoaded = ref(false);

const fetchOrders = async () => {
  if (!store.user) return;
  try {
    const data = await $api(`http://localhost:8000/orders/user/${store.user.uid}`);
    orders.value = data;
    isOrdersLoaded.value = true;
  } catch (error) {
    console.error('Failed to fetch orders:', error);
  }
};

// Kullanıcı bilgilerini auth store'dan doldur
onMounted(async () => {
  await store.syncProfileFromServer();
  if (store.user) {
    userInfo.value = {
      name: store.user.name || '',
      surname: store.user.surname || '',
      phone: store.user.phone || '',
      email: store.user.email || '',
      birthDate: store.user.birthDate || ''
    };
  }
});

// HESAPLAMALAR
const isEditing = computed(() => editingAddressId.value !== null);
const modalTitle = computed(() => isEditing.value ? $t('profile.edit_address') : $t('profile.add_new_address'));
const modalButtonText = computed(() => isEditing.value ? $t('profile.btn_update') : $t('profile.btn_add_address'));


// --- METOTLAR ---
const closeModal = () => {
  editingAddressId.value = null;
  newAddressData.value = { title: '', name: '', phone: '', identity: '', city: '', district: '', fullAddress: '', isDefault: false, id: null, type: 'bireysel' };
  showAddressModal.value = false;
};

const startEdit = (address: AddressData) => {
  newAddressData.value = JSON.parse(JSON.stringify(address)); 
  editingAddressId.value = address.id;
  showAddressModal.value = true;
};

const addNewAddress = async () => {
  if (!newAddressData.value.title || !newAddressData.value.fullAddress) {
    await showToast($t('profile.alert_address_empty') || 'Lütfen Adres Başlığı ve Adres alanlarını doldurun.', 'warning');
    return;
  }
  if (isEditing.value) {
    const index = addresses.value.findIndex((a: AddressData) => a.id === editingAddressId.value);
    if (index !== -1) {
      addresses.value[index] = { ...newAddressData.value };
      await showToast($t('profile.alert_address_updated') || 'Adres başarıyla güncellendi!', 'success');
    }
  } else {
    addresses.value.push({ ...newAddressData.value, id: Date.now() });
    await showToast($t('profile.alert_address_added') || 'Yeni adres başarıyla kaydedildi!', 'success');
  }
  closeModal();
};

const deleteAddress = async (id: number | null) => {
  if (id === null) return;
  // Show confirmation via toast before deletion
  addresses.value = addresses.value.filter((addr: AddressData) => addr.id !== id);
  await showToast($t('profile.alert_address_deleted') || 'Adres silindi.', 'info');
};

const handleNavigation = (slug: string) => {
  if (slug === 'admin-panel') {
    router.push('/admin');
    return;
  }
  if (slug === 'cikis-yap') { showLogoutModal.value = true; } 
  else if (slug === 'hesabi-sil') { showDeleteModal.value = true; } 
  else { 
    activeTab.value = slug; 
    if (slug === 'siparislerim' && !isOrdersLoaded.value) {
      fetchOrders();
    }
  }
};
const confirmDeleteAccount = async () => { 
  try {
    const userId = store.user?.uid;
    if (!userId) {
      await showToast($t('profile.alert_user_not_found') || 'Kullanıcı bulunamadı', 'error');
      return;
    }
    console.log('Mock: User data deleted from Firestore (simulated)');
    cartStore.clearCart();
    favoritesStore.clearFavorites();
    await store.logout();
    showDeleteModal.value = false; 
    router.push('/');
    await showToast($t('profile.alert_account_deleted') || 'Hesabınız ve tüm verileriniz başarıyla silindi.', 'success');
  } catch (error) {
    console.error('Delete error:', error);
    await showToast(($t('profile.alert_delete_error') || 'Hesap silinirken bir hata oluştu: ') + ' ' + (error as Error).message, 'error');
  }
};
const confirmLogout = () => { store.logout(); showLogoutModal.value = false; router.push('/login'); };
const saveUserInfo = () => { showToast($t('profile.alert_info_updated') || 'Bilgiler Güncellendi!', 'success'); };
const sendFeedback = async () => {
  if (!store.user?.uid) return;
  if (!feedback.value.message.trim()) {
    await showToast($t('profile.alert_feedback_empty') || 'Lütfen geri bildiriminizi yazın.', 'warning');
    return;
  }
  try {
    await $api('http://localhost:8000/feedbacks/', {
      method: 'POST',
      body: {
        user_id: parseInt(store.user.uid),
        type: feedback.value.type,
        message: feedback.value.message
      }
    });
    await showToast($t('profile.alert_feedback_sent') || 'Görüşünüz iletildi!', 'success');
    feedback.value.message = '';
  } catch (error: any) {
    console.error('Failed to send feedback:', error);
    await showToast(
      ($t('profile.alert_feedback_error') || 'Geri bildirim gönderilirken hata oluştu:') + ' ' + (error?.data?.detail || error.message),
      'error'
    );
  }
};

// Ürün işlemleri
const handleAddToCart = (product: IProduct) => {
  cartStore.addToCart(product);
  showToast(`${product.name} ${$t('cart.added_to_cart')}`, 'success');
};

const goToProductDetail = (product: IProduct) => {
  router.push(`/product/${product.id}`);
};

// SABİT VERİLER
const breadcrumbLinks = computed(() => [ { text: $t('cart.breadcrumb_home'), href: '/' }, { text: $t('profile.title'), href: '/profile' } ]);
const profileNavItems = computed(() => {
  const items = [
    { label: $t('profile.my_info'), slug: 'bilgilerim' },
    { label: $t('profile.my_addresses'), slug: 'adreslerim' },
    { label: $t('profile.my_favorites'), slug: 'favorilerim' },
    { label: $t('profile.my_orders'), slug: 'siparislerim' },
    { label: $t('profile.feedback'), slug: 'gorus-bildir' }
  ];
  if (store.isAdmin) {
    items.unshift({ label: $t('admin.title'), slug: 'admin-panel' });
  }
  items.push(
    { label: $t('profile.delete_account'), slug: 'hesabi-sil' },
    { label: $t('profile.logout'), slug: 'cikis-yap' }
  );
  return items;
});
</script>

<template>
  <main class="page-content">
    <div class="content-wrapper">
      <Breadcrumbs :links="breadcrumbLinks" />
      
      <div class="profile-layout">
        <ProfileSideNav 
          :navItems="profileNavItems"
          :activeSlug="activeTab"
          @navigate="handleNavigation"
          class="sidebar-nav"
        />
        
        <section class="profile-content-area">
          
          <div v-if="activeTab === 'adreslerim'">
             <div class="content-panel">
                 <div class="panel-header">
                     <h2 class="panel-title">{{ $t('profile.my_addresses') }}</h2>
                 </div>
                 <div class="panel-body">
                     <div class="saved-addresses" v-if="addresses.length > 0">
                        <div v-for="(addr, index) in addresses" :key="addr.id ?? index" class="address-item">
                            <div class="address-text-content">
                                <span class="address-title">{{ addr.title }}</span>
                                <p class="address-detail">{{ addr.name }} / {{ addr.fullAddress }}</p>
                                <p class="address-contact">Tel: {{ addr.phone }}</p>
                            </div>
                            <div class="address-actions">
                                <button class="edit-btn" @click="startEdit(addr)">{{ $t('profile.btn_edit') }}</button>
                                <button class="delete-btn" @click="deleteAddress(addr.id)">{{ $t('profile.btn_delete') }}</button>
                            </div>
                        </div>
                     </div>
                     <div class="add-address-wrapper">
                         <button class="add-new-address-btn" @click="closeModal(); showAddressModal = true;">
                             {{ $t('profile.btn_add_address') }}
                         </button>
                     </div>
                 </div>
             </div>
          </div>

          <div v-if="activeTab === 'bilgilerim'">
            <div class="content-panel">
               <div class="panel-header">
                  <h2 class="panel-title">{{ $t('profile.my_info') }}</h2>
               </div>
               <div class="panel-body info-body">
                  <div class="info-form">
                    <div class="custom-input-group">
                      <span class="input-icon-left">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#c00000" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
                      </span>
                      <input type="text" v-model="userInfo.name" :placeholder="$t('profile.placeholder_name')" />
                    </div>
                    <div class="custom-input-group">
                      <span class="input-icon-left">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#c00000" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
                      </span>
                      <input type="text" v-model="userInfo.surname" :placeholder="$t('profile.placeholder_surname')" />
                    </div>
                    <div class="custom-input-group phone-group disabled-input">
                      <div class="phone-prefix"><span class="country-code">TR</span><span class="code-num">+90</span></div>
                      <input type="text" v-model="userInfo.phone" placeholder="555 123 45 67" class="phone-input" disabled />
                    </div>
                    <div class="custom-input-group disabled-input">
                      <span class="input-icon-left">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#999" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
                      </span>
                      <input type="email" v-model="userInfo.email" placeholder="ornek@email.com" disabled />
                    </div>
                    <div class="custom-input-group">
                      <span class="input-icon-left">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#c00000" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
                      </span>
                      <input type="date" v-model="userInfo.birthDate" />
                    </div>
                    <div class="warning-note">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="info-icon"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
                      <span>{{ $t('profile.warning_birth_date') }}</span>
                    </div>
                    <button class="update-btn-full" @click="saveUserInfo">{{ $t('profile.btn_update') }}</button>
                  </div>
               </div>
            </div>
          </div>

          <div v-if="activeTab === 'favorilerim'">
            <div class="content-panel">
              <div class="panel-header">
                <h2 class="panel-title">{{ $t('profile.my_favorites') }}</h2>
              </div>
              <div class="panel-body">
                <div v-if="favoriteProducts.length > 0" class="favorites-grid">
                  <ProductCard v-for="product in favoriteProducts" :key="product.id" :product="product" @addToCart="handleAddToCart" @view="goToProductDetail"/>
                </div>
                <div v-else class="empty-favorites">
                  <p class="empty-favorites-text">{{ $t('profile.empty_favorites') }}</p>
                </div>
              </div>
            </div>
          </div>

          <div v-if="activeTab === 'siparislerim'">
            <div class="content-panel">
               <div class="panel-header">
                  <h2 class="panel-title">{{ $t('profile.my_orders') }}</h2>
               </div>
               <div class="panel-body">
                 <div v-if="orders.length > 0" class="orders-list">
                    <div v-for="order in orders" :key="order.id" class="order-card">
                       <div class="order-header">
                          <span class="order-id">{{ $t('profile.order_id') }}: #{{ order.id }}</span>
                          <span class="order-date">{{ new Date(order.created_at).toLocaleDateString() }}</span>
                       </div>
                       <div class="order-details">
                          <p class="order-total">{{ $t('profile.order_total') }}: <strong>₺{{ order.total.toFixed(2) }}</strong></p>
                          <p class="order-status">
                            {{ $t('profile.order_status') }}: 
                            <span :class="['status-badge', order.status]">
                              {{ $t(`profile.status_${order.status}`) || order.status }}
                            </span>
                          </p>
                       </div>
                       <div class="order-items-list">
                         <div v-for="item in order.items" :key="item.id" class="ordered-product">
                           <div class="ordered-product-img-wrapper">
                             <img :src="item.product?.image_url || '/images/products/placeholder.png'" :alt="item.product?.name" class="ordered-product-img" />
                           </div>
                           <div class="ordered-product-info">
                             <span class="ordered-product-name">{{ $t(item.product?.name || 'Ürün') }}</span>
                             <span class="ordered-product-qty">{{ item.quantity }} x ₺{{ item.unit_price.toFixed(2) }}</span>
                           </div>
                           <div class="ordered-product-total">
                             <span>₺{{ (item.quantity * item.unit_price).toFixed(2) }}</span>
                           </div>
                         </div>
                       </div>
                    </div>
                 </div>
                 <div v-else class="empty-orders-panel">
                     <p class="empty-text">{{ $t('profile.empty_orders') }}</p>
                 </div>
               </div>
            </div>
          </div>

          <div v-if="activeTab === 'gorus-bildir'">
            <div class="content-panel">
               <div class="panel-header">
                  <h2 class="panel-title">{{ $t('profile.feedback') }}</h2>
               </div>
               <div class="panel-body feedback-body-redesign">
                  <div class="feedback-form-redesign">
                    
                    <div class="form-group">
                      <label class="feedback-label">{{ $t('profile.feedback_topic') }}</label>
                      <div class="radio-buttons-row">
                        <label class="radio-option">
                          <input type="radio" v-model="feedback.type" value="sikayet" name="feedback-type">
                          <span class="radio-circle"></span>
                          <span class="radio-text">{{ $t('profile.feedback_complaint') }}</span>
                        </label>
                        <label class="radio-option">
                          <input type="radio" v-model="feedback.type" value="oneri" name="feedback-type">
                          <span class="radio-circle"></span>
                          <span class="radio-text">{{ $t('profile.feedback_suggestion') }}</span>
                        </label>
                        <label class="radio-option">
                          <input type="radio" v-model="feedback.type" value="siparis" name="feedback-type">
                          <span class="radio-circle"></span>
                          <span class="radio-text">{{ $t('profile.feedback_order') }}</span>
                        </label>
                        <label class="radio-option">
                          <input type="radio" v-model="feedback.type" value="bilgi" name="feedback-type">
                          <span class="radio-circle"></span>
                          <span class="radio-text">{{ $t('profile.feedback_info') }}</span>
                        </label>
                      </div>
                    </div>

                    <div class="form-group">
                      <label class="feedback-label">{{ $t('profile.feedback_comment') }}</label>
                      <textarea 
                        v-model="feedback.message" 
                        :placeholder="$t('profile.feedback_placeholder')" 
                        class="feedback-input" 
                        maxlength="2000"
                        rows="6"
                      ></textarea>
                      <div class="char-counter">{{ feedback.message.length }}/2000</div>
                    </div>

                    <p class="feedback-bottom-text">{{ $t('profile.feedback_bottom_text') }}</p>

                    <div class="submit-button-wrapper">
                      <button class="feedback-submit-btn" @click="sendFeedback">{{ $t('profile.btn_send') }}</button>
                    </div>

                  </div>
               </div>
            </div>
          </div>

        </section>
      </div>
    </div>

    <div v-if="showDeleteModal" class="modal-overlay delete-overlay" @click.self="showDeleteModal = false">
      <div class="confirm-modal-content">
        <button class="close-btn abs-close" @click="showDeleteModal = false">×</button>
        <div class="warning-icon-wrapper"><span class="warning-icon">!</span></div>
        <h3 class="confirm-title">{{ $t('profile.modal_delete_title') }}</h3>
        <p class="confirm-desc">{{ $t('profile.modal_delete_desc') }}</p>
        <div class="confirm-actions">
          <button class="cancel-btn" @click="showDeleteModal = false">{{ $t('profile.btn_no') }}</button>
          <button class="confirm-btn" @click="confirmDeleteAccount">{{ $t('profile.btn_yes') }}</button>
        </div>
      </div>
    </div>

    <div v-if="showLogoutModal" class="modal-overlay logout-overlay" @click.self="showLogoutModal = false">
      <div class="confirm-modal-content">
        <button class="close-btn abs-close" @click="showLogoutModal = false">×</button>
        <div class="warning-icon-wrapper"><span class="warning-icon">!</span></div>
        <h3 class="confirm-title">{{ $t('profile.modal_logout_title') }}</h3>
        <p class="confirm-desc">{{ $t('profile.modal_logout_desc') }}</p>
        <div class="confirm-actions">
          <button class="cancel-btn" @click="showLogoutModal = false">{{ $t('profile.btn_no') }}</button>
          <button class="confirm-btn" @click="confirmLogout">{{ $t('profile.btn_yes') }}</button>
        </div>
      </div>
    </div>

    <div v-if="showAddressModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content address-modal">
        <div class="modal-header">
          <h3>{{ modalTitle }}</h3>
          <button class="close-btn" @click="closeModal">×</button>
        </div>
        <div class="modal-body">
          <input type="text" :placeholder="$t('profile.address_title')" class="modal-input" v-model="newAddressData.title" />
          <input type="text" :placeholder="$t('profile.address_fullname')" class="modal-input" v-model="newAddressData.name" />
          <div class="phone-input-row"><span class="prefix">+90</span><input type="text" class="modal-input" :placeholder="$t('profile.address_phone')" v-model="newAddressData.phone" /></div>
          <div class="radio-row">
            <label><input type="radio" name="fatura" v-model="newAddressData.type" value="bireysel" checked> {{ $t('profile.address_individual') }}</label>
            <label><input type="radio" name="fatura" v-model="newAddressData.type" value="kurumsal"> {{ $t('profile.address_corporate') }}</label>
          </div>
          <input type="text" :placeholder="$t('profile.address_tc')" class="modal-input" v-model="newAddressData.identity" />
          <input type="text" :placeholder="$t('profile.address_city')" class="modal-input" v-model="newAddressData.city" />
          <input type="text" :placeholder="$t('profile.address_district')" class="modal-input" v-model="newAddressData.district" />
          <textarea :placeholder="$t('profile.address_full')" class="modal-textarea" v-model="newAddressData.fullAddress"></textarea>
          <label class="checkbox-row"><input type="checkbox" v-model="newAddressData.isDefault"> {{ $t('profile.address_default') }}</label>
          <button class="modal-save-btn" @click="addNewAddress">{{ modalButtonText }}</button>
          <button v-if="isEditing" class="modal-delete-btn" @click="deleteAddress(editingAddressId); closeModal();">{{ $t('profile.btn_delete') }}</button>
        </div>
      </div>
    </div>

  </main>
</template>

<style scoped>
/* --- GENEL SAYFA DÜZENİ --- */
.page-content { background-color: #fff; padding-top: 40px; padding-bottom: 60px; }
.content-wrapper { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
.profile-layout { display: grid; grid-template-columns: 250px 1fr; gap: 30px; margin-top: 20px; }
.section-title { font-size: 1.1rem; font-weight: 700; margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 10px; color: #333; }

/* --- SIDEBAR TASARIMI --- */
:deep(.side-nav-item) {
    padding: 15px 20px;
    border-bottom: 1px solid #f0f0f0;
    color: #333;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s;
    background: #fff;
    display: block;
    width: 100%;
    text-align: left;
}
:deep(.side-nav-item:hover) { background-color: #f9f9f9; }
:deep(.side-nav-item.active) { background-color: #FFF5F5; color: #c00a00; font-weight: 700; }

/* --- ORTAK PANEL STİLİ --- */
.content-panel {
    border: 1px solid #e5e5e5;
    border-radius: 8px;
    background-color: #fff;
    min-height: 400px;
    display: flex;
    flex-direction: column;
}
.panel-header { padding: 20px 30px; border-bottom: 1px solid #e5e5e5; }
.panel-title { font-size: 16px; font-weight: 700; color: #000; margin: 0; }
.panel-body { padding: 30px; display: flex; flex-direction: column; flex-grow: 1; }

/* --- YENİ GÖRÜŞ BİLDİR TASARIMI --- */
.feedback-body-redesign {
    padding: 40px;
}

.feedback-form-redesign {
    max-width: 100%;
}

.form-group {
    margin-bottom: 30px;
}

.feedback-label {
    display: block;
    font-size: 14px;
    font-weight: 600;
    color: #000;
    margin-bottom: 15px;
}

/* Yatay yan yana radio butonlar */
.radio-buttons-row {
    display: flex;
    gap: 35px;
    align-items: center;
}

.radio-option {
    display: flex;
    align-items: center;
    cursor: pointer;
    font-size: 14px;
    color: #333;
}

.radio-option input[type="radio"] {
    display: none;
}

.radio-circle {
    width: 18px;
    height: 18px;
    border: 2px solid #ccc;
    border-radius: 50%;
    margin-right: 8px;
    position: relative;
    transition: border-color 0.2s;
}

.radio-option input[type="radio"]:checked + .radio-circle {
    border-color: #007bff;
}

.radio-option input[type="radio"]:checked + .radio-circle::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 8px;
    height: 8px;
    background-color: #007bff;
    border-radius: 50%;
}

.radio-text {
    font-size: 14px;
    color: #333;
}

/* Textarea */
.feedback-input {
    width: 100%;
    border: 1px solid #e5e5e5;
    border-radius: 8px;
    padding: 15px;
    font-size: 14px;
    font-family: inherit;
    resize: none;
    outline: none;
    box-sizing: border-box;
}

.feedback-input::placeholder {
    color: #ccc;
}

.feedback-input:focus {
    border-color: #bbb;
}

.char-counter {
    text-align: left;
    font-size: 12px;
    color: #999;
    margin-top: 8px;
}

.feedback-bottom-text {
    font-size: 12px;
    color: #666;
    text-align: center;
    margin: 20px 0;
    line-height: 1.5;
}

.submit-button-wrapper {
    display: flex;
    justify-content: center;
    margin-top: 25px;
}

.feedback-submit-btn {
    background-color: #d98686;
    color: white;
    border: none;
    padding: 12px 80px;
    border-radius: 50px;
    font-weight: 700;
    font-size: 16px;
    cursor: pointer;
    transition: background 0.3s;
}

.feedback-submit-btn:hover {
    background-color: #c00a00;
}

/* --- DİĞER MODÜLLERİN STİLLERİ (Değişmedi) --- */
.info-body { justify-content: flex-start; }
.info-form { display: flex; flex-direction: column; gap: 20px; max-width: 100%; }
.custom-input-group { display: flex; align-items: center; border: 1px solid #e5e5e5; border-radius: 6px; height: 50px; padding: 0 15px; background-color: #fff; }
.custom-input-group:focus-within { border-color: #ccc; }
.custom-input-group.disabled-input { background-color: #f5f5f5; border-color: #ddd; }
.custom-input-group.disabled-input input { color: #999; cursor: not-allowed; }
.custom-input-group input:disabled { color: #999; cursor: not-allowed; background: transparent; }
.input-icon-left { margin-right: 15px; display: flex; align-items: center; }
.custom-input-group input { border: none; outline: none; width: 100%; font-size: 15px; color: #333; background: transparent; height: 100%; }
.phone-group { padding-left: 0; }
.phone-group.disabled-input .phone-prefix { background-color: #e5e5e5; }
.phone-prefix { background-color: #F5F5F5; height: 100%; display: flex; align-items: center; padding: 0 15px; border-right: 1px solid #e5e5e5; border-top-left-radius: 6px; border-bottom-left-radius: 6px; font-weight: 600; font-size: 14px; color: #333; gap: 5px; }
.country-code { font-weight: 700; font-size: 12px; }
.code-num { font-size: 14px; }
.phone-input { padding-left: 15px; }
.warning-note { display: flex; align-items: center; gap: 8px; font-size: 13px; color: #333; margin-top: -5px; }
.info-icon { color: #000; }
.update-btn-full { background-color: #c00a00; color: #fff; border: none; border-radius: 50px; height: 50px; font-size: 16px; font-weight: 700; cursor: pointer; width: 50%; margin-top: 10px; transition: background 0.3s; }
.update-btn-full:hover { background-color: #a00000; }
.saved-addresses { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; margin-bottom: 30px; justify-content: flex-start; }
.add-address-wrapper { display: flex; justify-content: center; width: 100%; }
.add-new-address-btn { background-color: #fff; border: 1px solid #f2f2f2; color: #c00a00; font-weight: 600; padding: 14px 40px; border-radius: 50px; cursor: pointer; font-size: 14px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); transition: all 0.3s ease; min-width: 250px; }
.add-new-address-btn:hover { border-color: #c00a00; background-color: #fff5f5; }
.address-item { border: 1px solid #eee; padding: 15px; border-radius: 8px; background-color: #fcfcfc; position: relative; display: flex; justify-content: space-between; align-items: flex-start; flex-direction: column; gap: 10px; height: 100%; }
.address-title { font-weight: 700; color: #c00a00; margin-bottom: 5px; display: block;}
.address-detail { font-size: 0.9rem; color: #666; margin: 0; line-height: 1.4; }
.address-actions { display: flex; gap: 10px; margin-top: auto; }
.edit-btn, .delete-btn { background: none; border: none; color: #c00a00; font-size: 0.85rem; cursor: pointer; text-decoration: underline; padding: 0;}
.delete-btn { color: #999; }
.empty-orders-panel { min-height: 200px; padding: 30px; display: flex; align-items: center; justify-content: center; }
.empty-text { font-size: 14px; color: #555; margin: 0; }

.orders-list { display: flex; flex-direction: column; gap: 20px; }
.order-card { border: 1px solid #eee; border-radius: 8px; padding: 20px; background-color: #fcfcfc; }
.order-header { display: flex; justify-content: space-between; border-bottom: 1px solid #eee; padding-bottom: 10px; margin-bottom: 10px; font-weight: bold; }
.order-details { display: flex; justify-content: space-between; margin-bottom: 15px; }
.order-total strong { color: #c00a00; font-size: 1.1rem; }
.status-badge { padding: 4px 10px; border-radius: 50px; font-size: 0.8rem; font-weight: bold; }
.status-badge.pending { background-color: #fff3cd; color: #856404; }
.status-badge.confirmed { background-color: #d4edda; color: #155724; }
.status-badge.shipped { background-color: #cce5ff; color: #004085; }
.status-badge.delivered { background-color: #d1ecf1; color: #0c5460; }
.status-badge.cancelled { background-color: #f8d7da; color: #721c24; }
.order-items-list { display: flex; flex-direction: column; gap: 10px; margin-top: 15px; border-top: 1px solid #f0f0f0; padding-top: 15px; }
.ordered-product { display: flex; align-items: center; justify-content: space-between; background: #fff; padding: 10px 15px; border: 1px solid #f0f0f0; border-radius: 8px; transition: box-shadow 0.2s; }
.ordered-product:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.03); }
.ordered-product-img-wrapper { width: 50px; height: 50px; border-radius: 6px; overflow: hidden; background: #f9f9f9; display: flex; align-items: center; justify-content: center; border: 1px solid #eee; flex-shrink: 0; }
.ordered-product-img { width: 100%; height: 100%; object-fit: contain; padding: 4px; }
.ordered-product-info { flex-grow: 1; padding: 0 15px; display: flex; flex-direction: column; gap: 4px; }
.ordered-product-name { font-size: 0.95rem; font-weight: 600; color: #333; }
.ordered-product-qty { font-size: 0.85rem; color: #777; }
.ordered-product-total { font-weight: 700; color: #c00a00; font-size: 1rem; }

/* --- BOŞ FAVORİLER --- */
.empty-favorites {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 300px;
}

.empty-favorites-text {
  font-size: 14px;
  color: #666;
  margin: 0;
}

/* --- SİDEBAR AKTİF RENK --- */
:deep(.profile-nav-link.active) {
  background-color: #FFF5F5 !important; /* Açık pembe/kırmızı */
  color: #c00a00 !important;
}
.modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.5); z-index: 2000; display: flex; justify-content: center; align-items: center; }
.address-modal { background: white; width: 500px; max-height: 90vh; overflow-y: auto; border-radius: 12px; padding: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.close-btn { background: none; border: none; font-size: 1.5rem; cursor: pointer; color: #555; }
.modal-body { display: flex; flex-direction: column; gap: 15px; }
.modal-input, .modal-textarea, .modal-select { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box; }
.phone-input-row { display: flex; align-items: center; border: 1px solid #ddd; border-radius: 8px; padding-left: 10px; }
.phone-input-row .modal-input { border: none; }
.phone-input-row .prefix { font-weight: bold; border-right: 1px solid #ddd; padding-right: 10px; }
.radio-row { display: flex; gap: 20px; font-size: 0.9rem; }
.modal-textarea { height: 80px; resize: none; }
.modal-save-btn { background-color: #c00a00; color: white; padding: 12px; border: none; border-radius: 50px; width: 100%; font-weight: bold; cursor: pointer; margin-top: 10px; }
.modal-delete-btn { background-color: #fff; color: #c00a00; border: 1px solid #c00a00; padding: 12px; border-radius: 50px; width: 100%; font-weight: bold; cursor: pointer; margin-top: 10px; }
.confirm-modal-content { background: white; width: 400px; border-radius: 16px; padding: 30px; text-align: center; position: relative; box-shadow: 0 10px 40px rgba(0,0,0,0.2); }
.abs-close { position: absolute; top: 15px; right: 20px; font-size: 1.5rem; }
.warning-icon-wrapper { width: 50px; height: 50px; border-radius: 50%; background-color: #FEE2E2; color: #c00a00; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px auto; }
.warning-icon { font-size: 24px; font-weight: bold; }
.confirm-title { margin: 0 0 10px 0; font-size: 1.2rem; font-weight: 700; color: #111; }
.confirm-desc { color: #666; font-size: 0.; margin-bottom: 30px; }
.confirm-actions { display: flex; flex-direction: column; gap: 10px; }
.cancel-btn { background: #fff; border: 1px solid #ddd; color: #333; padding: 12px; border-radius: 50px; font-weight: 600; cursor: pointer; }
.confirm-btn { background: #c00a00; border: none; color: #fff; padding: 12px; border-radius: 50px; font-weight: 600; cursor: pointer; }
.favorites-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px; }

@media (max-width: 992px) { .profile-layout { grid-template-columns: 1fr; } .modal-content { width: 90%; } }
</style>