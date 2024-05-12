// Autorzy: Jonasz Lazar, Kacper Malinowski

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Layout from '../components/Layout';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const Achievements = () => {
    const [userAchievements, setUserAchievements] = useState([]);
    const [achievementsToGain, setAchievementsToGain] = useState([]);
    const { user } = useAuth();
    const navigate = useNavigate();

    const apiUrl = process.env.REACT_APP_API_URL;

    useEffect(() => {
        if (!user) {
            navigate("/login");
        } else {
            const fetchUserAchievements = async () => {
                try {
                    const authTokens = JSON.parse(localStorage.getItem('authTokens'));
                    const config = authTokens ? {
                        headers: {
                            'Authorization': `Bearer ${authTokens.access}`
                        }
                    } : {};
                    const response = await axios.get(`${apiUrl}user_achievements/`, config);
                    setUserAchievements(response.data);
                } catch (error) {
                    console.error(error);
                }
            };

            const fetchAchievementsToGain = async () => {
                try {
                    const authTokens = JSON.parse(localStorage.getItem('authTokens'));
                    const config = authTokens ? {
                        headers: {
                            'Authorization': `Bearer ${authTokens.access}`
                        }
                    } : {};
                    const response = await axios.get(`${apiUrl}achievements_to_gain/`, config);
                    setAchievementsToGain(response.data);
                } catch (error) {
                    console.error(error);
                }
            };

            fetchUserAchievements();
            fetchAchievementsToGain();
        }
    }, [user, navigate, apiUrl]);

    return (
        <Layout>
            <div className="container mt-4">
                <h1 className="mb-3">Moje osiągnięcia</h1>
                <div className="row bg-light text-dark p-2 mb-2">
                    <div className="col-md-3"><strong>Nazwa</strong></div>
                    <div className="col-md-3"><strong>Opis</strong></div>
                    <div className="col-md-3"><strong>Odznaka</strong></div>
                    <div className="col-md-3"><strong>Data zdobycia</strong></div>
                </div>
                <ul className="list-group">
                    {userAchievements.map((achievement, index) => (
                        <li className="list-group-item" key={index}>
                            <div className="row">
                                <div className="col-md-3">{achievement.achievement.name}</div>
                                <div className="col-md-3">{achievement.achievement.description}</div>
                                <div className="col-md-3">
                                    <img src={achievement.achievement.badge_icon} alt="Odznaka"
                                         style={{width: '30px', maxHeight: '30px'}}/>
                                </div>
                                <div
                                    className="col-md-3">{new Date(achievement.achievement_date).toLocaleDateString()}</div>
                            </div>
                        </li>
                    ))}
                    {userAchievements.length === 0 && <p className="list-group-item">Brak osiągnięć.</p>}
                </ul>
                <h1 className="mb-3 mt-4">Do zdobycia</h1>
                <div className="row bg-light text-dark p-2 mb-2">
                    <div className="col-md-3"><strong>Nazwa</strong></div>
                    <div className="col-md-3"><strong>Opis</strong></div>
                    <div className="col-md-6"><strong>Odznaka</strong></div>
                </div>
                <ul className="list-group">
                    {achievementsToGain.map((achievement, index) => (
                        <li className="list-group-item" key={index}>
                            <div className="row">
                                <div className="col-md-3">{achievement.name}</div>
                                <div className="col-md-3">{achievement.description}</div>
                                <div className="col-md-6">
                                    <img src={achievement.badge_icon} alt="Odznaka"
                                         style={{width: '30px', maxHeight: '30px'}}/>
                                </div>
                            </div>
                        </li>
                    ))}
                    {achievementsToGain.length === 0 && <p className="list-group-item">Brak osiągnięć.</p>}
                </ul>
            </div>
        </Layout>
    );
};

export default Achievements;