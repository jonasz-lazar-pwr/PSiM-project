// Autorzy: Jonasz Lazar, Kacper Malinowski

import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Layout from '../components/Layout';

const MainPage = () => {
    const { user } = useAuth();

    return (
        <Layout>
            <div className="container mt-4">
                <div className="row justify-content-center">
                    <div className="col-md-6 text-center">
                        <h1 className="mb-4">Strona główna</h1>
                        <div className="d-flex flex-column align-items-center links-container">
                            <Link className="btn btn-primary mb-2 w-50" to="/dwarfs">Lista krasnali</Link>
                            {user && (
                                <>
                                    <Link className="btn btn-primary mb-2 w-50" to="/users_ranking">Ranking użytkowników</Link>
                                    <Link className="btn btn-primary mb-2 w-50" to="/user_achievements">Moje osiągnięcia</Link>
                                    <Link className="btn btn-primary mb-2 w-50" to="/user_comments">Moje komentarze</Link>
                                    <Link className="btn btn-primary mb-2 w-50" to="/verify_qr_code">Skanuj QR</Link>
                                </>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </Layout>
    );
};

export default MainPage;