// Autorzy: Jonasz Lazar, Kacper Malinowski

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

const QrCodePage = () => {
    const { id } = useParams();
    const [qrCode, setQrCode] = useState(null);

    const apiUrl = process.env.REACT_APP_API_URL;

    useEffect(() => {
        const fetchQrCode = async () => {
            try {
                const authTokens = JSON.parse(localStorage.getItem('authTokens'));
                const config = authTokens ? {
                    headers: {
                        'Authorization': `Bearer ${authTokens.access}`
                    }
                } : {};
                const response = await axios.get(`${apiUrl}dwarfs/${id}/qr_code/`, config);
                setQrCode(response.data.qr_code);
            } catch (error) {
                console.error(error);
            }
        };

        fetchQrCode();
    }, [id, apiUrl]);

    return (
        <div>
            {qrCode ? (
                <img src={`data:image/png;base64,${qrCode}`} alt="QR Code" />
            ) : (
                <p>Loading...</p>
            )}
        </div>
    );
};

export default QrCodePage;