// Autorzy: Jonasz Lazar, Kacper Malinowski

// Komponent LoginPage służy do logowania użytkowników.
// Wykorzystuje kontekst AuthContext do logowania użytkowników i uzyskania informacji o aktualnie zalogowanym użytkowniku.
// Wykorzystuje hook useEffect do przekierowania zalogowanego użytkownika na stronę główną.
// Użytkownik wprowadza swoją nazwę użytkownika i hasło, które są przechowywane w stanie komponentu.
// Po naciśnięciu przycisku "Zaloguj się", dane są przekazywane do funkcji loginUser z kontekstu AuthContext.
// Jeżeli logowanie się nie powiedzie, wyświetlany jest komunikat o błędzie.
// Jeżeli logowanie się powiedzie, użytkownik jest przekierowywany na stronę główną.

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Layout from '../components/Layout';

const LoginPage = () => {
    const { user, loginUser } = useAuth();
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    useEffect(() => {
      if (user) {
        navigate('/');
      }
    }, [user, navigate]);


    const handleSubmit = async (e) => {
        e.preventDefault();
        const error = await loginUser(username, password);
        if (error) {
            setError(error);
        } else {
            navigate('/');
        }
    };

    return (
        <Layout>
            <div className="container mt-4">
                <div className="row justify-content-center">
                    <div className="col-md-6">
                        <div className="card">
                            <div className="card-body">
                                <h2 className="card-title mb-4">Logowanie</h2>
                                <form onSubmit={handleSubmit}>
                                    {error && <p className="card-text text-danger">{error}</p>}
                                    <div className="form-group">
                                        <label htmlFor="username">Nazwa użytkownika:</label>
                                        <input type="text" id="username" className="form-control" value={username} onChange={(e) => setUsername(e.target.value)} />
                                    </div>
                                    <div className="form-group">
                                        <label htmlFor="password">Hasło:</label>
                                        <input type="password" id="password" className="form-control" value={password} onChange={(e) => setPassword(e.target.value)} />
                                    </div>
                                    <button type="submit" className="btn btn-primary btn-block mt-3">Zaloguj się</button>
                                </form>
                            </div>
                        </div>
                        <div className="text-center mt-2">
                            Nie masz konta? Zarejestruj się <a href="/register">tutaj</a>
                        </div>
                    </div>
                </div>
            </div>
        </Layout>
    );
};

export default LoginPage;