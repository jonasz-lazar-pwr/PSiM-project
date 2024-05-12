// Autorzy: Jonasz Lazar, Kacper Malinowski

import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';

const Layout = ({ children }) => {
    const { user, logoutUser } = useAuth();
    const location = useLocation();

    return (
        <div>
            <nav className="navbar bg-dark navbar-expand-lg navbar-dark">
                <div className="container">
                    <Link className="navbar-brand" to="/">
                        Wrocławskie Krasnale
                        <i className="bi bi-house" style={{marginLeft: "10px"}}></i>
                    </Link>
                    <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                        <span className="navbar-toggler-icon"></span>
                    </button>

                    <div className="collapse navbar-collapse" id="navbarNavAltMarkup">
                        <div className="navbar-nav">
                            {location.pathname !== "/dwarfs" && <Link className="nav-link link" to="/dwarfs">Krasnale</Link>}
                            {user && location.pathname !== "/users_ranking" && <Link className="nav-link link" to="/users_ranking">Ranking</Link>}
                            {user && location.pathname !== "/user_achievements" && <Link className="nav-link link" to="/user_achievements">Osiągnięcia</Link>}
                            {user && location.pathname !== "/user_comments" && <Link className="nav-link link" to="/user_comments">Komentarze</Link>}
                            {user && location.pathname !== "/verify_qr_code" && <Link className="nav-link link" to="/verify_qr_code">Skanuj QR</Link>}
                        </div>
                        <div className="navbar-nav ms-auto">
                            {user ? (
                                <>
                                    <span className="navbar-text welcome-text">Witaj: {user.username}</span>
                                    <button className="nav-link link" onClick={logoutUser}>Wyloguj się</button>
                                </>
                            ) : (
                                <>
                                    {location.pathname !== "/login" && <Link className="nav-link link" to="/login">Zaloguj się</Link>}
                                    {location.pathname === "/login" && <Link className="nav-link link" to="/register">Zarejestruj się</Link>}
                                </>
                            )}
                        </div>
                    </div>
                </div>
            </nav>

            <div className="container mt-4">
                <div className="row">
                    <div className="col-md-12">
                        <div className="content">
                            {children}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Layout;