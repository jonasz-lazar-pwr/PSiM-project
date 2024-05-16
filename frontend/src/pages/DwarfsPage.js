// Autorzy: Jonasz Lazar, Kacper Malinowski

// Komponent DwarfsPage wyświetla listę wszystkich krasnali.
// Wykorzystuje kontekst AuthContext do uzyskania informacji o aktualnie zalogowanym użytkowniku.
// Wykorzystuje hook useEffect do pobrania danych o krasnalach z serwera po załadowaniu komponentu.
// Użytkownik może wyszukać krasnala wpisując jego nazwę w polu wyszukiwania.
// Jeżeli krasnal jest odblokowany dla użytkownika, obok nazwy krasnala wyświetla się informacja "zdobyty".
// Jeżeli użytkownik nie jest zalogowany, wyświetla tylko listę krasnali bez informacji o ich zdobyciu.

import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import Layout from '../components/Layout';

const DwarfsPage = () => {
    const { user } = useAuth();
    const [dwarfs, setDwarfs] = useState([]);
    const [totalDwarfs, setTotalDwarfs] = useState(0);
    const [userDwarfsCount, setUserDwarfsCount] = useState(0);
    const [searchQuery, setSearchQuery] = useState('');

    const apiUrl = process.env.REACT_APP_API_URL;

    useEffect(() => {
        const fetchDwarfs = async () => {
            try {
                const authTokens = JSON.parse(localStorage.getItem('authTokens'));
                const config = authTokens ? {
                    headers: {
                        'Authorization': `Bearer ${authTokens.access}`
                    }
                } : {};
                const response = await axios.get(`${apiUrl}dwarfs/?q=${searchQuery}`, config);
                setDwarfs(response.data.dwarfs);
                setTotalDwarfs(response.data.total_dwarfs);
                setUserDwarfsCount(response.data.user_dwarfs_count);
            } catch (error) {
                console.error(error);
            }
        };

        fetchDwarfs();
    }, [searchQuery, apiUrl]);

    return (
        <Layout>
            <div className="container mt-4">
                <h1 className="mb-3">Lista krasnali</h1>
                {user && <p>Zdobyto {userDwarfsCount}/{totalDwarfs} krasnali</p>}
                <form method="get">
                    <div className="input-group mb-3">
                        <label>
                            <input type="text" className="form-control" placeholder="Wyszukaj krasnala" name="q" value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} />
                        </label>
                    </div>
                </form>
                <ul className="list-group">
                    {dwarfs.map((dwarf) => (
                        <li className="list-group-item" key={dwarf.id}>
                            <a href={`/dwarfs/${dwarf.id}`}>{dwarf.name}</a>
                            {dwarf && dwarf.is_unlocked && <span> - zdobyty</span>}
                        </li>
                    ))}
                    {dwarfs.length === 0 && <p>Brak krasnali.</p>}
                </ul>
            </div>
        </Layout>
    );
};

export default DwarfsPage;