# ESPRESSOLAB E-COMMERCE FRONTEND SYSTEM
## Technical Documentation & Client Architecture Manual

---

## 1. Application Architecture and Directory Structure

### 1.1. Application Architecture
The client application is built using the **Nuxt 3** framework, which implements a modern, high-performance Vue 3 client architecture. The application leverages file-based routing, client-side rendering (CSR), and modular state management to present a premium user interface.

To ensure separation of concerns and component reusability, the user interface is designed following **Atomic Design** principles, dividing UI elements into:
*   **Atoms:** Single-purpose, primitive components (buttons, check-boxes, inputs, star badges) that carry styling but no direct business logic.
*   **Molecules:** Simple combinations of atoms (cards, breadcrumbs, inputs with buttons) that represent small functional units.
*   **Organisms:** Complex UI assemblies containing business logic and API integrations (headers, footers, best-seller sliders, reviews list, and payment forms).

### 1.2. Directory Structure

The directory organization is detailed below:

```text
Frontend/
│
├── app.vue                       # Root application view configuring layout & global Dark Mode styles
├── nuxt.config.ts                # Main Nuxt 3 configuration file (registers Pinia and global setups)
│
├── components/                   # UI Component Directory (Atomic Design)
│   ├── atoms/                    # Primitive elements (BaseButton, PriceDisplay, QuantitySpinner, ProfileNavLink)
│   ├── molecules/                # Simple layouts (CampaignCard, Breadcrumbs, ProductCard, LangSwitcher)
│   └── organisms/                # Smart blocks (TheHeader, TheFooter, StoreBestSellers, StoreSlider, CartSidebar)
│
├── composables/                  # Shared composition API states (useI18n, useTheme, useToast)
│
├── layouts/                      # Layout templates
│   └── default.vue               # Main page layout containing Header, Page Slot, and Footer
│
├── middleware/                   # Route protection guards
│   ├── auth.ts                   # Restricts profile/checkout to logged-in users
│   └── admin.ts                  # Restricts admin panel to users with administrative privileges
│
├── pages/                        # File-system routes
│   ├── admin.vue                 # Admin Panel (Offline Payments, Comments, & Feedbacks management)
│   ├── campaigns.vue             # Promotional Campaigns information view
│   ├── cart.vue                  # Shopping Cart items listing & summary checkout bridge
│   ├── checkout.vue              # Stripe Card Payments and bank transfer checkout forms
│   ├── profile.vue               # User settings, addresses, order history, and feedback form
│   ├── store/
│   │   └── index.vue             # Online Store storefront (filters, search, best sellers list)
│   └── product/
│       └── [id].vue              # Product detailed view, star reviews, and submission form
│
├── stores/                       # Global state stores driven by Pinia
│   ├── auth.ts                   # Handles user profiles and admin role flags
│   ├── cart.ts                   # Cart list items, subtotal calculators, and storage sync
│   ├── products.ts               # Local cache for active products
│   └── favorites.ts              # Wishlist persistence
│
└── utils/
    └── locales.ts                # Localization dictionary maps for TR and EN locales
```

---

## 2. List of Utilized Libraries and Justification

The following libraries are integrated into the Frontend client:

| Library | Role in Project | Selection Justification |
| :--- | :--- | :--- |
| **Nuxt 3** | Core Framework | Out-of-the-box routing, auto-importing features, high performance rendering options, and structured directory layouts. |
| **Vue 3** | Logic Framework | Reusable Composition API, fast Virtual DOM, and reactive data properties. |
| **Pinia** | State Management | Modular design, simple configuration, and full reactivity support. |
| **Vee-Validate & Yup** | Input Validation | Manages form validation errors, tracking input states and formatting validation rules in schemas. |
| **Firebase SDK** | User Authentication | Handshakes federated Google/Facebook OAuth2 authentication securely. |
| **Sass (SCSS)** | Styling Compiler | Enables structured variables, nesting, and modular styles. |
| **Vitest** | Automated Testing | High performance frontend test runner natively integrated with Vite and Nuxt configurations. |

---

## 3. UI Mockups and Screenshots

The application features a sleek dark brand theme (`#111827`). Below are the actual system screenshots illustrating the production environments for key application pages:

### 3.1. Storefront Page Layout (Store View Grid Toggle)
Displays store categories, promotional slides, and product lists. The storefront has a responsive product layout and manual control sliders for best-selling items:

![Storefront Production Screenshot](./screenshot_1.png)


### 3.2. Product Details Page (Star Review Section)
Includes product images, descriptions, rating averages next to titles (e.g. `★ 4.8`), and a customer reviews layout section:

![Product Details Page Main View](./screenshot_2.png)


![Product Details Page Reviews Form](./screenshot_3.png)

### 3.3. Admin Panel Page Layout
Allows administrators to manage payment actions, pending reviews, and feedback messages using tabs:

![Admin Control Panel Dashboard](./screenshot_4.png)


---

## 4. State Management Strategy

Client-side persistence and reactivity are managed using **Pinia** stores.

### 4.1. Pinia Store Configurations
1.  **Authentication (`stores/auth.ts`):** Manages user session state, user login metadata, and administrator flags (`isAdmin`). Handles API calls for login and logouts.
2.  **Shopping Cart (`stores/cart.ts`):** Handles adding, updating, and removing items in the cart. Automatically calculates intermediate values (subtotal, shipping, 10% promotional discounts).
3.  **Local Storage Synchronization:** Cart item array state and wishlist item records synchronize with the browser's `localStorage` on modifications. This prevents data loss when page reloads occur.

### 4.2. Internationalization (i18n) Persistence
The language preference state (e.g. `tr` or `en`) is managed through the `useI18n` composable. When a user toggles the LangSwitcher, the application updates the active locale state in memory, updates translations, and saves the choice in `localStorage`. Upon returning, Nuxt reads this key to restore the localized view.

---

## 5. API Communication Documentation

The client communicates with the FastAPI backend through a custom API wrapper.

### 5.1. API Request Layer
The frontend sets up a Nuxt `$api` plugin (defined in `plugins/api.ts`) that configures a baseline client fetching provider:
*   **Base URL:** Connected to `http://localhost:8000`.
*   **Credentials:** Configured with `allow_credentials=True` headers to manage sessions.
*   **Request Interceptors:** Adds required authorization parameters (e.g., passing the admin's `uid` query param for protected administrative actions).

### 5.2. Integration Example (Submitting Feedback)
In `pages/profile.vue`, the feedback form invokes the backend endpoint asynchronously:
```typescript
const sendFeedback = async () => {
  try {
    await $api('http://localhost:8000/feedbacks/', {
      method: 'POST',
      body: {
        user_id: parseInt(store.user.uid),
        type: feedback.value.type,
        message: feedback.value.message
      }
    });
    showToast('Feedback submitted successfully!', 'success');
  } catch (error) {
    showToast('Failed to send feedback.', 'error');
  }
};
```

---

## 6. Instructions for Building and Running the Application

Follow these steps to run the frontend client application:

### 6.1. Package Installation
Navigate to the `Frontend` directory and install the required npm dependencies:
```bash
cd Frontend
npm install
```

### 6.2. Running the Development Server
Launch the local development environment:
```bash
npm run dev
```
*The client application will start at [http://localhost:3000](http://localhost:3000).*

### 6.3. Production Build and Preview
To generate a production bundle and run the preview:
```bash
# Build the production bundle
npm run build

# Preview production bundle locally
npm run preview
```

### 6.4. Running Frontend Unit Tests
Execute the Vitest runner:
```bash
npm run test
```
