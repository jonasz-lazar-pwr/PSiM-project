// Autorzy: Jonasz Lazar, Kacper Malinowski

// Plik AuthContext.js definiuje kontekst autoryzacji, który jest używany do zarządzania stanem autoryzacji użytkownika w aplikacji.
// Kontekst ten zawiera informacje o aktualnie zalogowanym użytkowniku i tokenach autoryzacji, a także funkcje do logowania, rejestracji i wylogowywania użytkownika.
// Kontekst korzysta z hooka useEffect do pobrania pełnych informacji o użytkowniku z serwera po każdej zmianie tokenów autoryzacji.
// Jeżeli tokeny autoryzacji są przechowywane w pamięci lokalnej przeglądarki, są one używane do ustawienia początkowego stanu kontekstu.

import React, { createContext, useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import axios from 'axios';

const AuthContext = createContext();

export const useAuth = () => {
    return useContext(AuthContext);
};

export const AuthProvider = ({ children }) => {

    const navigate = useNavigate();

    const storedTokens = localStorage.getItem("authTokens");
    const [authTokens, setAuthTokens] = useState(() => storedTokens ? JSON.parse(storedTokens) : null);
    const [user, setUser] = useState(() => storedTokens ? jwtDecode(JSON.parse(storedTokens).access) : null);

    const apiUrl = process.env.REACT_APP_API_URL;

    const registerUser = async (username, password, password2) => {
        try {
            const response = await axios.post(`${apiUrl}register/`, { username, password, password2 });
            const data = response.data;
            setAuthTokens({access: data.access, refresh: data.refresh});
            localStorage.setItem("authTokens", JSON.stringify({access: data.access, refresh: data.refresh}));

            // Pobieranie danych użytkownika
            const userResponse = await axios.get(`${apiUrl}user/`, {
                headers: {
                    'Authorization': `Bearer ${data.access}`
                }
            });
            setUser(userResponse.data); // Zapisanie danych użytkownika

            navigate("/");
            return null;
        } catch (error) {
            console.error(error);
            return 'Podano nieprawidłowe dane rejestracji. Spróbuj ponownie.';
        }
    };

    const loginUser = async (username, password) => {
        try {
            const response = await axios.post(`${apiUrl}token/`, { username, password });
            const data = response.data;
            setAuthTokens(data);
            localStorage.setItem("authTokens", JSON.stringify(data));

            // Pobieranie danych użytkownika
            const userResponse = await axios.get(`${apiUrl}user/`, {
                headers: {
                    'Authorization': `Bearer ${data.access}`
                }
            });
            setUser(userResponse.data); // Zapisanie danych użytkownika

            navigate("/");
            return null;
        } catch (error) {
            console.error(error);
            return 'Podano nieprawidłowe dane logowania. Spróbuj ponownie.';
        }
    };

    const logoutUser = async () => {
        try {
            // Wysyłanie żądania do punktu końcowego wylogowania na serwerze
            await axios.post(`${apiUrl}logout/`, {
                refresh_token: authTokens.refresh,
            }, {
                headers: {
                    'Authorization': `Bearer ${authTokens.access}`
                }
            });

            // Usuwanie tokenów z pamięci lokalnej
            setAuthTokens(null);
            setUser(null);
            localStorage.removeItem("authTokens");
            navigate("/login");
        } catch (error) {
            console.error(error);
            alert("Logout failed");
        }
    };

    const contextData = {
        user: user,
        setUser: setUser,
        authTokens: authTokens,
        setAuthTokens: setAuthTokens,
        loginUser: loginUser,
        registerUser: registerUser,
        logoutUser: logoutUser,
    };

    useEffect(() => {
        if (authTokens) {
            setUser(jwtDecode(authTokens.access));

            // Pobieranie pełnych informacji o użytkowniku z serwera
            const fetchUser = async () => {
                try {
                    const response = await axios.get(`${apiUrl}user/`, {
                        headers: {
                            'Authorization': `Bearer ${authTokens.access}`
                        }
                    });
                    setUser(response.data);
                } catch (error) {
                    console.error(error);
                }
            };

            fetchUser();
        }
    }, [authTokens, apiUrl]);

    return <AuthContext.Provider value={contextData}>
        {children}
    </AuthContext.Provider>;
};

export default AuthContext;