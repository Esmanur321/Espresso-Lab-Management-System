<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '~/stores/auth';
import { useNuxtApp } from '#app';
import { useToast } from '~/composables/useToast';

definePageMeta({
  middleware: ['auth', 'admin']
});

const store = useAuthStore();
const { $api, $t } = useNuxtApp() as any;
const { showToast } = useToast();

const API_BASE = 'http://localhost:8000';
const orderIdInput = ref('');
const pendingOrders = ref<any[]>([]);
const pendingComments = ref<any[]>([]);
const feedbacks = ref<any[]>([]);
const isPageLoading = ref(true);
const isActionLoading = ref(false);
const activeTab = ref('payments'); // 'payments', 'comments', or 'feedbacks'

const isAdmin = computed(() => store.isAdmin);

const unreadFeedbacksCount = computed(() => {
  return feedbacks.value.filter((f: any) => !f.is_read).length;
});

const fetchAdminData = async () => {
  if (!isAdmin.value || !store.user?.uid) {
    isPageLoading.value = false;
    return;
  }
  isPageLoading.value = true;
  try {
    const adminId = parseInt(store.user.uid);
    // Fetch pending orders
    pendingOrders.value = await $api(
      `${API_BASE}/payments/offline/pending`,
      { params: { admin_id: adminId } }
    );
    // Fetch pending comments
    pendingComments.value = await $api(
      `${API_BASE}/comments/pending`,
      { params: { admin_id: adminId } }
    );
    // Fetch feedbacks
    feedbacks.value = await $api(
      `${API_BASE}/feedbacks/`,
      { params: { admin_id: adminId } }
    );
  } catch (error: any) {
    console.error('Failed to load admin data:', error);
    await showToast($t('admin.load_error') || 'Yönetici verileri yüklenirken hata oluştu.', 'error');
  } finally {
    isPageLoading.value = false;
  }
};

const handleCommentApproval = async (commentId: number, approved: boolean) => {
  if (!store.user?.uid) return;

  isActionLoading.value = true;
  try {
    if (approved) {
      await $api(`${API_BASE}/comments/${commentId}/approve`, {
        method: 'PATCH',
        params: { admin_id: parseInt(store.user.uid) }
      });
      await showToast($t('admin.comment_approved') || 'Yorum onaylandı!', 'success');
    } else {
      await $api(`${API_BASE}/comments/${commentId}`, {
        method: 'DELETE',
        params: { admin_id: parseInt(store.user.uid) }
      });
      await showToast($t('admin.comment_rejected') || 'Yorum silindi!', 'success');
    }
    await fetchAdminData();
  } catch (error: any) {
    await showToast(
      ($t('admin.error') || 'İşlem başarısız:') + ' ' + (error?.data?.detail || error.message),
      'error'
    );
  } finally {
    isActionLoading.value = false;
  }
};

const handleFeedbackRead = async (feedbackId: number) => {
  if (!store.user?.uid) return;

  isActionLoading.value = true;
  try {
    await $api(`${API_BASE}/feedbacks/${feedbackId}/read`, {
      method: 'PATCH',
      params: { admin_id: parseInt(store.user.uid) }
    });
    await showToast($t('admin.feedback_marked_read') || 'Geri bildirim okundu olarak işaretlendi!', 'success');
    await fetchAdminData();
  } catch (error: any) {
    await showToast(
      ($t('admin.error') || 'İşlem başarısız:') + ' ' + (error?.data?.detail || error.message),
      'error'
    );
  } finally {
    isActionLoading.value = false;
  }
};

const formatDate = (dateStr: string) => {
  if (!dateStr) return '';
  return new Date(dateStr).toLocaleString();
};

const handleApproval = async (targetOrderId: number, approved: boolean) => {
  if (!store.user?.uid) return;

  isActionLoading.value = true;
  try {
    const response = await $api(`${API_BASE}/payments/offline/${targetOrderId}`, {
      method: 'PATCH',
      body: {
        admin_id: parseInt(store.user.uid),
        payment_status: approved ? 'approved' : 'rejected'
      }
    });

    const defaultMsg = approved
      ? ($t('admin.approved_success') || 'Ödeme onaylandı!')
      : ($t('admin.rejected_success') || 'Ödeme reddedildi!');
    await showToast(response.message || defaultMsg, 'success');

    if (parseInt(orderIdInput.value) === targetOrderId) {
      orderIdInput.value = '';
    }

    await fetchAdminData();
  } catch (error: any) {
    await showToast(
      ($t('admin.error') || 'İşlem başarısız:') + ' ' + (error?.data?.detail || error.message),
      'error'
    );
  } finally {
    isActionLoading.value = false;
  }
};

const handleManualSubmit = (approved: boolean) => {
  if (!orderIdInput.value) {
    showToast($t('admin.error_empty') || 'Lütfen bir Sipariş ID girin.', 'warning');
    return;
  }
  handleApproval(parseInt(orderIdInput.value), approved);
};

onMounted(() => {
  fetchAdminData();
});
</script>

<template>
  <main class="page-content">
    <div class="content-container">

      <div v-if="!isPageLoading && !isAdmin" class="unauthorized-card">
        <span class="lock-icon">🔒</span>
        <h2>{{ $t('admin.unauthorized_title') }}</h2>
        <p>{{ $t('admin.unauthorized_desc') }}</p>
        <router-link to="/" class="home-btn">{{ $t('admin.back_home') }}</router-link>
      </div>

      <div v-else-if="isPageLoading" class="loading-container">
        <div class="spinner"></div>
        <p>{{ $t('admin.loading') }}</p>
      </div>

      <div v-else>
        <h1 class="page-title">{{ $t('admin.title') }}</h1>
        <p class="desc">{{ $t('admin.subtitle') }}</p>

        <!-- Admin Tabs -->
        <div class="admin-tabs">
          <button 
            :class="['tab-btn', { active: activeTab === 'payments' }]" 
            @click="activeTab = 'payments'"
          >
            💳 {{ $t('admin.offline_payments') || 'Çevrimdışı Ödemeler' }} ({{ pendingOrders.length }})
          </button>
          <button 
            :class="['tab-btn', { active: activeTab === 'comments' }]" 
            @click="activeTab = 'comments'"
          >
            💬 {{ $t('admin.pending_comments') || 'Onay Bekleyen Yorumlar' }} ({{ pendingComments.length }})
          </button>
          <button 
            :class="['tab-btn', { active: activeTab === 'feedbacks' }]" 
            @click="activeTab = 'feedbacks'"
          >
            ✉️ {{ $t('admin.user_feedbacks') || 'Kullanıcı Geri Bildirimleri' }} ({{ unreadFeedbacksCount }})
          </button>
        </div>

        <div class="dashboard-grid">

          <!-- Payments Tab content -->
          <template v-if="activeTab === 'payments'">
            <div class="card form-card">
              <h3 class="card-title">{{ $t('admin.manual_title') }}</h3>
              <div class="admin-panel">
                <label>{{ $t('admin.order_id') }}</label>
                <input
                  type="number"
                  v-model="orderIdInput"
                  :placeholder="$t('admin.order_id_placeholder')"
                  class="admin-input"
                />

                <div class="action-buttons">
                  <button class="approve-btn" @click="handleManualSubmit(true)" :disabled="isActionLoading">
                    {{ $t('admin.approve') }}
                  </button>
                  <button class="reject-btn" @click="handleManualSubmit(false)" :disabled="isActionLoading">
                    {{ $t('admin.reject') }}
                  </button>
                </div>
              </div>
            </div>

            <div class="card table-card">
              <h3 class="card-title">
                {{ $t('admin.pending_table_title') }} ({{ pendingOrders.length }})
              </h3>

              <div v-if="pendingOrders.length === 0" class="empty-state">
                <p>{{ $t('admin.no_pending') }}</p>
              </div>

              <div v-else class="table-responsive">
                <table class="orders-table">
                  <thead>
                    <tr>
                      <th>{{ $t('admin.col_order_id') }}</th>
                      <th>{{ $t('admin.col_customer') }}</th>
                      <th>{{ $t('admin.col_email') }}</th>
                      <th>{{ $t('admin.col_amount') }}</th>
                      <th>{{ $t('admin.col_date') }}</th>
                      <th>{{ $t('admin.col_actions') }}</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="order in pendingOrders" :key="order.id">
                      <td class="font-bold">#{{ order.id }}</td>
                      <td>{{ order.customer_name }}</td>
                      <td>{{ order.customer_email }}</td>
                      <td class="amount">{{ order.total.toFixed(2) }} ₺</td>
                      <td class="date-cell">{{ formatDate(order.created_at) }}</td>
                      <td>
                        <div class="row-actions">
                          <button
                            class="approve-badge-btn"
                            @click="handleApproval(order.id, true)"
                            :disabled="isActionLoading"
                            :title="$t('admin.approve_payment')"
                          >
                            ✓ {{ $t('admin.approve_payment') }}
                          </button>
                          <button
                            class="reject-badge-btn"
                            @click="handleApproval(order.id, false)"
                            :disabled="isActionLoading"
                            :title="$t('admin.reject')"
                          >
                            ✗ {{ $t('admin.reject') }}
                          </button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </template>

          <!-- Comments Tab content -->
          <template v-else-if="activeTab === 'comments'">
            <div class="card table-card full-width">
              <h3 class="card-title">
                {{ $t('admin.pending_comments_title') || 'Onay Bekleyen Değerlendirmeler' }} ({{ pendingComments.length }})
              </h3>

              <div v-if="pendingComments.length === 0" class="empty-state">
                <p>{{ $t('admin.no_pending_comments') || 'Onay bekleyen yorum bulunmuyor.' }}</p>
              </div>

              <div v-else class="table-responsive">
                <table class="orders-table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>{{ $t('admin.col_customer') || 'Kullanıcı' }}</th>
                      <th>{{ $t('admin.rating') || 'Puan' }}</th>
                      <th>{{ $t('admin.comment') || 'Yorum' }}</th>
                      <th>{{ $t('admin.col_date') || 'Tarih' }}</th>
                      <th>{{ $t('admin.col_actions') || 'İşlemler' }}</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="c in pendingComments" :key="c.id">
                      <td class="font-bold">#{{ c.id }}</td>
                      <td>{{ c.user_name }}</td>
                      <td class="amount">★ {{ c.rating }} / 5</td>
                      <td>{{ c.content }}</td>
                      <td class="date-cell">{{ formatDate(c.created_at) }}</td>
                      <td>
                        <div class="row-actions">
                          <button
                            class="approve-badge-btn"
                            @click="handleCommentApproval(c.id, true)"
                            :disabled="isActionLoading"
                          >
                            ✓ {{ $t('admin.approve') || 'Onayla' }}
                          </button>
                          <button
                            class="reject-badge-btn"
                            @click="handleCommentApproval(c.id, false)"
                            :disabled="isActionLoading"
                          >
                            ✗ {{ $t('admin.reject') || 'Sil' }}
                          </button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </template>

          <!-- Feedbacks Tab content -->
          <template v-else-if="activeTab === 'feedbacks'">
            <div class="card table-card full-width">
              <h3 class="card-title">
                {{ $t('admin.user_feedbacks_title') || 'Kullanıcı Geri Bildirimleri' }} ({{ feedbacks.length }})
              </h3>

              <div v-if="feedbacks.length === 0" class="empty-state">
                <p>{{ $t('admin.no_feedbacks') || 'Geri bildirim bulunmuyor.' }}</p>
              </div>

              <div v-else class="table-responsive">
                <table class="orders-table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>{{ $t('admin.col_customer') || 'Kullanıcı' }}</th>
                      <th>{{ $t('admin.col_email') || 'E-posta' }}</th>
                      <th>{{ $t('admin.feedback_type') || 'Tür' }}</th>
                      <th>{{ $t('admin.feedback_message') || 'Mesaj' }}</th>
                      <th>{{ $t('admin.col_date') || 'Tarih' }}</th>
                      <th>{{ $t('admin.col_actions') || 'İşlemler' }}</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="f in feedbacks" :key="f.id" :class="{ 'unread-row': !f.is_read }">
                      <td class="font-bold">#{{ f.id }}</td>
                      <td>{{ f.user_name }}</td>
                      <td>{{ f.user_email }}</td>
                      <td>
                        <span :class="['feedback-type-badge', f.type]">
                          {{ $t(`profile.feedback_${f.type}`) || f.type }}
                        </span>
                      </td>
                      <td style="max-width: 300px; word-wrap: break-word; white-space: normal;">{{ f.message }}</td>
                      <td class="date-cell">{{ formatDate(f.created_at) }}</td>
                      <td>
                        <div class="row-actions">
                          <button
                            v-if="!f.is_read"
                            class="approve-badge-btn"
                            @click="handleFeedbackRead(f.id)"
                            :disabled="isActionLoading"
                          >
                            ✓ {{ $t('admin.mark_as_read') || 'Okundu İşaretle' }}
                          </button>
                          <span v-else class="read-status-text">
                            {{ $t('admin.read') || 'Okundu' }}
                          </span>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </template>

        </div>
      </div>

    </div>
  </main>
</template>

<style scoped>
.page-content {
  padding: 60px 0;
  background-color: #f9f9f9;
  min-height: 80vh;
}
.content-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}
.page-title {
  font-size: 2.2rem;
  font-weight: 800;
  margin-bottom: 5px;
  color: #1a1a1a;
  text-align: center;
}
.desc {
  margin-bottom: 40px;
  color: #666;
  text-align: center;
  font-size: 1.1rem;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 30px;
}

@media (min-width: 992px) {
  .dashboard-grid {
    grid-template-columns: 350px 1fr;
  }
}

.card {
  background: #ffffff;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.05);
  border: 1px solid #eee;
  text-align: left;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(0,0,0,0.08);
}

.card-title {
  font-size: 1.25rem;
  font-weight: 700;
  margin-top: 0;
  margin-bottom: 20px;
  color: #111;
  border-bottom: 2px solid #f1f1f1;
  padding-bottom: 10px;
}

.admin-panel label {
  display: block;
  font-weight: 600;
  margin-bottom: 8px;
  font-size: 0.95rem;
  color: #444;
}
.admin-input {
  width: 100%;
  padding: 12px;
  margin-bottom: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
  box-sizing: border-box;
  transition: border-color 0.2s;
}
.admin-input:focus {
  border-color: #c00a00;
  outline: none;
}
.action-buttons {
  display: flex;
  gap: 12px;
}
.approve-btn {
  flex: 1;
  background-color: #2ec156;
  color: #fff;
  border: none;
  padding: 12px;
  font-size: 1rem;
  font-weight: 700;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
}
.approve-btn:hover:not(:disabled) { background-color: #249743; }
.reject-btn {
  flex: 1;
  background-color: #EA4335;
  color: #fff;
  border: none;
  padding: 12px;
  font-size: 1rem;
  font-weight: 700;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
}
.reject-btn:hover:not(:disabled) { background-color: #c73628; }

.table-card {
  overflow: hidden;
}
.table-responsive {
  overflow-x: auto;
}
.orders-table {
  width: 100%;
  border-collapse: collapse;
}
.orders-table th, .orders-table td {
  padding: 14px 16px;
  text-align: left;
  border-bottom: 1px solid #eee;
  font-size: 0.95rem;
}
.orders-table th {
  background-color: #fafafa;
  font-weight: 700;
  color: #555;
  text-transform: uppercase;
  font-size: 0.8rem;
  letter-spacing: 0.5px;
}
.orders-table tr:hover {
  background-color: #fcfcfc;
}
.font-bold {
  font-weight: 700;
  color: #111;
}
.amount {
  font-weight: 700;
  color: #c00a00;
}
.date-cell {
  color: #666;
  font-size: 0.85rem;
}
.row-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
.approve-badge-btn {
  background-color: #e6f7ec;
  color: #249743;
  border: 1px solid #c2eed0;
  padding: 6px 12px;
  font-size: 0.85rem;
  font-weight: 700;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}
.approve-badge-btn:hover:not(:disabled) {
  background-color: #249743;
  color: white;
}
.reject-badge-btn {
  background-color: #fdebee;
  color: #EA4335;
  border: 1px solid #fad2d6;
  padding: 6px 12px;
  font-size: 0.85rem;
  font-weight: 700;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}
.reject-badge-btn:hover:not(:disabled) {
  background-color: #EA4335;
  color: white;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #777;
  font-size: 1rem;
}

.loading-container {
  text-align: center;
  padding: 80px 0;
}
.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #c00a00;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.unauthorized-card {
  background: white;
  padding: 50px 30px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.05);
  border: 1px solid #eee;
  max-width: 500px;
  margin: 40px auto;
  text-align: center;
}
.lock-icon {
  font-size: 3rem;
  display: block;
  margin-bottom: 20px;
}
.unauthorized-card h2 {
  font-size: 1.8rem;
  margin-bottom: 10px;
  color: #c00a00;
}
.unauthorized-card p {
  color: #555;
  margin-bottom: 30px;
  line-height: 1.5;
}
.home-btn {
  background-color: #111;
  color: white;
  padding: 12px 24px;
  border-radius: 50px;
  text-decoration: none;
  font-weight: 700;
  font-size: 0.95rem;
  display: inline-block;
  transition: background-color 0.2s;
}
.home-btn:hover {
  background-color: #333;
}
button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Admin Tabs CSS */
.admin-tabs {
  display: flex;
  gap: 15px;
  margin-bottom: 30px;
  justify-content: center;
}
.tab-btn {
  background-color: var(--card-bg, #fff);
  color: var(--text-color, #333);
  border: 1px solid var(--border-color, #eee);
  padding: 10px 24px;
  font-size: 1rem;
  font-weight: 700;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 12px rgba(0,0,0,0.03);
}
.tab-btn:hover {
  border-color: #c00a00;
}
.tab-btn.active {
  background-color: #c00a00;
  color: white;
  border-color: #c00a00;
}
.full-width {
  grid-column: 1 / -1;
}

/* Feedbacks Tab CSS */
.unread-row {
  background-color: #fff9f9;
  font-weight: 500;
}
.dark-theme .unread-row {
  background-color: #2a1f2d !important;
}
.feedback-type-badge {
  padding: 4px 10px;
  border-radius: 50px;
  font-size: 0.8rem;
  font-weight: bold;
  text-transform: capitalize;
}
.feedback-type-badge.sikayet { background-color: #f8d7da; color: #721c24; }
.feedback-type-badge.oneri { background-color: #d1ecf1; color: #0c5460; }
.feedback-type-badge.siparis { background-color: #fff3cd; color: #856404; }
.feedback-type-badge.bilgi { background-color: #d4edda; color: #155724; }

.dark-theme .feedback-type-badge.sikayet { background-color: #4c1d24; color: #f8d7da; }
.dark-theme .feedback-type-badge.oneri { background-color: #0c3a44; color: #d1ecf1; }
.dark-theme .feedback-type-badge.siparis { background-color: #4e3f16; color: #fff3cd; }
.dark-theme .feedback-type-badge.bilgi { background-color: #1b4721; color: #d4edda; }

.read-status-text {
  color: #888;
  font-size: 0.85rem;
  font-weight: 600;
}
</style>
