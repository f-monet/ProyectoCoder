// Configuración pública del proyecto Firebase (no son credenciales secretas).
// La seguridad real está en las reglas de Firestore, no en ocultar estos valores.
const firebaseConfig = {
  apiKey: "AIzaSyCDddnBprANtPN_HOIY5tfgOUgHT3f-eYA",
  authDomain: "dashboardstone.firebaseapp.com",
  projectId: "dashboardstone",
  storageBucket: "dashboardstone.firebasestorage.app",
  messagingSenderId: "504122674314",
  appId: "1:504122674314:web:73349fb7c60ce8eb573173",
};

firebase.initializeApp(firebaseConfig);
