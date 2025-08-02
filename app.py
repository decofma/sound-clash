# app.py

import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

# --- CONFIGURAÇÃO DA PÁGINA E SEGREDOS ---

# Configura o título da página, ícone e layout. Isso deve ser a primeira chamada do Streamlit.
st.set_page_config(page_title="Sound-Clash", page_icon="⚔️", layout="wide")

# Carrega as credenciais de forma segura usando os segredos do Streamlit.
# Para rodar localmente, crie o arquivo .streamlit/secrets.toml
# Para deploy na Vercel, configure as Environment Variables.
SPOTIPY_CLIENT_ID = st.secrets["SPOTIPY_CLIENT_ID"]
SPOTIPY_CLIENT_SECRET = st.secrets["SPOTIPY_CLIENT_SECRET"]

# --- CONEXÃO COM A API DO SPOTIFY ---

# A anotação @st.cache_data garante que só vamos buscar os dados da API uma vez,
# mesmo que o usuário interaja com a interface. Isso torna o app muito mais rápido.
@st.cache_data
def get_top_artists():
    """
    Busca diretamente os artistas mais relevantes no Spotify usando a API de busca,
    conforme a sua sugestão. Este método é mais direto e robusto.
    """
    try:
        auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
        sp = spotipy.Spotify(auth_manager=auth_manager)

        # Usamos uma busca genérica. O Spotify geralmente retorna os artistas
        # mais populares/relevantes primeiro. A busca por "a" é um truque comum
        # para obter uma lista geral e bem classificada. Limitamos a 50 para ter uma boa amostra.
        search_result = sp.search(q="a", type="artist", limit=50)

        artists = []
        # Verificamos se a busca retornou a estrutura esperada com artistas
        if search_result and search_result.get('artists', {}).get('items'):
            for artist_item in search_result['artists']['items']:
                # O item do artista já contém tudo que precisamos.
                # Apenas garantimos que ele tenha uma imagem antes de adicioná-lo.
                if artist_item and artist_item.get('images'):
                    artists.append({
                        'name': artist_item.get('name'),
                        'image_url': artist_item['images'][0]['url'], # Pega a primeira imagem (maior)
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
    # Nas rodadas seguintes, o campeão enfrenta um novo desafiante
    else:
        challenger1 = st.session_state.current_champion
        # Garante que o novo desafiante não seja o próprio campeão
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

# CÓDIGO NOVO E CENTRALIZADO
st.markdown("<h1 style='text-align: center;'>⚔️ Sound-Clash ⚔️</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Escolha o artista mais popular em uma batalha de 30 rounds!</p>", unsafe_allow_html=True)

# Inicializa o jogo se ele ainda não começou
if 'artists_pool' not in st.session_state:
    initialize_game()

# if st.session_state.game_over: (substitua todo este bloco)

if st.session_state.game_over:
    st.balloons()
    
    # Título do campeão, já centralizado
    st.markdown(f"<h1 style='text-align: center;'>🏆 O Campeão Final é: {st.session_state.current_champion['name']}! 🏆</h1>", unsafe_allow_html=True)
    
    # --- CENTRALIZAÇÃO DA IMAGEM ---
    # Criamos 3 colunas, mas só usamos a do meio para colocar a imagem.
    # As colunas 1 e 3 servem como espaçadores para empurrar a do meio para o centro.
    img_spacer1, img_col, img_spacer2 = st.columns([1, 2, 1])
    with img_col:
        st.image(st.session_state.current_champion['image_url'], use_container_width=True)
    
    # Adiciona um espaço em branco para separar a imagem do botão
    st.write("") 

    # --- CENTRALIZAÇÃO DO BOTÃO ---
    # Usamos o mesmo truque para o botão, com proporções diferentes para um visual melhor.
    btn_spacer1, btn_col, btn_spacer2 = st.columns([2, 1, 2])
    with btn_col:
        if st.button("Jogar Novamente", use_container_width=True):
            initialize_game()
            st.rerun()

# app.py (substitua o bloco 'else' final por esta versão completa)

else:
    # --- PASSO 1: ADICIONAR O CSS PARA PADRONIZAR A ALTURA DAS IMAGENS ---
    # Este CSS vai ser aplicado a todas as imagens dentro do container principal do Streamlit.
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

    # --- PASSO 2: MANTER A ESTRUTURA DE COLUNAS (NÃO MUDA NADA AQUI) ---
    # O resto do código continua exatamente o mesmo da versão anterior.
    
    # Prepara os desafiantes para a rodada
    setup_round()
    challenger1 = st.session_state.challenger1
    challenger2 = st.session_state.challenger2

    st.markdown(f"<h2 style='text-align: center;'>Round {st.session_state.round} de 30</h2>", unsafe_allow_html=True)
    st.divider()

    # As duas colunas principais do layout
    col1, col2 = st.columns(2, gap="large")

    # --- CARD DO ARTISTA 1 ---
    with col1:
        # Colunas aninhadas para controlar o tamanho e o alinhamento.
        sub_col1, sub_col2, sub_col3 = st.columns([1, 3, 1])

        # Todo o conteúdo vai na coluna do meio (sub_col2)
        with sub_col2:
            st.header(challenger1['name'])
            
            # A imagem e o botão preenchem a largura da sub_col2
            st.image(challenger1['image_url'], use_container_width=True)
            st.button(f"Escolher: {challenger1['name']}", on_click=player_chooses, args=(challenger1,), use_container_width=True, type="primary")

    # --- CARD DO ARTISTA 2 ---
    with col2:
        # Repetimos a mesma estrutura para o segundo artista
        sub_col1, sub_col2, sub_col3 = st.columns([1, 3, 1])
        
        with sub_col2:
            st.header(challenger2['name'])
            st.image(challenger2['image_url'], use_container_width=True)
            st.button(f"Escolher: {challenger2['name']}", on_click=player_chooses, args=(challenger2,), use_container_width=True, type="primary")