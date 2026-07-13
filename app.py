import streamlit as st
import requests

# Configuração da página web
st.set_page_config(page_title="Monitor P2P Arbitragem", page_icon="📊", layout="wide")

st.title("📊 Monitor de Preços P2P: Binance")
st.subheader("Acompanhe as cotações em tempo real e analise as condições dos anunciantes.")

# Aba para escolher qual mercado visualizar
aba_zar, aba_aoa = st.tabs(["🇿🇦 Mercado ZAR (África do Sul)", "🇦🇴 Mercado AOA (Angola)"])

# Função genérica para buscar dados da Binance passando a moeda (fiat)
def obter_dados_p2p(tipo_operacao, moeda_fiat):
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    payload = {
        "fiat": moeda_fiat,
        "page": 1,
        "rows": 20,
        "tradeType": tipo_operacao,
        "asset": "USDT",
        "countries": [],
        "proMerchantAds": False,
        "shieldMerchantAds": False,
        "publisherType": None
    }
    try:
        resposta = requests.post(url, json=payload)
        return resposta.json().get('data', [])
    except Exception as e:
        st.error(f"Erro ao conectar com a Binance ({moeda_fiat}): {e}")
        return []

# --- ABA 1: MERCADO ZAR ---
with aba_zar:
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("🟢 Compradores ZAR")
        dados = obter_dados_p2p("BUY", "ZAR")
        if dados:
            for i, anuncio in enumerate(dados, 1):
                adv = anuncio['adv']
                user = anuncio['advertiser']
                with st.container(border=True):
                    st.markdown(f"**#{i} `{user['nickName']}`** ➔ ### **{adv['price']} ZAR**")
                    st.caption(f"Limites: {adv['minSingleTransAmount']} - {adv['maxSingleTransAmount']} ZAR")
        else: st.warning("Sem dados.")

    with col2:
        st.header("🔴 Vendedores ZAR")
        dados = obter_dados_p2p("SELL", "ZAR")
        if dados:
            for i, anuncio in enumerate(dados, 1):
                adv = anuncio['adv']
                user = anuncio['advertiser']
                with st.container(border=True):
                    st.markdown(f"**#{i} `{user['nickName']}`** ➔ ### **{adv['price']} ZAR**")
                    st.caption(f"Limites: {adv['minSingleTransAmount']} - {adv['maxSingleTransAmount']} ZAR")
        else: st.warning("Sem dados.")

# --- ABA 2: MERCADO AOA (ANGOLA com Termos do Anunciante) ---
with aba_aoa:
    st.info("💡 Nota para Angola: Como muitos anunciantes não colocam o câmbio real no preço estruturado, clique em '📄 Ver Termos do Anunciante' para checar as condições e taxas descritas por eles.")
    
    col1_aoa, col2_aoa = st.columns(2)
    
    with col1_aoa:
        st.header("🟢 Compradores AOA")
        dados_aoa_buy = obter_dados_p2p("BUY", "AOA")
        if dados_aoa_buy:
            for i, anuncio in enumerate(dados_aoa_buy, 1):
                adv = anuncio['adv']
                user = anuncio['advertiser']
                termos = adv.get('advDetailRemark', 'Nenhum termo inserido pelo anunciante.')
                
                with st.container(border=True):
                    st.markdown(f"**#{i} Anunciante:** `{user['nickName']}`")
                    st.markdown(f"### Preço de Tabela: **{adv['price']} AOA**")
                    st.text(f"Limites: {adv['minSingleTransAmount']} - {adv['maxSingleTransAmount']} AOA")
                    
                    # Botão expansível para ler os termos reais ocultos
                    with st.expander("📄 Ver Termos do Anunciante"):
                        st.write(termos)
        else: st.warning("Nenhum dado encontrado.")

    with col2_aoa:
        st.header("🔴 Vendedores AOA")
        dados_aoa_sell = obter_dados_p2p("SELL", "AOA")
        if dados_aoa_sell:
            for i, anuncio in enumerate(dados_aoa_sell, 1):
                adv = anuncio['adv']
                user = anuncio['advertiser']
                termos = adv.get('advDetailRemark', 'Nenhum termo inserido pelo anunciante.')
                
                with st.container(border=True):
                    st.markdown(f"**#{i} Anunciante:** `{user['nickName']}`")
                    st.markdown(f"### Preço de Tabela: **{adv['price']} AOA**")
                    st.text(f"Limites: {adv['minSingleTransAmount']} - {adv['maxSingleTransAmount']} AOA")
                    
                    # Botão expansível para ler os termos reais ocultos
                    with st.expander("📄 Ver Termos do Anunciante"):
                        st.write(termos)
        else: st.warning("Nenhum dado encontrado.")