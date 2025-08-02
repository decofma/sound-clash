# ⚔️ Sound-Clash ⚔️

Um web app divertido para decidir quem são os artistas mais populares do momento em uma batalha de 30 rounds! O Sound-Clash utiliza a API do Spotify para buscar dados de artistas em tempo real e oferece uma experiência interativa e dinâmica.

[![Linguagem](https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Framework](https://img.shields.io/badge/Framework-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Hospedagem](https://img.shields.io/badge/Hosted%20on-Vercel-black?style=for-the-badge&logo=vercel&logoColor=white)](https://vercel.com)
[![Licença](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

---

## 🚀 Acessando o Projeto
Você pode jogar o Sound-Clash agora mesmo clicando no link abaixo:

**[https://sound-clash-SEU-NOME.vercel.app/](https://sound-clash-SEU-NOME.vercel.app/)** *(Lembre-se de substituir pelo link real do seu app na Vercel!)*

## ✨ Features
- **Dados em Tempo Real:** Integração com a API do Spotify para buscar os artistas mais relevantes do momento.
- **Jogabilidade Interativa:** Batalha de 10 rounds onde o vencedor de cada rodada avança para enfrentar um novo desafiante.
- **Interface Limpa:** Layout responsivo e agradável criado inteiramente com Streamlit.
- **Deploy Simplificado:** Configurado para deploy contínuo na plataforma Vercel.

## 🛠️ Tecnologias Utilizadas
- **Python:** Linguagem principal do projeto.
- **Streamlit:** Framework utilizado para a construção da interface e da lógica do backend.
- **Spotipy:** Biblioteca Python para comunicação com a API do Spotify.
- **Vercel:** Plataforma de hospedagem para o deploy do aplicativo.

## ⚙️ Configuração do Ambiente Local
Para rodar este projeto na sua própria máquina, siga os passos abaixo:

**1. Clone o repositório:**
```bash
git clone [https://github.com/SEU-USUARIO/sound-clash.git](https://github.com/SEU-USUARIO/sound-clash.git)
cd sound-clash
```

**2. Crie e ative um ambiente virtual (recomendado):**
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Instale as dependências:**
```bash
pip install -r requirements.txt
```

**4. Configure suas chaves da API do Spotify:**
   - Crie uma pasta chamada `.streamlit` na raiz do projeto.
   - Dentro dela, crie um arquivo chamado `secrets.toml`.
   - Adicione suas credenciais do Spotify neste arquivo. **Este arquivo não deve ser enviado para o GitHub!**
   
   ```toml
   # .streamlit/secrets.toml

   SPOTIPY_CLIENT_ID = "SEU_CLIENT_ID_AQUI"
   SPOTIPY_CLIENT_SECRET = "SEU_CLIENT_SECRET_AQUI"
   ```

## ▶️ Como Executar Localmente
Com o ambiente configurado, basta executar o seguinte comando no seu terminal:
```bash
streamlit run app.py
```
O aplicativo abrirá automaticamente no seu navegador.

## 🚢 Deploy
O projeto está configurado para deploy na Vercel. O processo envolve:
1. Enviar o código para um repositório no GitHub.
2. Importar o repositório na Vercel.
3. Configurar as `Environment Variables` (`SPOTIPY_CLIENT_ID` e `SPOTIPY_CLIENT_SECRET`) no painel da Vercel.

## 📄 Licença
Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](https://opensource.org/licenses/MIT) para mais detalhes.

---

[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/andreamferraz])
[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/decofma)
