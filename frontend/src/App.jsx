import { useState } from 'react';
import axios from 'axios';
import { Dna, Search, CheckCircle, AlertTriangle, Loader2, ExternalLink } from 'lucide-react';
import './App.css';

function App() {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleExtract = async () => {
    if (!text) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const response = await axios.post('http://127.0.0.1:8001/api/samples/extract', { text });
      setResult(response.data);
    } catch (err) {
      setError('خطا در ارتباط با سرور. لطفا مطمئن شوید سرویس FastAPI روشن است.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <header>
        <div className="logo"><Dna size={32} /></div>
        <h1>BioSample AI Gateway</h1>
        <p>دروازه هوشمند نمونه‌های زیستی با MCP و LLM</p>
      </header>

      <main>
        <div className="input-section">
          <textarea
            placeholder="متن خود را وارد کنید... مثلا: biopsy of human liver from London in 2023, patient with cirrhosis"
            value={text}
            onChange={(e) => setText(e.target.value)}
            rows={4}
          />
          <button onClick={handleExtract} disabled={loading || !text}>
            {loading ? <Loader2 className="spin" size={20} /> : <Search size={20} />}
            {loading ? 'در حال استخراج...' : 'استخراج اطلاعات'}
          </button>
        </div>

        {error && <div className="error"><AlertTriangle size={20} /> {error}</div>}

        {result && result.sample && (
          <div className="result-section">
            <h2><CheckCircle size={24} color="#10b981" /> نتیجه استخراج</h2>
            
            {/* نمایش لینک BioSamples */}
            {result.ebi && result.ebi.accession && (
              <div style={{ marginBottom: '1rem', padding: '1rem', background: '#0f172a', borderRadius: '8px', border: '1px solid #334155', display: 'flex', alignItems: 'center', gap: '10px' }}>
                <span style={{ color: '#94a3b8' }}>شناسه BioSamples (EBI):</span>
                <a 
                  href={`https://www.ebi.ac.uk/biosamples/samples/${result.ebi.accession}`} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  style={{ color: '#60a5fa', textDecoration: 'underline', fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: '5px' }}
                >
                  {result.ebi.accession} <ExternalLink size={16} />
                </a>
              </div>
            )}

            <div className="data-grid">
              {Object.entries(result.sample).map(([key, value]) => {
                if (key === 'additional_metadata' && value && Object.keys(value).length === 0) return null;
                return (
                  <div key={key} className="data-item">
                    <span className="label">{key}</span>
                    <span className="value">{value || 'نامشخص'}</span>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;