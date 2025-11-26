// /static/js/firebase.js
import { initializeApp } from "https://www.gstatic.com/firebasejs/12.2.1/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/12.2.1/firebase-auth.js";


const firebaseConfig = {
apiKey: "AIzaSyCVNU-cb9DQRk395LE2tjhI7FJKBjkzvXg",
authDomain: "empresa-tecnologia.firebaseapp.com",
projectId: "empresa-tecnologia",
storageBucket: "empresa-tecnologia.appspot.com",
messagingSenderId: "317305921158",
appId: "1:317305921158:web:b863bf634cfe6adcaffb07",
measurementId: "G-3P63NE5HQF"
};


export const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);


export function mensajeErrorAmigable(code) {
const map = {
'auth/invalid-credential': 'Credenciales inválidas. Verifica email y contraseña.',
'auth/invalid-email': 'Email inválido.',
'auth/user-disabled': 'Usuario deshabilitado.',
'auth/user-not-found': 'Usuario no encontrado.',
'auth/wrong-password': 'Contraseña incorrecta.',
'auth/email-already-in-use': 'Ese email ya está registrado.',
'auth/weak-password': 'La contraseña es muy débil (mínimo 6 caracteres).'
};
return map[code] || 'Ocurrió un error. Intenta nuevamente.';
}