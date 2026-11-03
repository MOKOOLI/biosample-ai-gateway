import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'

// این بخش برای پیدا کردن خطا اضافه شده
window.onerror = function(message, source, lineno, colno, error) {
  document.body.innerHTML = `<div style="color: red; padding: 20px; font-family: monospace; background: white; z-index: 9999; position: absolute; top: 0; left: 0; width: 100%; height: 100%;">
    <h2>خطای React پیدا شد:</h2>
    <p><strong>پیام:</strong> ${message}</p>
    <p><strong>فایل:</strong> ${source} (خط ${lineno})</p>
    <p><strong>جزئیات:</strong> ${error ? error.stack : 'ندارد'}</p>
  </div>`;
};

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)