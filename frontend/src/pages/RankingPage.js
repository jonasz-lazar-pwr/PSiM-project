// Autorzy: Jonasz Lazar, Kacper Malinowski

// Komponent RankingPage służy do wyświetlania rankingu użytkowników.
// Wykorzystuje kontekst AuthContext do uzyskania informacji o aktualnie zalogowanym użytkowniku.
// Wykorzystuje hook useEffect do pobrania rankingu użytkowników z serwera po załadowaniu komponentu.
// Użytkownik może sortować ranking według liczby zdobytych krasnali lub liczby dodanych komentarzy.
// Jeżeli użytkownik nie jest zalogowany, jest przekierowywany na stronę logowania.
// W rankingu, wiersz z aktualnie zalogowanym użytkownikiem jest wyróżniony.

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import Layout from '../components/Layout';
import { useNavigate } from 'react-router-dom';

const RankingPage = () => {
    const [users, setUsers] = useState([]);
    const [sort, setSort] = useState('num_dwarfs');
    const { user } = useAuth();
    const navigate = useNavigate();

    const apiUrl = process.env.REACT_APP_API_URL;

    useEffect(() => {
        if (!user) {
            navigate("/login");
        } else {
            const fetchUsers = async () => {
                try {
                    const response = await axios.get(`${apiUrl}users_ranking?sort_by=${sort}`);
                    setUsers(response.data);
                } catch (error) {
                    console.error(error);
                }
            };

            fetchUsers();
        }
    }, [sort, user, navigate, apiUrl]);

    return (
        <Layout>
            <div className="container mt-4">
                <h1 className="mb-3">Ranking użytkowników</h1>
                <ul className="list-group">
                    <li className="list-group-item">
                        <div className="row">
                            <div className="col-md-3"><strong>Pozycja w rankingu</strong></div>
                            <div className="col-md-3"><strong>Nazwa użytkownika</strong></div>
                            <div className="col-md-3">
                                <strong>
                                    {/*eslint-disable-next-line*/}
                                    <a href="#" onClick={(e) => {e.preventDefault(); setSort('num_dwarfs');}}>Liczba zdobytych krasnali</a>
                                </strong>
                            </div>
                            <div className="col-md-3">
                                <strong>
                                    {/*eslint-disable-next-line*/}
                                    <a href="#" onClick={(e) => {e.preventDefault(); setSort('num_comments');}}>Liczba dodanych komentarzy</a>
                                </strong>
                            </div>
                        </div>
                    </li>
                    {users.map((userItem, index) => (
                        <li className={`list-group-item ${userItem.username === user.username ? 'highlight' : ''}`}
                            key={index}
                            style={userItem.username === user.username ? { backgroundColor: 'lightgray' } : {}}
                        >
                            <div className="row">
                                <div className="col-md-3">{index + 1}</div>
                                <div className="col-md-3">{userItem.username}</div>
                                <div className="col-md-3">{userItem.num_dwarfs}</div>
                                <div className="col-md-3">{userItem.num_comments}</div>
                            </div>
                        </li>
                    ))}
                </ul>
            </div>
        </Layout>
    );
};

export default RankingPage;