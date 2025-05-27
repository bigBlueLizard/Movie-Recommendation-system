import pickle
import streamlit as st
import requests

st.set_page_config(
    page_title="🎬 MovieMate by Somil",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🎬"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        margin: 0;
        padding: 0;
        height: 100%;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: #0a0a0a !important;
        color: #ffffff !important;
    }

    .stApp {
        background: #0a0a0a !important;
        padding: 0 !important;
        margin: 0 !important;
        min-height: 100vh !important;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background: transparent;
    }

    /* Hero Section */
    .hero-container {
        width: 100%;
        min-height: 100vh;
        background: radial-gradient(ellipse at center, rgba(102, 126, 234, 0.15) 0%, rgba(10, 10, 10, 1) 70%);
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem;
        position: relative;
        overflow: hidden;
    }

    .hero-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle at 20% 50%, rgba(102, 126, 234, 0.08) 0%, transparent 50%),
                    radial-gradient(circle at 80% 20%, rgba(118, 75, 162, 0.08) 0%, transparent 50%),
                    radial-gradient(circle at 40% 80%, rgba(102, 126, 234, 0.08) 0%, transparent 50%);
        animation: float 20s ease-in-out infinite;
        z-index: 1;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        33% { transform: translateY(-30px) rotate(120deg); }
        66% { transform: translateY(30px) rotate(240deg); }
    }

    .hero-content {
        position: relative;
        z-index: 2;
        text-align: center;
        color: white;
        max-width: 800px;
        padding: 4rem 3rem;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 25px;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .hero-content h1 {
        font-size: clamp(3rem, 8vw, 5rem);
        margin-bottom: 0.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: none;
    }

    .hero-subtitle {
        font-size: 1.5rem;
        margin-bottom: 1rem;
        color: #a0a0a0;
        font-weight: 300;
    }

    .hero-description {
        font-size: 1.2rem;
        margin-bottom: 2.5rem;
        color: #c0c0c0;
        line-height: 1.6;
        font-weight: 400;
    }

    .social-links {
        margin-top: 2rem;
        display: flex;
        justify-content: center;
        gap: 1rem;
    }

    .social-links a {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 50px;
        height: 50px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .social-links a:hover {
        background: rgba(102, 126, 234, 0.2);
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
    }

    /* Main Application Styling */
    .main-container {
        background: rgba(255, 255, 255, 0.03);
        padding: 3rem 2rem;
        border-radius: 25px;
        margin: 2rem 0;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.2);
    }

    .main-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }

    .main-subtitle {
        color: #a0a0a0;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }

    /* Enhanced Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        padding: 1rem 2rem !important;
        border-radius: 25px !important;
        border: none !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3) !important;
        width: 100% !important;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: 0.5px !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4) !important;
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%) !important;
    }

    .stButton > button:active {
        transform: translateY(-1px) !important;
    }

    /* Navigation Button Styling - Fixed text color */
    .stButton > button[disabled] {
        background: rgba(102, 126, 234, 0.3) !important;
        color: #ffffff !important;
        opacity: 0.7 !important;
        cursor: not-allowed !important;
        box-shadow: none !important;
    }

    .stButton > button[disabled]:hover {
        transform: none !important;
        box-shadow: none !important;
        background: rgba(102, 126, 234, 0.3) !important;
    }

    /* Sidebar Enhancements */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    /* Sidebar Text Color Override */
    .css-1d391kg .stMarkdown,
    .css-1d391kg .stMarkdown p,
    .css-1d391kg .stMarkdown h1,
    .css-1d391kg .stMarkdown h2,
    .css-1d391kg .stMarkdown h3,
    .css-1d391kg .stMarkdown h4,
    .css-1d391kg .stMarkdown h5,
    .css-1d391kg .stMarkdown h6,
    .css-1d391kg .stText,
    .css-1d391kg .stWrite,
    .css-1d391kg div[data-testid="stSidebar"] .stMarkdown,
    .css-1d391kg div[data-testid="stSidebar"] .stMarkdown p,
    .css-1d391kg div[data-testid="stSidebar"] h1,
    .css-1d391kg div[data-testid="stSidebar"] h2,
    .css-1d391kg div[data-testid="stSidebar"] h3,
    .css-1d391kg div[data-testid="stSidebar"] h4,
    .css-1d391kg div[data-testid="stSidebar"] h5,
    .css-1d391kg div[data-testid="stSidebar"] h6,
    div[data-testid="stSidebar"] .stMarkdown,
    div[data-testid="stSidebar"] .stMarkdown p,
    div[data-testid="stSidebar"] .stMarkdown h1,
    div[data-testid="stSidebar"] .stMarkdown h2,
    div[data-testid="stSidebar"] .stMarkdown h3,
    div[data-testid="stSidebar"] .stMarkdown h4,
    div[data-testid="stSidebar"] .stMarkdown h5,
    div[data-testid="stSidebar"] .stMarkdown h6,
    div[data-testid="stSidebar"] .stText,
    div[data-testid="stSidebar"] .stWrite,
    div[data-testid="stSidebar"] p,
    div[data-testid="stSidebar"] span {
        color: #000000 !important;
    }

    .sidebar-header {
        text-align: center;
        margin-bottom: 2rem;
        padding: 1.5rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .sidebar-header h2 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.8rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }

    .sidebar-header p {
        color: #000000;
        font-style: italic;
        font-weight: 300;
    }

    .sidebar-social a {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        color: #333333;
        text-decoration: none;
        margin-bottom: 0.75rem;
        padding: 0.5rem;
        border-radius: 10px;
        transition: all 0.3s ease;
        font-weight: 500;
    }

    .sidebar-social a:hover {
        color: #667eea;
        background: rgba(102, 126, 234, 0.1);
        transform: translateX(5px);
    }

    /* Select Box Styling */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        color: #ffffff !important;
        backdrop-filter: blur(10px) !important;
    }

    .stSelectbox > div > div:focus-within {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }

    .stSelectbox label {
        color: #ffffff !important;
        font-weight: 500 !important;
        font-size: 1.1rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* Movie Card Enhancements */
    .movie-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        height: 100%;
    }

    .movie-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
        border-color: rgba(102, 126, 234, 0.3);
    }

    .movie-card img {
        border-radius: 15px;
        margin-bottom: 1rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease;
    }

    .movie-card:hover img {
        transform: scale(1.02);
    }

    .movie-card h3 {
        color: #ffffff !important;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    .movie-card p {
        color: #a0a0a0 !important;
        font-size: 0.95rem;
        margin-bottom: 0.25rem;
    }

    /* Footer Styling */
    .footer {
        text-align: center;
        padding: 2rem 1rem;
        color: #666;
        font-size: 0.95rem;
        margin-top: 3rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        background: rgba(255, 255, 255, 0.02);
    }

    .footer a {
        color: #667eea;
        text-decoration: none;
        font-weight: 500;
    }

    .footer a:hover {
        text-decoration: underline;
        color: #764ba2;
    }

    /* Text and Element Color Overrides */
    .stMarkdown, .stMarkdown p, .stText {
        color: #ffffff !important;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }

    /* Spinner/Loading Enhancements */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-content h1 {
            font-size: 2.5rem;
        }
        
        .hero-content {
            padding: 2rem 1.5rem;
            margin: 1rem;
        }

        .main-container {
            padding: 2rem 1rem;
            margin: 1rem 0;
        }

        .main-title {
            font-size: 2rem;
        }
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
    }

    /* Remove Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
            
    /* Target all Streamlit markdown elements and force white text */
    .stMarkdown * {
        color: white !important;
    }

    .movie-card * {
        color: white !important;
    }

    /* Target specific Streamlit classes */
    .css-1v0mbdj, .css-1v0mbdj *,
    .element-container *, 
    div[data-testid="stMarkdownContainer"] *,
    div[data-testid="stMarkdownContainer"] h1,
    div[data-testid="stMarkdownContainer"] h2,
    div[data-testid="stMarkdownContainer"] h3,
    div[data-testid="stMarkdownContainer"] p {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

def fetch_movie_data(movie_title):
    """Fetch movie data from OMDB API"""
    try:
        url = f"http://www.omdbapi.com/?t={movie_title.replace(' ', '%20')}&apikey=3f42ea31"
        response = requests.get(url, timeout=5)
        data = response.json()
        if data.get("Response") == "True":
            return {
                "poster": data.get("Poster", 'https://via.placeholder.com/300x450/333/fff?text=No+Image'),
                "year": data.get("Year", "N/A"),
                "genre": data.get("Genre", "N/A"),
                "rating": data.get("imdbRating", "N/A")
            }
        else:
            return {
                "poster": 'https://via.placeholder.com/300x450/333/fff?text=No+Image',
                "year": "N/A",
                "genre": "N/A",
                "rating": "N/A"
            }
    except Exception as e:
        return {
            "poster": 'https://via.placeholder.com/300x450/333/fff?text=No+Image',
            "year": "N/A",
            "genre": "N/A",
            "rating": "N/A"
        }

def recommend(movie):
    """Generate movie recommendations based on similarity"""
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended = []

        for i in distances[1:6]:
            movie_title = movies.iloc[i[0]].title
            movie_data = fetch_movie_data(movie_title)
            recommended.append({
                "title": movie_title,
                "poster": movie_data["poster"],
                "year": movie_data["year"],
                "genre": movie_data["genre"],
                "rating": movie_data["rating"]
            })

        return recommended
    except Exception as e:
        st.error(f"Error generating recommendations: {str(e)}")
        return []

@st.cache_data
def load_data():
    """Load movie data and similarity matrix"""
    try:
        movies = pickle.load(open('movie_list.pkl', 'rb'))
        similarity = pickle.load(open('similarity.pkl', 'rb'))
        return movies, similarity
    except FileNotFoundError:
        st.error("⚠️ Required data files (movie_list.pkl, similarity.pkl) not found!")
        st.info("Please ensure you have the following files in your directory:")
        st.code("- movie_list.pkl\n- similarity.pkl")
        st.stop()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.stop()

# Load data
movies, similarity = load_data()
movie_list = movies['title'].values

# Initialize session state
if 'started' not in st.session_state:
    st.session_state.started = False

# Landing page
if not st.session_state.started:
    st.markdown(
        """
        <div class="hero-container">
            <div class="hero-content">
                <h1>MovieMate</h1>
                <p class="hero-subtitle">by Somil Pandita</p>
                <p class="hero-description">Discover your next favorite film with AI-powered recommendations. Get personalized movie suggestions based on your taste and preferences.</p>
                <div class="social-links">
                    <a href="https://github.com/bigBlueLizard/" target="_blank">
                        <svg width="24" height="24" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                        </svg>
                    </a>
                    <a href="https://www.linkedin.com/in/somil-p-b0aa36266/" target="_blank">
                        <svg width="24" height="24" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                        </svg>
                    </a>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("🚀 Get Started", key="start_button"):
        st.session_state.started = True
        st.rerun()

# Main application
else:
    with st.sidebar:
        # CSS to make all text black - exclude sidebar controls
        st.markdown("""
        <style>
        /* Target all sidebar text elements but exclude controls */
        .sidebar-header h2, .sidebar-header p,
        .sidebar .markdown-text-container,
        .sidebar .element-container p,
        .sidebar .element-container h1,
        .sidebar .element-container h2,
        .sidebar .element-container h3,
        .sidebar .stMarkdown p,
        .sidebar .stMarkdown h3,
        .sidebar .stMarkdown div,
        .sidebar-social a,
        section[data-testid="stSidebar"] .stMarkdown *,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            color: black !important;
        }
        
        /* Ensure social links and SVGs are black */
        .sidebar-social a {
            color: black !important;
            fill: black !important;
        }
        
        .sidebar-social svg {
            fill: black !important;
        }
        
        /* Override any theme colors for links */
        .sidebar-social a:hover {
            color: #333 !important;
        }
        
        /* Force black text on markdown elements */
        .stMarkdown > div > p {
            color: black !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown(
            """
            <div class="sidebar-header">
                <h2 style="color: black;">MovieMate</h2>
                <p style="color: black;">by Somil Pandita</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")
        st.markdown('<h3 style="color: black;">🧭 Navigation</h3>', unsafe_allow_html=True)
        
        if st.button("Home", key="nav_home"):
            st.session_state.started = False
            st.rerun()

        st.button("Recommender", disabled=True, key="nav_rec")

        st.markdown("---")
        st.markdown('<h3 style="color: black;">ℹ️ About</h3>', unsafe_allow_html=True)
        st.markdown('<p style="color: black;">This AI-powered recommender suggests films you\'ll love based on your preferences. Built with Python and Streamlit using advanced machine learning algorithms.</p>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<h3 style="color: black;">🌐 Connect With Me</h3>', unsafe_allow_html=True)
        st.markdown("""
        <div class="sidebar-social">
            <a href="https://github.com/bigBlueLizard/" target="_blank" style="color: black; text-decoration: none;">
                <svg width="20" height="20" fill="black" viewBox="0 0 24 24">
                    <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                </svg>
                GitHub Profile
            </a>
            <br><br>
            <a href="https://www.linkedin.com/in/somil-p-b0aa36266/" target="_blank" style="color: black; text-decoration: none;">
                <svg width="20" height="20" fill="black" viewBox="0 0 24 24">
                    <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                </svg>
                LinkedIn Profile
            </a>
        </div>
        """, unsafe_allow_html=True)

    # Main content
    st.markdown(
        """
        <div class="main-container">
            <h1 class="main-title">🎬 Movie Recommender</h1>
            <p class="main-subtitle">Find similar movies to your favorites using AI-powered recommendations</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    selected_movie = st.selectbox(
        "🔍 Search or select a movie you like:",
        movie_list,
        key="movie_select"
    )

    if st.button('✨ Show Recommendations', key="recommend_button", type="primary"):
        with st.spinner("🎯 Finding similar movies tailored to your taste..."):
            recommendations = recommend(selected_movie)

            if recommendations:
                st.markdown(f"### 🎯 Top 5 Recommendations for: **{selected_movie}**")
                st.markdown("---")

                cols = st.columns(5)
                for i, col in enumerate(cols):
                    if i < len(recommendations):
                        with col:
                            with st.container():
                                # CSS to make movie card text white
                                st.markdown("""
                                <style>
                                .movie-card * {
                                    color: white !important;
                                }
                                
                                .movie-card h1,
                                .movie-card h2,
                                .movie-card h3,
                                .movie-card h4,
                                .movie-card h5,
                                .movie-card h6,
                                .movie-card p {
                                    color: white !important;
                                }
                                </style>
                                """, unsafe_allow_html=True)
                                
                                st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                                st.image(recommendations[i]["poster"], use_container_width=True)
                                st.markdown(f'<h3 style="color: white;">{recommendations[i]["title"]}</h3>', unsafe_allow_html=True)
                                st.markdown(f'<p style="color: white;"><strong>📅 Year:</strong> {recommendations[i]["year"]}</p>', unsafe_allow_html=True)
                                st.markdown(f'<p style="color: white;"><strong>🎭 Genre:</strong> {recommendations[i]["genre"]}</p>', unsafe_allow_html=True)
                                st.markdown(f'<p style="color: white;"><strong>⭐ Rating:</strong> {recommendations[i]["rating"]}/10</p>', unsafe_allow_html=True)
                                st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    st.markdown(
        """
        <div class="footer">
            <p>© 2024 MovieMate by <strong>Somil Pandita</strong> | 
                <a href="https://github.com/bigBlueLizard/" target="_blank">GitHub</a> | 
                <a href="https://www.linkedin.com/in/somil-p-b0aa36266/" target="_blank">LinkedIn</a>
            </p>
            <p style="margin-top: 0.5rem; font-size: 0.85rem; opacity: 0.7;">
                Built with ❤️ using Streamlit • Powered by Machine Learning
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )