// import { initializeApp } from "firebase/app";
// import { getAuth } from "firebase/auth";
// import { getFirestore } from "firebase/firestore";

export default defineNuxtPlugin((nuxtApp) => {
  // const config = useRuntimeConfig();

  // // Replace with actual config or environment variables
  // const firebaseConfig = {
  //   apiKey: "AIzaSyC93bvf1CVOITI5hc9RCVI1Zwc1_nLFelE",
  //   authDomain: "espressolab-nuxt.firebaseapp.com",
  //   projectId: "espressolab-nuxt",
  //   storageBucket: "espressolab-nuxt.firebasestorage.app",
  //   messagingSenderId: "48137518496",
  //   appId: "1:48137518496:web:c209e00c1befba9b4538c5",
  //   measurementId: "G-6H3XQVHJX5"
  // };

  // const app = initializeApp(firebaseConfig);
  // const auth = getAuth(app);
  // const db = getFirestore(app);

  // WEEK 6 MOCK DATA: Firebase geçici olarak kapatıldı
  return {
    provide: {
      auth: null,
      db: null
    }
  };
});
