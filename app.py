# app.py

import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

# --- CONFIGURAÇÃO DA PÁGINA E SEGREDOS ---

st.set_page_config(page_title="Sound-Clash", page_icon="⚔️", layout="wide")

# Para rodar localmente, crie o arquivo .streamlit/secrets.toml
# Para deploy na Vercel, configure as Environment Variables.
SPOTIPY_CLIENT_ID = st.secrets["SPOTIPY_CLIENT_ID"]
SPOTIPY_CLIENT_SECRET = st.secrets["SPOTIPY_CLIENT_SECRET"]

# --- CONEXÃO COM A API DO SPOTIFY ---

@st.cache_data
def get_top_artists():
    """
    Busca diretamente os artistas mais relevantes no Spotify usando a API de busca,
    conforme a sua sugestão. Este método é mais direto e robusto.
    """
    try:
        auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
        sp = spotipy.Spotify(auth_manager=auth_manager)

        # Usamos uma busca genérica e spotify retorna os artistas
        # mais populares/relevantes primeiro. A busca por "a" é um truque comum, mas pode colocar "artist" como esta na documentação deles
        # url pra consulta: https://developer.spotify.com/documentation/web-api/reference/search
        search_result = sp.search(q="a", type="artist", limit=50)

        artists = []
        # Criei essa verificação para ver se a busca retornou a estrutura esperada com artistas
        if search_result and search_result.get('artists', {}).get('items'):
            for artist_item in search_result['artists']['items']:
                # O item do artista já contém tudo que precisamos.
                # Apenas garantimos que ele tenha uma imagem antes de adicioná-lo.
                if artist_item and artist_item.get('images'):
                    artists.append({
                        'name': artist_item.get('name'),
                        'image_url': artist_item['images'][0]['url'],
                        'id': artist_item.get('id')
                    })
        
        if not artists:
            st.error("A busca por artistas não retornou resultados válidos.")
            return []

        return artists
        
    except Exception as e:
        st.error(f"Ocorreu um erro inesperado ao buscar os artistas.")
        st.error(f"Detalhe do erro: {e}")
        return []

# --- LÓGICA DO JOGO ---

def initialize_game():
    """Configura o estado inicial do jogo."""
    artists = get_top_artists()
    if not artists or len(artists) < 11:
        st.error("Não foi possível carregar artistas suficientes para o jogo.")
        st.stop()
        
    random.shuffle(artists)
    st.session_state.artists_pool = artists
    st.session_state.round = 1
    st.session_state.current_champion = None
    st.session_state.game_over = False

def setup_round():
    """Prepara os competidores para a rodada atual."""
    pool = st.session_state.artists_pool

    # Se for a primeira rodada, pega dois artistas aleatórios
    if st.session_state.current_champion is None:
        challenger1 = pool.pop()
        challenger2 = pool.pop()
    # Nas rodadas seguintes, o campeão enfrenta um novo artista
    else:
        challenger1 = st.session_state.current_champion
        # Lógica para garantir que o novo artista não seja o próprio campeão
        challenger2 = pool.pop()
        while challenger2['id'] == challenger1['id'] and pool:
            challenger2 = pool.pop()

    st.session_state.challenger1 = challenger1
    st.session_state.challenger2 = challenger2

def player_chooses(winner):
    """Callback chamado quando o jogador escolhe um vencedor."""
    st.session_state.current_champion = winner
    st.session_state.round += 1
    if st.session_state.round > 30:
        st.session_state.game_over = True

# --- INTERFACE DO USUÁRIO (FRONTEND) ---

st.markdown("<h1 style='text-align: center;'>⚔️ Sound-Clash ⚔️</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Escolha o artista mais popular em uma batalha de 30 rounds!</p>", unsafe_allow_html=True)

# Inicializa o jogo se ele ainda não começou
if 'artists_pool' not in st.session_state:
    initialize_game()

if st.session_state.game_over:
    st.balloons()
    
    st.markdown(f"<h1 style='text-align: center;'>🏆 O Campeão Final é: {st.session_state.current_champion['name']}! 🏆</h1>", unsafe_allow_html=True)
    
    # --- CENTRALIZAÇÃO DA IMAGEM ---

    img_spacer1, img_col, img_spacer2 = st.columns([1, 2, 1])
    with img_col:
        st.image(st.session_state.current_champion['image_url'], use_container_width=True)
    
    # Espaço entre a imagem e o botão para centralizar melhor hehehe #McgiverApproves 👀
    st.write("") 

    # --- CENTRALIZAÇÃO DO BOTÃO ---
    btn_spacer1, btn_col, btn_spacer2 = st.columns([2, 1, 2])
    with btn_col:
        if st.button("Jogar Novamente", use_container_width=True):
            initialize_game()
            st.rerun()

else:
    st.markdown("""
        <style>
        /* Seleciona todas as imagens dentro do container da aplicação */
        [data-testid="stAppViewContainer"] img {
            width: 100%; /* A imagem deve preencher a largura do seu container (nossa sub-coluna) */
            height: 300px; /* AQUI DEFINIMOS UMA ALTURA FIXA PARA TODAS AS IMAGENS */
            object-fit: cover; /* A MÁGICA: Corta a imagem para caber sem distorcer */
            border-radius: 8px; /* Opcional: Cantos arredondados na imagem */
        }
        </style>
        """, unsafe_allow_html=True)

    
    setup_round()
    challenger1 = st.session_state.challenger1
    challenger2 = st.session_state.challenger2

    st.markdown(f"<h2 style='text-align: center;'>Round {st.session_state.round} de 30</h2>", unsafe_allow_html=True)
    st.divider()

    col1, col2 = st.columns(2, gap="large")

    # --- CARD DO ARTISTA 1 ---
    with col1:
        sub_col1, sub_col2, sub_col3 = st.columns([1, 3, 1])

        with sub_col2:
            st.header(challenger1['name'])
            
            st.image(challenger1['image_url'], use_container_width=True)
            st.button(f"Escolher: {challenger1['name']}", on_click=player_chooses, args=(challenger1,), use_container_width=True, type="primary")

    # --- CARD DO ARTISTA 2 ---
    with col2:
        sub_col1, sub_col2, sub_col3 = st.columns([1, 3, 1])
        
        with sub_col2:
            st.header(challenger2['name'])
            st.image(challenger2['image_url'], use_container_width=True)
            st.button(f"Escolher: {challenger2['name']}", on_click=player_chooses, args=(challenger2,), use_container_width=True, type="primary")