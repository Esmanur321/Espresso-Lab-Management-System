import { describe, it, expect, beforeEach, vi } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useCartStore } from './cart';

// Mock the global process.client and $fetch
global.process = { ...global.process, client: true } as any;
(global as any).$fetch = vi.fn(() => Promise.resolve({ stock: 10 })) as any;

describe('Cart Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    // clear mock localstorage if any
    localStorage.clear();
  });

  it('should initialize with an empty cart', () => {
    const store = useCartStore();
    expect(store.items).toEqual([]);
    expect(store.totalItems).toBe(0);
    expect(store.subtotal).toBe(0);
    expect(store.isEmpty).toBe(true);
  });

  it('should add an item to the cart', async () => {
    const store = useCartStore();
    const product = { id: '1', name: 'Kahve', price: 50 };
    
    await store.addToCart(product, 2);
    
    expect(store.items.length).toBe(1);
    expect(store.items[0].quantity).toBe(2);
    expect(store.totalItems).toBe(2);
    expect(store.subtotal).toBe(100);
    expect(store.isEmpty).toBe(false);
  });

  it('should update quantity of an existing item', async () => {
    const store = useCartStore();
    const product = { id: '1', name: 'Kahve', price: 50 };
    
    await store.addToCart(product, 1);
    await store.updateQuantity('1', 5);
    
    expect(store.items[0].quantity).toBe(5);
    expect(store.subtotal).toBe(250);
  });

  it('should remove an item from the cart', async () => {
    const store = useCartStore();
    const product = { id: '1', name: 'Kahve', price: 50 };
    
    await store.addToCart(product, 1);
    await store.removeFromCart('1');
    
    expect(store.items.length).toBe(0);
  });

  it('should clear the cart', async () => {
    const store = useCartStore();
    const product = { id: '1', name: 'Kahve', price: 50 };
    
    await store.addToCart(product, 1);
    store.clearCart();
    
    expect(store.items.length).toBe(0);
  });
});
