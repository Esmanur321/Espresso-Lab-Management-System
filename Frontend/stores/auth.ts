import { defineStore } from 'pinia';
import type { IUser } from '~/types';

export const useAuthStore = defineStore('auth', {
  state: () => {
    let user = null as IUser | null;
    let isAuthenticated = false;
    
    if (process.client) {
      const savedUser = localStorage.getItem('auth_user');
      const savedAuth = localStorage.getItem('auth_authenticated');
      if (savedUser && savedAuth === 'true') {
        try {
          user = JSON.parse(savedUser);
          isAuthenticated = true;
        } catch (e) {
          console.error('Failed to parse saved user:', e);
        }
      }
    }
    
    return {
      user,
      isAuthenticated,
      isLoading: false
    };
  },

  getters: {
    fullName: (state) =>
      state.user ? `${state.user.name} ${state.user.surname}`.trim() : '',

    isLoggedIn: (state) => state.isAuthenticated && state.user !== null,

    isAdmin: (state) => state.user?.role === 'admin'
  },

  actions: {
    setSession(userData: IUser) {
      this.user = userData;
      this.isAuthenticated = true;
      if (process.client) {
        localStorage.setItem('auth_user', JSON.stringify(userData));
        localStorage.setItem('auth_authenticated', 'true');
      }
    },

    async login(credentials: any) {
      this.isLoading = true;
      try {
        const { $api } = useNuxtApp() as any;
        const response = await $api('http://localhost:8000/auth/login', {
          method: 'POST',
          body: {
            email: credentials.email,
            password: credentials.password
          }
        });

        if (response && response.status === 'success') {
          this.user = {
            uid: String(response.user.id),
            name: response.user.name,
            surname: response.user.surname,
            email: response.user.email,
            phone: response.user.phone || '',
            birthDate: '',
            role: response.user.is_admin ? 'admin' : 'user'
          };
          this.isAuthenticated = true;
          
          if (process.client) {
            localStorage.setItem('auth_user', JSON.stringify(this.user));
            localStorage.setItem('auth_authenticated', 'true');
            if (response.token) {
              localStorage.setItem('auth_token', response.token);
            }
          }
          console.log('✅ Real login başarılı:', this.user.name);
        }
      } catch (error: any) {
        console.error('Login error:', error);
        throw new Error(error?.data?.detail || 'Giriş başarısız oldu.');
      } finally {
        this.isLoading = false;
      }
    },

    async socialLogin(provider: string, token: string) {
      this.isLoading = true;
      try {
        const { $api } = useNuxtApp() as any;
        const response = await $api('http://localhost:8000/auth/social-login', {
          method: 'POST',
          body: {
            provider: provider,
            access_token: token
          }
        });

        if (response && response.status === 'success') {
          this.user = {
            uid: String(response.user.id),
            name: response.user.name,
            surname: response.user.surname || '',
            email: response.user.email,
            phone: response.user.phone || '',
            birthDate: '',
            role: response.user.is_admin ? 'admin' : 'user'
          };
          this.isAuthenticated = true;
          
          if (process.client) {
            localStorage.setItem('auth_user', JSON.stringify(this.user));
            localStorage.setItem('auth_authenticated', 'true');
            if (response.token) {
              localStorage.setItem('auth_token', response.token);
            }
          }
          console.log('✅ Social login başarılı:', this.user.name);
        }
      } catch (error: any) {
        console.error('Social Login error:', error);
        throw new Error(error?.data?.detail || 'Sosyal medya girişi başarısız oldu.');
      } finally {
        this.isLoading = false;
      }
    },

    async register(userData: any) {
      this.isLoading = true;
      try {
        const { $api } = useNuxtApp() as any;
        const response = await $api('http://localhost:8000/users/', {
          method: 'POST',
          body: {
            name: userData.name,
            surname: userData.surname,
            email: userData.email,
            password: userData.password,
            phone: userData.phone || '',
            gender: userData.gender || 'belirtmem',
            birth_date: userData.birthDate || ''
          }
        });

        if (response && response.id) {
          this.user = {
            uid: String(response.id),
            name: response.name,
            surname: response.surname,
            email: response.email,
            phone: response.phone || '',
            birthDate: response.birth_date || '',
            role: response.is_admin ? 'admin' : 'user'
          };
          this.isAuthenticated = true;
          
          if (process.client) {
            localStorage.setItem('auth_user', JSON.stringify(this.user));
            localStorage.setItem('auth_authenticated', 'true');
          }
          console.log('✅ Real kayıt başarılı:', this.user.name);
        }
      } catch (error: any) {
        console.error('Register error:', error);
        throw new Error(error?.data?.detail || 'Kayıt başarısız oldu.');
      } finally {
        this.isLoading = false;
      }
    },

    /** Refresh name, email, admin flag from backend (fixes stale localStorage after DB role change). */
    async syncProfileFromServer() {
      if (!process.client || !this.user?.uid) return;

      try {
        const { $api } = useNuxtApp() as any;
        const profile = await $api(`http://localhost:8000/users/${this.user.uid}`);
        if (!profile?.id) return;

        this.user = {
          ...this.user,
          name: profile.name,
          surname: profile.surname,
          email: profile.email,
          phone: profile.phone || '',
          role: profile.is_admin ? 'admin' : 'user'
        };
        localStorage.setItem('auth_user', JSON.stringify(this.user));
      } catch (e) {
        console.warn('Could not sync user profile from server:', e);
      }
    },

    async logout() {
      this.user = null;
      this.isAuthenticated = false;
      if (process.client) {
        localStorage.removeItem('auth_user');
        localStorage.removeItem('auth_authenticated');
        localStorage.removeItem('auth_token');
      }
      console.log('✅ Çıkış yapıldı');
    },

    async deleteAccount() {
      this.user = null;
      this.isAuthenticated = false;
      if (process.client) {
        localStorage.removeItem('auth_user');
        localStorage.removeItem('auth_authenticated');
        localStorage.removeItem('auth_token');
      }
    }
  }
});
