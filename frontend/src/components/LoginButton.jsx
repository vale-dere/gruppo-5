import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
//import { getAuth, signInWithPopup, GoogleAuthProvider, onAuthStateChanged } from 'firebase/auth';
//import '../services/firebase';

export default function LoginButton() {
  const navigate = useNavigate();

 /* useEffect(() => {
    const auth = getAuth();
    onAuthStateChanged(auth, user => {
      if (user) navigate('/dashboard');
    });
  }, [navigate]);

  const handleLogin = async () => {
    const provider = new GoogleAuthProvider();
    const auth = getAuth();
    try {
      await signInWithPopup(auth, provider);
    } catch (err) {
      alert('Login failed: ' + err.message);
    }
  };*/

  
const handleLogin = () => {
  window.location.href = '/dashboard'; // simula login andando direttamente alla dashboard
};

  return (
    <button onClick={handleLogin} className="px-4 py-2 bg-blue-600 text-white rounded">
      Login with Google
    </button>
  );
}