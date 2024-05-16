// Autorzy: Jonasz Lazar, Kacper Malinowski

// Komponent CommentDwarfPage pozwala użytkownikowi na dodanie komentarza do wybranego krasnala.
// Wykorzystuje kontekst AuthContext do uzyskania informacji o aktualnie zalogowanym użytkowniku.
// Jeżeli użytkownik nie jest zalogowany, krasnal jest zablokowany lub użytkownik już skomentował tego krasnala, przekierowuje go do strony krasnala.
// Wykorzystuje hook useEffect do pobrania danych o krasnalu po załadowaniu komponentu.
// Po wypełnieniu formularza, komentarz jest wysyłany do serwera, a następnie użytkownik jest przekierowywany do strony krasnala.

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';
import { useAuth } from '../context/AuthContext';

const CommentDwarfPage = () => {
    const [commentText, setCommentText] = useState('');
    const { id } = useParams();
    const navigate = useNavigate();
    const { user } = useAuth();

    const apiUrl = process.env.REACT_APP_API_URL;

    useEffect(() => {
        const fetchDwarf = async () => {
            try {
                const authTokens = JSON.parse(localStorage.getItem('authTokens'));
                const config = authTokens ? {
                    headers: {
                        'Authorization': `Bearer ${authTokens.access}`
                    }
                } : {};
                const response = await axios.get(`${apiUrl}dwarfs/${id}`, config);

                // Przeprowadź sprawdzenie tutaj, po pobraniu danych o krasnolu
                if (!user || !response.data.is_unlocked || response.data.user_comments_count > 0) {
                    navigate(`/dwarfs/${id}`);
                }
            } catch (error) {
                console.error(error);
            }
        };

        fetchDwarf();
    }, [id, user, navigate, apiUrl]);

    const handleSubmit = async (event) => {
        event.preventDefault();
        const authTokens = JSON.parse(localStorage.getItem('authTokens'));
        const config = authTokens ? {
            headers: {
                'Authorization': `Bearer ${authTokens.access}`
            }
        } : {};
        await axios.post(`${apiUrl}dwarfs/${id}/comments/`, { comment_text: commentText }, config);
        navigate(`/dwarfs/${id}`);
    };

    return (
        <Layout>
            <div className="container mt-4">
                <div className="row justify-content-center">
                    <div className="col-md-8">
                        <div className="card">
                            <div className="card-header bg-white">
                                <h3 className="text-dark mb-0">Dodaj komentarz</h3>
                            </div>
                            <div className="card-body">
                                <form onSubmit={handleSubmit}>
                                    <div className="form-group">
                                        <label htmlFor="comment_text">Twój komentarz:</label>
                                        <textarea className="form-control mt-3" id="comment_text" value={commentText} onChange={e => setCommentText(e.target.value)} rows="5" placeholder="Wpisz swój komentarz tutaj" required />
                                    </div>
                                    <button type="submit" className="btn btn-primary mt-3">Opublikuj</button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </Layout>
    );
};

export default CommentDwarfPage;