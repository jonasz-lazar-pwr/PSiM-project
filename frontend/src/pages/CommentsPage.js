// Autorzy: Jonasz Lazar, Kacper Malinowski

// Komponent CommentsPage wyświetla listę komentarzy dodanych przez użytkownika do różnych krasnali.
// Wykorzystuje kontekst AuthContext do uzyskania informacji o aktualnie zalogowanym użytkowniku.
// Jeżeli użytkownik nie jest zalogowany, przekierowuje go do strony logowania.
// Wykorzystuje hook useEffect do pobrania komentarzy użytkownika z serwera po załadowaniu komponentu.
// Każdy komentarz jest wyświetlany jako link, który przekierowuje do strony krasnala, do którego komentarz został dodany.

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import Layout from '../components/Layout';
import { useNavigate } from 'react-router-dom';

const CommentsPage = () => {
    const [comments, setComments] = useState([]);
    const { user } = useAuth();
    const navigate = useNavigate();

    const apiUrl = process.env.REACT_APP_API_URL;

    useEffect(() => {
        if (!user) {
            navigate("/login");
        } else {
            const fetchComments = async () => {
                try {
                    const authTokens = JSON.parse(localStorage.getItem('authTokens'));
                    const config = authTokens ? {
                        headers: {
                            'Authorization': `Bearer ${authTokens.access}`
                        }
                    } : {};
                    const response = await axios.get(`${apiUrl}user_comments`, config);
                    setComments(response.data);
                } catch (error) {
                    console.error(error);
                }
            };

            fetchComments();
        }
    }, [user, navigate, apiUrl]);

    return (
        <Layout>
            <div className="container mt-4">
                <h1>Moje komentarze</h1>
                <div className="list-group">
                    {comments.map((comment, index) => (
                        <a href={`/dwarfs/${comment.dwarf.id}`} className="list-group-item list-group-item-action" key={index}>
                            <div className="d-flex w-100 justify-content-between">
                                <h5 className="mb-1">{comment.dwarf.name}</h5>
                                <small>{new Date(comment.comment_date).toLocaleDateString()}</small>
                            </div>
                            <p className="mb-1">{comment.comment_text}</p>
                        </a>
                    ))}
                    {comments.length === 0 && <p className="list-group-item">Brak komentarzy.</p>}
                </div>
            </div>
        </Layout>
    );
};

export default CommentsPage;