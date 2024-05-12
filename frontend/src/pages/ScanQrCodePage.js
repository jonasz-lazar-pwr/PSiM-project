// Autorzy: Jonasz Lazar, Kacper Malinowski

import React, { useEffect, useRef } from 'react';
import axios from 'axios';
import { Html5QrcodeScanner } from 'html5-qrcode';
import Layout from '../components/Layout';

const ScanQrCodePage = () => {
    const scannerRef = useRef(null);
    const apiUrl = process.env.REACT_APP_API_URL;

    useEffect(() => {
        const scanner = new Html5QrcodeScanner(
            scannerRef.current.id,
            { fps: 10, qrbox: { width: 250, height: 250 } },
            false
        );

        const onSuccess = async (decodedText) => {
            try {
                const authTokens = JSON.parse(localStorage.getItem('authTokens'));
                const config = authTokens ? {
                    headers: {
                        'Authorization': `Bearer ${authTokens.access}`
                    }
                } : {};
                const response = await axios.post(`${apiUrl}verify_qr_code/`, { qr_code: decodedText }, config);
                if (response.data.success) {
                    // Przetwarzanie URL z serwera na URL dla aplikacji React
                    const url = response.data.url;
                    window.location.href = url;
                } else {
                    alert(response.data.message);
                    if (response.data.url) {
                        const url = response.data.url;
                        window.location.href = url;
                    }
                }
            } catch (error) {
                console.error(error);
            }
        };

        const onError = (error) => {
            console.error(error);
        };

        scanner.render(onSuccess, onError);
    }, [apiUrl]);

    return (
        <Layout>
            <div className="container mt-4">
                <h1 className="mb-3">Skanuj kod QR</h1>
                <div className="row justify-content-center">
                     <div className="col-md-6">
                        <div className="d-flex justify-content-center align-items-center mt-5" style={{ height: 'auto' }}>
                            <div id="reader" ref={scannerRef} style={{ width: '100%', height: 'auto' }}></div>
                        </div>
                    </div>
                </div>
            </div>
        </Layout>
    );
};

export default ScanQrCodePage;