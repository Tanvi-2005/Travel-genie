import { useState, useEffect } from 'react'

const translations = {
  English: {
    home: '🏠 Home', plan: '🗺️ Plan Trip', history: '📋 History',
    brand: 'Travel Genie', heroTitle1: 'Your Personal', heroTitle2: 'AI Travel Planner',
    heroDesc: 'Let Travel Genie craft the perfect trip for you. AI-powered itineraries, smart destination recommendations, and data-driven insights — all in one place.',
    startBtn: '✨ Start Planning',
    planHeader: '🗺️ Plan Your Trip', planSub: 'Fill in your preferences and let AI create your perfect itinerary',
    formName: 'Your Name', formDest: 'Destination', formBudget: 'Budget (₹)', formPeople: 'Number of People',
    formStartDate: 'Start Date', formEndDate: 'End Date', formStyle: 'Travel Style',
    formInterests: 'Interests & Preferences', formInterestsPlaceholder: 'Photography, local food, hiking, temples, adventure...',
    destPlaceholder: 'Goa, Manali, Kerala, Rajasthan...',
    namePlaceholder: 'Rahul Sharma',
    genBtn: '✨ Generate Itinerary', genLoading: '🔄 Generating...',
    adv: '🏔️ Adventure', rel: '🏖️ Relaxation', cul: '🏛️ Cultural', fam: '👨‍👩‍👧‍👦 Family',
    tripDetails: 'Trip Details', tripSub: 'Tell us about your dream trip',
    aiCrafting: '🤖 AI is crafting your perfect itinerary...',
    emptyPlan: 'Fill in your trip details and click "Generate Itinerary" to get started!',
    emptyHist: 'No trips planned yet. Go to "Plan Trip" to create your first itinerary!',
    feedbackTitle: 'How was your itinerary?',
    feedbackSub: 'Rate your experience to help us improve.',
    feedbackThanks: 'Thank you for your feedback! ✨',
  },
  Hindi: {
    home: '🏠 होम', plan: '🗺️ ट्रिप प्लान करें', history: '📋 इतिहास',
    brand: 'ट्रेवल जिन्न', heroTitle1: 'आपका व्यक्तिगत', heroTitle2: 'AI यात्रा योजनाकार',
    heroDesc: 'ट्रैवल जिन्न को आपके लिए परफेक्ट ट्रिप तैयार करने दें। AI-सं संचालित कार्यक्रम, स्मार्ट गंतव्य सिफारिशें और डेटा-संचालित अंतर्दृष्टि - सब एक जगह पर।',
    startBtn: '✨ योजना शुरू करें',
    planHeader: '🗺️ अपनी यात्रा की योजना बनाएं', planSub: 'अपनी प्राथमिकताएं भरें और AI को आपका आदर्श कार्यक्रम बनाने दें',
    formName: 'आपका नाम', formDest: 'गंतव्य', formBudget: 'बजट (₹)', formPeople: 'लोगों की संख्या',
    formStartDate: 'प्रारंभ तिथि', formEndDate: 'अंतिम तिथि', formStyle: 'यात्रा शैली',
    formInterests: 'रुचि और प्राथमिकताएं', formInterestsPlaceholder: 'फोटोग्राफी, स्थानीय भोजन, पहाड़ी यात्राएं, मंदिर...',
    destPlaceholder: 'गोवा, मनाली, केरल, राजस्थान...',
    namePlaceholder: 'राहुल शर्मा',
    genBtn: '✨ इटिनरेरी जनरेट करें', genLoading: '🔄 जनरेट हो रहा है...',
    adv: '🏔️ साहसिक (Adventure)', rel: '🏖️ विश्राम (Relaxation)', cul: '🏛️ सांस्कृतिक (Cultural)', fam: '👨‍👩‍👧‍👦 परिवार (Family)',
    tripDetails: 'यात्रा विवरण', tripSub: 'हमें अपने सपनो की यात्रा के बारे में बताएं',
    aiCrafting: '🤖 AI आपका आदर्श कार्यक्रम तैयार कर रहा है...',
    emptyPlan: 'अपना यात्रा विवरण भरें और शुरू करने के लिए "इटिनरेरी जनरेट करें" पर क्लिक करें!',
    emptyHist: 'अभी कोई यात्रा योजना नहीं है। अपना पहला कार्यक्रम बनाने के लिए "ट्रिप प्लान करें" पर जाएं!',
    feedbackTitle: 'आपका कार्यक्रम कैसा था?',
    feedbackSub: 'हमें बेहतर बनाने में मदद करने के लिए अपने अनुभव को रेट करें।',
    feedbackThanks: 'आपकी प्रतिक्रिया के लिए धन्यवाद! ✨',
  },
  Punjabi: {
    home: '🏠 ਘਰ', plan: '🗺️ ਯਾਤਰਾ ਦੀ ਯੋਜਨਾ', history: '📋 ਇਤਿਹਾਸ',
    brand: 'ਟਰੈਵਲ ਜਿੰਨੀ', heroTitle1: 'ਤੁਹਾਡਾ ਨਿੱਜੀ', heroTitle2: 'AI ਟਰੈਵਲ ਪਲਾਨਰ',
    heroDesc: 'ਟਰੈਵਲ ਜਿੰਨੀ ਨੂੰ ਤੁਹਾਡੇ ਲਈ ਸਹੀ ਯਾਤਰਾ ਤਿਆਰ ਕਰਨ ਦਿਓ। AI ਦੁਆਰਾ ਸੰਚਾਲਿਤ ਪ੍ਰੋਗਰਾਮ, ਸਮਾਰਟ ਮੰਜ਼ਿਲ ਦੀਆਂ ਸਿਫ਼ਾਰਸ਼ਾਂ, ਅਤੇ ਡੇਟਾ-ਸੰਚਾਲਿਤ ਸੂਝ — ਸਭ ਇੱਕ ਥਾਂ ’ਤੇ।',
    startBtn: '✨ ਯੋਜਨਾ ਸ਼ੁਰੂ ਕਰੋ',
    planHeader: '🗺️ ਆਪਣੀ ਯਾਤਰਾ ਦੀ ਯੋਜਨਾ ਬਣਾਓ', planSub: 'ਆਪਣੀਆਂ ਤਰਜੀਹਾਂ ਭਰੋ ਅਤੇ AI ਨੂੰ ਆਪਣਾ ਆਦਰਸ਼ ਪ੍ਰੋਗਰਾਮ ਬਣਾਉਣ ਦਿਓ',
    formName: 'ਤੁਹਾਡਾ ਨਾਮ', formDest: 'ਮੰਜ਼ਿਲ', formBudget: 'ਬਜਟ (₹)', formPeople: 'ਲੋਕਾਂ ਦੀ ਗਿਣਤੀ',
    formStartDate: 'ਸ਼ੁਰੂਆਤੀ ਮਿਤੀ', formEndDate: 'ਸਮਾਪਤੀ ਮਿਤੀ', formStyle: 'ਯਾਤਰਾ ਸ਼ੈਲੀ',
    formInterests: 'ਦਿਲਚਸਪੀ ਅਤੇ ਤਰਜੀਹਾਂ', formInterestsPlaceholder: 'ਫੋਟੋਗ੍ਰਾਫੀ, ਸਥਾਨਕ ਭੋਜਨ, ਹਾਈਕਿੰਗ, ਮੰਦਰ...',
    destPlaceholder: 'ਗੋਆ, ਮਨਾਲੀ, ਕੇਰਲਾ, ਰਾਜਸਥਾਨ...',
    namePlaceholder: 'ਰਾਹੁਲ ਸ਼ਰਮਾ',
    genBtn: '✨ ਇਟਿਨਰਰੀ ਜਨਰੇਟ ਕਰੋ', genLoading: '🔄 ਜਨਰੇਟ ਹੋ ਰਿਹਾ ਹੈ...',
    adv: '🏔️ ਐਡਵੈਂਚਰ (Adventure)', rel: '🏖️ ਆਰਾਮ (Relaxation)', cul: '🏛️ ਸੱਭਿਆਚਾਰਕ (Cultural)', fam: '👨‍👩‍👧‍👦 ਪਰਿਵਾਰ (Family)',
    tripDetails: 'ਯਾਤਰਾ ਦੇ ਵੇਰਵੇ', tripSub: 'ਸਾਨੂੰ ਆਪਣੀ ਸੁਪਨਿਆਂ ਦੀ ਯਾਤਰਾ ਬਾਰੇ ਦੱਸੋ',
    aiCrafting: '🤖 AI ਤੁਹਾਡਾ ਆਦਰਸ਼ ਪ੍ਰੋਗਰਾਮ ਬਣਾ ਰਿਹਾ ਹੈ...',
    emptyPlan: 'ਆਪਣੇ ਯਾਤਰਾ ਦੇ ਵੇਰਵੇ ਭਰੋ ਅਤੇ ਸ਼ੁਰੂ ਕਰਨ ਲਈ "ਇਟਿਨਰਰੀ ਜਨਰੇਟ ਕਰੋ" ਤੇ ਕਲਿਕ ਕਰੋ!',
    emptyHist: 'ਅਜੇ ਕੋਈ ਯਾਤਰਾ ਯੋਜਨਾ ਨਹੀਂ ਹੈ। ਆਪਣਾ ਪਹਿਲਾ ਪ੍ਰੋਗਰਾਮ ਬਣਾਉਣ ਲਈ "ਯਾਤਰਾ ਦੀ ਯੋਜਨਾ" ਤੇ ਜਾਓ!',
    feedbackTitle: 'ਤੁਹਾਡਾ ਪ੍ਰੋਗਰਾਮ ਕਿਵੇਂ ਰਿਹਾ?',
    feedbackSub: 'ਸਾਨੂੰ ਆਪਣੀ ਸੇਵਾ ਸੁਧਾਰਨ ਵਿੱਚ ਮਦਦ ਕਰਨ ਲਈ ਆਪਣੇ ਅਨੁਭਵ ਨੂੰ ਰੇਟ ਕਰੋ।',
    feedbackThanks: 'ਤੁਹਾਡੇ ਫੀਡਬੈਕ ਲਈ ਧੰਨਵਾਦ! ✨',
  },
  Kannada: {
    home: '🏠 ಮುಖಪುಟ', plan: '🗺️ ಪ್ರವಾಸ ಯೋಜನೆ', history: '📋 ಇತಿಹಾಸ',
    brand: 'ಟ್ರಾವೆಲ್ ಜಿನಿ', heroTitle1: 'ನಿಮ್ಮ ವೈಯಕ್ತಿಕ', heroTitle2: 'AI ಪ್ರವಾಸ ಮ್ಯಾಪ್',
    heroDesc: 'ಟ್ರಾವೆಲ್ ಜಿನಿ ನಿಮಗಾಗಿ ಪರಿಪೂರ್ಣ ಪ್ರವಾಸವನ್ನು ನಿರ್ಮಿಸಲಿ. AI-ಚಾಲಿತ ವೇಳಾಪಟ್ಟಿಗಳು, ಗಮ್ಯಸ್ಥಾನ ಶಿಫಾರಸುಗಳು ಮತ್ತು ಡೇಟಾ ಒಳನೋಟಗಳು - ಎಲ್ಲವೂ ಒಂದೇ ಸ್ಥಳದಲ್ಲಿ.',
    startBtn: '✨ ಯೋಜನೆ ಪ್ರಾರಂಭಿಸಿ',
    planHeader: '🗺️ ನಿಮ್ಮ ಪ್ರವಾಸದ ಯೋಜನೆ ಮಾಡಿ', planSub: 'ನಿಮ್ಮ ಆದ್ಯತೆಗಳನ್ನು ಭರ್ತಿ ಮಾಡಿ ಮತ್ತು AI ನಿಮ್ಮ ಪರಿಪೂರ್ಣ ವೇಳಾಪಟ್ಟಿಯನ್ನು ರಚಿಸಲಿ',
    formName: 'ನಿಮ್ಮ ಹೆಸರು', formDest: 'ಗಮ್ಯಸ್ಥಾನ', formBudget: 'ಬಜೆಟ್ (₹)', formPeople: 'ಜನರ ಸಂಖ್ಯೆ',
    formStartDate: 'ಪ್ರಾರಂಭ ದಿನಾಂಕ', formEndDate: 'ಅಂತ್ಯ ದಿನಾಂಕ', formStyle: 'ಪ್ರವಾಸದ ಶೈಲಿ',
    formInterests: 'ಆಸಕ್ತಿಗಳು ಮತ್ತು ಆದ್ಯತೆಗಳು', formInterestsPlaceholder: 'ಛಾಯಾಗ್ರಹಣ, ಸ್ಥಳೀಯ ಆಹಾರ, ಚಾರಣ, ದೇವಾಲಯ...',
    destPlaceholder: 'ಗೋವಾ, ಮನಾಲಿ, ಕೇರಳ, ರಾಜಸ್ಥಾನ...',
    namePlaceholder: 'ರಾಹುಲ್ ಶರ್ಮಾ',
    genBtn: '✨ ವೇಳಾಪಟ್ಟಿ ರಚಿಸಿ', genLoading: '🔄 ರಚಿಸಲಾಗುತ್ತಿದೆ...',
    adv: '🏔️ ಸಾಹಸ (Adventure)', rel: '🏖️ ವಿಶ್ರಾಂತಿ (Relaxation)', cul: '🏛️ ಸಾಂಸ್ಕೃತಿಕ (Cultural)', fam: '👨‍👩‍👧‍👦 ಕುಟುಂಬ (Family)',
    tripDetails: 'ಪ್ರವಾಸದ ವಿವರಗಳು', tripSub: 'ನಿಮ್ಮ ಕನಸಿನ ಪ್ರವಾಸದ ಬಗ್ಗೆ ನಮಗೆ ತಿಳಿಸಿ',
    aiCrafting: '🤖 AI ನಿಮ್ಮ ಪರಿಪೂರ್ಣ ವೇಳಾಪಟ್ಟಿಯನ್ನು ರಚಿಸುತ್ತಿದೆ...',
    emptyPlan: 'ಪ್ರಾರಂಭಿಸಲು ನಿಮ್ಮ ಪ್ರವಾಸದ ವಿವರಗಳನ್ನು ಭರ್ತಿ ಮಾಡಿ ಮತ್ತು "ವೇಳಾಪಟ್ಟಿ ರಚಿಸಿ" ಕ್ಲಿಕ್ ಮಾಡಿ!',
    emptyHist: 'ಇನ್ನೂ ಯಾವ ಪ್ರವಾಸವನ್ನೂ ಯೋಜಿಸಿಲ್ಲ. ನಿಮ್ಮ ಮೊದಲ ವೇಳಾಪಟ್ಟಿ ರಚಿಸಲು "ಪ್ರವಾಸ ಯೋಜನೆ" ಗೆ ಹೋಗಿ!',
    feedbackTitle: 'ನಿಮ್ಮ ವೇಳಾಪಟ್ಟಿ ಹೇಗಿತ್ತು?',
    feedbackSub: 'ನಮ್ಮನ್ನು ಸುಧಾರಿಸಲು ಸಹಾಯ ಮಾಡಲು ನಿಮ್ಮ ಅನುಭವವನ್ನು ರೇಟ್ ಮಾಡಿ.',
    feedbackThanks: 'ಪ್ರತಿಕ್ರಿಯೆಗಾಗಿ ಧನ್ಯವಾದಗಳು! ✨',
  }
}


// Check if running on localhost or 127.0.0.1 for local testing
const API_BASE = (window.location.origin.includes('localhost') || window.location.origin.includes('127.0.0.1'))
  ? 'http://localhost:8000'
  : 'https://travel-genie.onrender.com'; // 👈 YOUR ACTUAL RENDER BACKEND URL


/* ═══════════════════════════════════════════════════════
   Travel Genie AI — Main Application
   ═══════════════════════════════════════════════════════ */
export default function App() {
  const [page, setPage] = useState('home')
  const [language, setLanguage] = useState('English')

  const t = translations[language]

  return (
    <>
      <Navbar page={page} setPage={setPage} language={language} setLanguage={setLanguage} t={t} />
      {page === 'home' && <HomePage setPage={setPage} t={t} />}
      {page === 'plan' && <PlanPage language={language} setLanguage={setLanguage} t={t} />}
      {page === 'history' && <HistoryPage t={t} />}
    </>
  )
}

/* ─── Navbar ─────────────────────────────────────────── */
function Navbar({ page, setPage, language, setLanguage, t }) {
  return (
    <nav className="navbar">
      <div className="navbar-brand" onClick={() => setPage('home')}>
        <span className="logo-icon">✈️</span>
        <span>{t.brand}</span>
      </div>
      <div className="navbar-links">
        {[
          { key: 'home', label: t.home },
          { key: 'plan', label: t.plan },
          { key: 'history', label: t.history },
        ].map(item => (
          <button
            key={item.key}
            className={`nav-link ${page === item.key ? 'active' : ''}`}
            onClick={() => setPage(item.key)}
          >
            {item.label}
          </button>
        ))}
      </div>
    </nav>
  )
}

/* ─── Home Page ──────────────────────────────────────── */
function HomePage({ setPage, t }) {
  return (
    <>
      <section className="hero">
        <div className="hero-float">🌍</div>
        <div className="hero-float">🏝️</div>
        <div className="hero-float">🏔️</div>
        <div className="hero-float">🌊</div>

        <div className="hero-badge">✨ Powered by Gemini AI & Machine Learning</div>

        <h1>
          {t.heroTitle1}<br />
          <span className="highlight">{t.heroTitle2}</span>
        </h1>

        <p>
          {t.heroDesc}
        </p>

        <div className="hero-actions">
          <button className="btn btn-primary" onClick={() => setPage('plan')}>
            {t.startBtn}
          </button>
        </div>


      </section>

      <section className="features-section">
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">🤖</div>
            <div className="feature-title">Gemini AI Itineraries</div>
            <div className="feature-desc">
              Get detailed day-by-day travel plans generated by Google's Gemini AI,
              tailored to your preferences and budget.
            </div>
          </div>
          <div className="feature-card">
            <div className="feature-icon">📈</div>
            <div className="feature-title">ML-Powered Recommendations</div>
            <div className="feature-desc">
              Our machine learning models analyze thousands of travel patterns
              to suggest the perfect destination category for you.
            </div>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🗄️</div>
            <div className="feature-title">Smart Data Storage</div>
            <div className="feature-desc">
              Every trip plan is stored securely in our database. Review,
              compare, and learn from your past adventures.
            </div>
          </div>
        </div>
      </section>
    </>
  )
}

/* ─── Plan Trip Page ─────────────────────────────────── */
function PlanPage({ language, setLanguage, t }) {
  const [form, setForm] = useState({
    user_name: '',
    destination: '',
    budget: '',
    start_date: '',
    end_date: '',
    travel_style: 'adventure',
    interests: '',
    people: 1,
  })
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [weather, setWeather] = useState(null)
  const [error, setError] = useState('')
  const [rating, setRating] = useState(0)
  const [hoverRating, setHoverRating] = useState(0)
  const [feedbackSubmitted, setFeedbackSubmitted] = useState(false)

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleDestBlur = async () => {
    if (!form.destination) return;
    try {
      const res = await fetch(`${API_BASE}/weather?destination=${encodeURIComponent(form.destination)}`);
      if (res.ok) {
        setWeather(await res.json());
      }
    } catch (err) {
      console.error("Weather fetch failed", err);
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setResult(null)
    setFeedbackSubmitted(false)
    setRating(0)


    try {
      const res = await fetch(`${API_BASE}/plan-trip`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...form,
          budget: parseFloat(form.budget),
          people: parseInt(form.people, 10) || 1,
          language: language
        }),
      })

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.error || `Server responded with status ${res.status}`);
      }
      const data = await res.json()
      setResult(data)

    } catch (err) {
      setError(`${err.message} (Tried reaching: ${API_BASE})`)
    } finally {
      setLoading(false)
    }
  }

  const submitFeedback = async (score) => {
    if (!result?.id) return
    setRating(score)
    try {
      const res = await fetch(`${API_BASE}/trips/${result.id}/feedback?satisfaction_score=${score}`, {
        method: 'POST'
      })
      if (res.ok) {
        setFeedbackSubmitted(true)
      }
    } catch (err) {
      console.error('Feedback submission failed', err)
    }
  }


  return (
    <div className="page">
      <div className="page-header">
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginBottom: '1rem' }}>
          <h1>{t.planHeader}</h1>
          <p>{t.planSub}</p>
          <div style={{ marginTop: '1rem', padding: '0.5rem 1rem', background: 'white', borderRadius: '12px', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)', display: 'inline-flex', alignItems: 'center', gap: '1rem' }}>
            <span style={{ fontWeight: 600, color: '#334155' }}>🌐 Select Language:</span>
            <select
              className="form-select"
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              style={{ width: 'auto', padding: '0.4rem', fontSize: '1rem', border: '1px solid #cbd5e1' }}
            >
              <option value="English">English</option>
              <option value="Hindi">हिंदी (Hindi)</option>
              <option value="Punjabi">ਪੰਜਾਬੀ (Punjabi)</option>
              <option value="Kannada">ಕನ್ನಡ (Kannada)</option>
            </select>
          </div>
        </div>
      </div>

      <div className="planning-container">
        <div className="card form-card">
          <div className="card-header">
            <div className="card-icon">✈️</div>
            <div>
              <div className="card-title">{t.tripDetails}</div>
              <div className="card-subtitle">{t.tripSub}</div>
            </div>
          </div>

          <form onSubmit={handleSubmit}>
            <div className="form-grid">
              <div className="form-group">
                <label className="form-label">{t.formDest}</label>
                <input
                  className="form-input"
                  name="destination"
                  value={form.destination}
                  onChange={handleChange}
                  onBlur={handleDestBlur}
                  placeholder={t.destPlaceholder}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">{t.formBudget}</label>
                <input
                  className="form-input"
                  name="budget"
                  type="number"
                  min="1000"
                  value={form.budget}
                  onChange={handleChange}
                  placeholder="50000"
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">{t.formStartDate}</label>
                <input
                  className="form-input"
                  name="start_date"
                  type="date"
                  value={form.start_date}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">{t.formEndDate}</label>
                <input
                  className="form-input"
                  name="end_date"
                  type="date"
                  value={form.end_date}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">{t.formPeople}</label>
                <input
                  className="form-input"
                  name="people"
                  type="number"
                  min="1"
                  value={form.people}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">{t.formStyle}</label>
                <select
                  className="form-select"
                  name="travel_style"
                  value={form.travel_style}
                  onChange={handleChange}
                >
                  <option value="adventure">{t.adv}</option>
                  <option value="relaxation">{t.rel}</option>
                  <option value="cultural">{t.cul}</option>
                  <option value="family">{t.fam}</option>
                </select>
              </div>

              <div className="form-group full-width">
                <label className="form-label">{t.formInterests}</label>
                <textarea
                  className="form-textarea"
                  name="interests"
                  value={form.interests}
                  onChange={handleChange}
                  placeholder={t.formInterestsPlaceholder}
                />
              </div>
            </div>

            <div style={{ marginTop: '1.5rem', display: 'flex', gap: '1rem' }}>
              <button
                type="submit"
                className="btn btn-primary"
                disabled={loading}
              >
                {loading ? t.genLoading : t.genBtn}
              </button>
            </div>
          </form>

          {error && (
            <div style={{ marginTop: '1rem', padding: '1rem', background: 'rgba(244,63,94,0.1)', border: '1px solid rgba(244,63,94,0.3)', borderRadius: '8px', color: '#f43f5e', fontSize: '0.9rem' }}>
              ❌ {error}
            </div>
          )}
        </div>

        <div>
          {weather && (
            <div style={{ marginBottom: '1.5rem', padding: '1.5rem', background: 'linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%)', color: 'white', borderRadius: '16px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', boxShadow: '0 10px 15px -3px rgba(14, 165, 233, 0.3)' }}>
              <div>
                <h3 style={{ margin: '0 0 0.8rem 0', fontSize: '1.4rem', fontWeight: '600' }}>Weather in {weather.city}</h3>
                <div style={{ display: 'flex', gap: '1.5rem', alignItems: 'center', fontSize: '1rem', flexWrap: 'wrap' }}>
                  <span style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', background: 'rgba(255,255,255,0.2)', padding: '0.3rem 0.8rem', borderRadius: '20px' }}>
                    🌡️ {Math.round(weather.temp)}°C
                  </span>
                  <span style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', textTransform: 'capitalize', background: 'rgba(255,255,255,0.2)', padding: '0.3rem 0.8rem', borderRadius: '20px' }}>
                    ☁️ {weather.description}
                  </span>
                  <span style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', background: 'rgba(255,255,255,0.2)', padding: '0.3rem 0.8rem', borderRadius: '20px' }}>
                    💧 Humidity: {weather.humidity}%
                  </span>
                  <span style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', background: 'rgba(255,255,255,0.2)', padding: '0.3rem 0.8rem', borderRadius: '20px' }}>
                    💨 Wind: {weather.wind_speed} m/s
                  </span>
                </div>
              </div>
              <img src={`http://openweathermap.org/img/wn/${weather.icon}@2x.png`} alt={weather.description} style={{ width: '80px', height: '80px', filter: 'drop-shadow(0px 4px 6px rgba(0,0,0,0.2))' }} />
            </div>
          )}

          {loading && (
            <div className="loading-container">
              <div className="spinner"></div>
              <div className="loading-text">
                {t.aiCrafting}
              </div>
            </div>
          )}

          {result && (
            <div className="itinerary-card" style={{ animation: 'fadeInUp 0.6s ease' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1.5rem', flexWrap: 'wrap' }}>
                <h2>📋 {result.destination}</h2>
                {result.ml_recommendation && (
                  <span className="ml-tag">🤖 AI: {result.ml_recommendation}</span>
                )}
              </div>
              <div style={{ fontSize: '0.85rem', color: '#64748b', marginBottom: '1rem' }}>
                Budget: <strong>₹{result.budget?.toLocaleString('en-IN')}</strong> | Trip #{result.id} | Language: {result.language || 'English'}
              </div>
              <div className="itinerary-content">
                <div dangerouslySetInnerHTML={{ __html: result.generated_itinerary.replace(/\n/g, '<br/>').replace(/\*\*(.*?)\*\*/g, '<b>$1</b>') }} />
              </div>

              {/* Feedback Section */}
              <div className="feedback-section" style={{ marginTop: '2rem', paddingTop: '1.5rem', borderTop: '2px dashed #e2e8f0', textAlign: 'center' }}>
                {feedbackSubmitted ? (
                  <div style={{ color: '#059669', fontWeight: '600', fontSize: '1.1rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem', padding: '1rem', background: '#ecfdf5', borderRadius: '12px' }}>
                    <span>{t.feedbackThanks}</span>
                  </div>
                ) : (
                  <>
                    <h3 style={{ fontSize: '1.2rem', marginBottom: '0.4rem', color: '#1e293b', fontWeight: '700' }}>{t.feedbackTitle}</h3>
                    <p style={{ fontSize: '0.95rem', color: '#64748b', marginBottom: '1.2rem' }}>{t.feedbackSub}</p>
                    <div style={{ display: 'flex', justifyContent: 'center', gap: '0.8rem' }}>
                      {[1, 2, 3, 4, 5].map((star) => (
                        <button
                          key={star}
                          onClick={() => submitFeedback(star)}
                          onMouseEnter={() => setHoverRating(star)}
                          onMouseLeave={() => setHoverRating(0)}
                          style={{
                            background: 'none',
                            border: 'none',
                            fontSize: '2.5rem',
                            cursor: 'pointer',
                            color: star <= (hoverRating || rating) ? '#fbbf24' : '#e2e8f0',
                            transition: 'all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275)',
                            transform: star <= hoverRating ? 'scale(1.2)' : 'scale(1)',
                            padding: '0',
                            outline: 'none'
                          }}
                        >
                          ★
                        </button>
                      ))}
                    </div>
                  </>
                )}
              </div>
            </div>
          )}

          {!loading && !result && !weather && (
            <div className="empty-state">
              <div className="empty-state-icon">🧳</div>
              <p>{t.emptyPlan}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

/* ─── History Page ───────────────────────────────────── */
function HistoryPage({ t }) {
  const [trips, setTrips] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedTrip, setSelectedTrip] = useState(null)
  const [toast, setToast] = useState('')
  const [performance, setPerformance] = useState([])

  useEffect(() => {
    fetchTrips()
    fetchPerformance()
  }, [])

  const fetchPerformance = async () => {
    try {
      const res = await fetch(`${API_BASE}/ml/user-performance`)
      if (res.ok) setPerformance(await res.json())
    } catch (err) {
      console.error('Failed to load performance:', err)
    }
  }

  const fetchTrips = async () => {
    setLoading(true)
    try {
      const res = await fetch(`${API_BASE}/trips`)
      if (res.ok) setTrips(await res.json())
    } catch (err) {
      console.error('Failed to load trips:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id, e) => {
    e.stopPropagation()
    try {
      const res = await fetch(`${API_BASE}/trips/${id}`, { method: 'DELETE' })
      if (res.ok) {
        setTrips(trips.filter(t => t.id !== id))
        if (selectedTrip?.id === id) setSelectedTrip(null)
        setToast('Trip deleted successfully!')
        setTimeout(() => setToast(''), 3000)
      }
    } catch (err) {
      console.error('Delete failed:', err)
    }
  }

  if (loading) {
    return (
      <div className="page">
        <div className="loading-container">
          <div className="spinner"></div>
          <div className="loading-text">Loading trip history...</div>
        </div>
      </div>
    )
  }

  return (
    <div className="page">
      <div className="page-header">
        <h1>{t.history}</h1>
      </div>

      {performance.length > 0 && !selectedTrip && (
        <div style={{ marginBottom: '2rem', padding: '1.5rem', background: 'white', borderRadius: '16px', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)', animation: 'fadeInUp 0.4s ease' }}>
          <h2 style={{ fontSize: '1.25rem', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#1e293b' }}>
            📊 Model Performance Insights
          </h2>
          <p style={{ fontSize: '0.9rem', color: '#64748b', marginBottom: '1.5rem' }}>
            Accuracy measured based on real-world user satisfaction scores (Success = 4+ stars).
          </p>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '1rem' }}>
            {performance.map((p, idx) => (
              <div key={idx} style={{ padding: '1rem', border: '1px solid #e2e8f0', borderRadius: '12px', position: 'relative', overflow: 'hidden' }}>
                {idx === 0 && <div style={{ position: 'absolute', top: 0, left: 0, width: '4px', height: '100%', background: '#3b82f6' }}></div>}
                <div style={{ fontWeight: '700', color: '#1e293b', marginBottom: '0.6rem', display: 'flex', justifyContent: 'space-between' }}>
                  {p.model_name}
                  {idx === 0 && <span style={{ fontSize: '0.7rem', background: '#dbeafe', color: '#1e40af', padding: '0.1rem 0.4rem', borderRadius: '4px' }}>BEST PERFORMER</span>}
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9rem', marginBottom: '0.4rem' }}>
                  <span style={{ color: '#64748b' }}>Success Accuracy:</span>
                  <span style={{ fontWeight: '800', color: p.user_accuracy > 50 ? '#059669' : '#1e293b' }}>{p.user_accuracy}%</span>
                </div>
                <div className="progress-bar-bg" style={{ height: '8px', background: '#f1f5f9', borderRadius: '4px', marginBottom: '0.8rem' }}>
                  <div style={{ height: '100%', width: `${p.user_accuracy}%`, background: p.user_accuracy > 50 ? '#10b981' : '#3b82f6', borderRadius: '4px', transition: 'width 1s ease' }}></div>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem' }}>
                  <span style={{ color: '#64748b' }}>Avg Satisfaction:</span>
                  <span style={{ fontWeight: '600' }}>{p.avg_satisfaction} / 5 ⭐</span>
                </div>
                <div style={{ fontSize: '0.75rem', marginTop: '0.5rem', color: '#94a3b8' }}>
                  Based on {p.total_reviews} historical user ratings
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {selectedTrip ? (
        <div style={{ animation: 'fadeInUp 0.4s ease' }}>
          <button
            className="btn btn-secondary"
            onClick={() => setSelectedTrip(null)}
            style={{ marginBottom: '1.5rem' }}
          >
            ← Back
          </button>
          <div className="itinerary-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1.5rem', flexWrap: 'wrap' }}>
              <h2>📋 {selectedTrip.destination}</h2>
              {selectedTrip.ml_recommendation && (
                <span className="ml-tag">🤖 {selectedTrip.ml_recommendation}</span>
              )}
              {selectedTrip.satisfaction_score && (
                <div style={{ display: 'flex', gap: '2px', marginLeft: '0.5rem' }}>
                  {[1, 2, 3, 4, 5].map((s) => (
                    <span key={s} style={{ color: s <= selectedTrip.satisfaction_score ? '#fbbf24' : '#e2e8f0', fontSize: '1.3rem' }}>★</span>
                  ))}
                </div>
              )}
              <span className="trip-tag">{selectedTrip.travel_style}</span>
            </div>
            <div style={{ fontSize: '0.85rem', color: '#64748b', marginBottom: '1rem', display: 'flex', gap: '1.5rem', flexWrap: 'wrap' }}>
              <span>👤 {selectedTrip.user_name}</span>
              <span>💰 ₹{selectedTrip.budget.toLocaleString('en-IN')}</span>
              <span>📅 {selectedTrip.start_date} / {selectedTrip.end_date} ({selectedTrip.duration_days} days)</span>
              <span>👥 {selectedTrip.people || 1} people</span>
              <span>🤖 {selectedTrip.ml_model_used}</span>
              <span>🌐 {selectedTrip.language || 'English'}</span>
              <span>🕐 {new Date(selectedTrip.created_at).toLocaleDateString()}</span>
            </div>
            <div className="itinerary-content">
              <div dangerouslySetInnerHTML={{ __html: selectedTrip.generated_itinerary.replace(/\n/g, '<br/>').replace(/\*\*(.*?)\*\*/g, '<b>$1</b>') }} />
            </div>
          </div>
        </div>
      ) : (
        <>
          {trips.length === 0 ? (
            <div className="empty-state">
              <div className="empty-state-icon">🧳</div>
              <p>{t.emptyHist}</p>
            </div>
          ) : (
            <div className="trip-list">
              {trips.map(trip => (
                <div
                  key={trip.id}
                  className="trip-item"
                  onClick={() => setSelectedTrip(trip)}
                >
                  <div className="trip-info">
                    <h3>🌍 {trip.destination}</h3>
                    <p>
                      {trip.user_name} • ₹{trip.budget.toLocaleString('en-IN')} •{' '}
                      {trip.start_date} to {trip.end_date} •{' '}
                      {new Date(trip.created_at).toLocaleDateString()}
                    </p>
                  </div>
                  <div className="trip-meta" style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '0.5rem' }}>
                    <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                      <span className="trip-tag">{trip.travel_style}</span>
                      {trip.ml_recommendation && (
                        <span className="ml-tag">🤖 {trip.ml_recommendation}</span>
                      )}
                    </div>
                    {trip.satisfaction_score && (
                      <div style={{ display: 'flex', gap: '1px' }}>
                        {[1, 2, 3, 4, 5].map((s) => (
                          <span key={s} style={{ color: s <= trip.satisfaction_score ? '#fbbf24' : '#e2e8f0', fontSize: '1rem' }}>★</span>
                        ))}
                      </div>
                    )}
                  </div>
                  <button
                    className="btn-delete"
                    onClick={(e) => handleDelete(trip.id, e)}
                  >
                    🗑️ Delete
                  </button>
                </div>
              ))}
            </div>
          )}
        </>
      )}

      {toast && <div className="toast">✅ {toast}</div>}
    </div>
  )
}
