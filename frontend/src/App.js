// Autorzy: Jonasz Lazar, Kacper Malinowski

// Główny plik aplikacji React. Definiuje routing (ścieżki URL) dla całej aplikacji.
// Każda ścieżka URL jest skojarzona z konkretnym komponentem, który jest renderowany, gdy użytkownik odwiedza daną ścieżkę.
// Autoryzacja użytkowników jest obsługiwana przez kontekst AuthProvider.

import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MainPage from './pages/MainPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from "./pages/RegisterPage";
import DwarfsPage from "./pages/DwarfsPage";
import DwarfDetailPage from "./pages/DwarfDetailPage";
import CommentDwarfPage from "./pages/CommentDwarfPage";
import ScanQrCodePage from "./pages/ScanQrCodePage";
import QrCodePage from "./pages/QrCodePage";
import RankingPage from "./pages/RankingPage";
import CommentsPage from "./pages/CommentsPage";
import AchievementsPage from "./pages/AchievementsPage";
import { AuthProvider } from './context/AuthContext';

const App = () => {
    return (
        <Router>
            <AuthProvider>
                <Routes>
                    <Route path="/" element={<MainPage />} />
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/register" element={<RegisterPage />} />
                    <Route path="/dwarfs" element={<DwarfsPage />} />
                    <Route path="/dwarfs/:id" element={<DwarfDetailPage />} />
                    <Route path="/dwarfs/:id/comment" element={<CommentDwarfPage />} />
                    <Route path="/dwarfs/:id/qr_code" element={<QrCodePage />} />
                    <Route path="/verify_qr_code" element={<ScanQrCodePage />} />
                    <Route path="/users_ranking" element={<RankingPage />} />
                    <Route path="/user_comments" element={<CommentsPage />} />
                    <Route path="/user_achievements" element={<AchievementsPage />} />
                </Routes>
            </AuthProvider>
        </Router>
    );
};

export default App;