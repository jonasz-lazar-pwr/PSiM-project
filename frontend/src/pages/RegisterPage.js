// Autorzy: Jonasz Lazar, Kacper Malinowski

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Layout from '../components/Layout';

const RegisterPage = () => {
    const { user, registerUser } = useAuth();
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [password2, setPassword2] = useState('');
    const [error, setError] = useState('');

    useEffect(() => {
      if (user) {
        navigate('/');
      }
    }, [user, navigate]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (password !== password2) { // Sprawdź, czy hasła są takie same
            setError('Hasła nie są takie same. Spróbuj ponownie.');
            return;
        }
        const error = await registerUser(username, password, password2);
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
                                <h2 className="card-title mb-4">Rejestracja</h2>
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
                                    <div className="form-group">
                                        <label htmlFor="confirmPassword">Potwierdź hasło:</label>
                                        <input type="password" id="password2" className="form-control" value={password2} onChange={(e) => setPassword2(e.target.value)}/>
                                    </div>
                                    <button type="submit" className="btn btn-primary btn-block mt-3">Zarejestruj się
                                    </button>
                                </form>
                            </div>
                        </div>
                        <div className="text-center mt-2">
                            Posiadasz konto? <a href="/login">Zaloguj się</a>
                        </div>
                    </div>
                </div>
            </div>
        </Layout>
    );
};

export default RegisterPage;