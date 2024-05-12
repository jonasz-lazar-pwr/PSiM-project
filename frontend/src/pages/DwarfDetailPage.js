// Autorzy: Jonasz Lazar, Kacper Malinowski

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import Layout from '../components/Layout';
import { useParams } from 'react-router-dom';

const DwarfDetailPage = () => {
    const { user } = useAuth();
    const [dwarf, setDwarf] = useState(null);
    const [comments, setComments] = useState([]);
    const [hasUnlocked, setHasUnlocked] = useState(false);
    const [userCommentsCount, setUserCommentsCount] = useState(0);

    const { id } = useParams();

    const apiUrl = process.env.REACT_APP_API_URL;

    const deleteComment = async (commentId) => {
        try {
            const authTokens = JSON.parse(localStorage.getItem('authTokens'));
            const config = authTokens ? {
                headers: {
                    'Authorization': `Bearer ${authTokens.access}`
                }
            } : {};
            await axios.delete(`${apiUrl}comments/${commentId}`, config);
            setComments(comments.filter(comment => comment.id !== commentId));
            setUserCommentsCount(userCommentsCount - 1);
        } catch (error) {
            console.error(error);
        }
    };

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
                setDwarf(response.data);
                setHasUnlocked(response.data.is_unlocked);
                setComments(response.data.comments);
                setUserCommentsCount(response.data.user_comments_count);
            } catch (error) {
                console.error(error);
            }
        };

        fetchDwarf();
    }, [id, apiUrl]);

    return (
        <Layout>
            <div className="container mt-4">
                {dwarf && (
                    <>
                        <h1 className="mb-3">{dwarf.name}</h1>
                        {user && (hasUnlocked ? <p className="text-success">Zdobyty</p> : <p className="text-danger">Niezdobyty</p>)}
                        <p><strong>Autor:</strong> {dwarf.author}</p>
                        <p><strong>Lokalizacja:</strong> {dwarf.address} ({dwarf.location})</p>
                        <p><strong>Opis:</strong> {dwarf.description}</p>
                        <img src={dwarf.image_url} alt={dwarf.name} className="img-fluid mb-3" />
                        {user && (
                            <div className="d-flex justify-content-between align-items-center mb-3">
                                <div className="col-4">
                                    <h2>Komentarze</h2>
                                </div>
                                <div className="col-4 text-center">
                                    {hasUnlocked ? (
                                        <p className="mb-0">{userCommentsCount}/1 umieszczonych komentarzy</p>
                                    ) : (
                                        <p className="mb-0">Zeskanuj kod QR, aby zdobyć krasnala.</p>
                                    )}
                                </div>
                                <div className="col-4 d-flex justify-content-end">
                                    {hasUnlocked ? (
                                        userCommentsCount < 1 && <Link to={`/dwarfs/${dwarf.id}/comment`} className="btn btn-primary">Dodaj komentarz</Link>
                                    ) : (
                                        <Link to="/verify_qr_code" className="btn btn-primary">Skanuj QR</Link>
                                    )}
                                </div>
                            </div>
                        )}
                    </>
                )}

                {user && comments && (
                    <div className="row mt-4">
                        <div className="col">
                            <ul className="list-group">
                                {comments.map((comment) => (
                                    <li className="list-group-item d-flex justify-content-between align-items-center" key={comment.id}>
                                        <div>
                                            <p>{comment.comment_text}</p>
                                            <small>{comment.user.username} - {new Date(comment.comment_date).toLocaleString()}</small>
                                        </div>
                                        {user && user.username === comment.user.username && (
                                            <button onClick={() => deleteComment(comment.id)} className="btn btn-danger">Usuń komentarz</button>
                                        )}
                                    </li>
                                ))}
                                {comments.length === 0 && <p>Brak komentarzy.</p>}
                            </ul>
                        </div>
                    </div>
                )}

                {!user && (
                    <p>Załóż konto, aby zobaczyć komentarze.</p>
                )}
            </div>
        </Layout>
    );
};

export default DwarfDetailPage;