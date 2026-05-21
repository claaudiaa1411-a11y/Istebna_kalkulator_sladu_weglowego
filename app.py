import streamlit as st
import pandas as pd
import numpy as np

# Konfiguracja strony na "szeroką" (wide), żeby wyglądało jak profesjonalny panel
st.set_page_config(page_title="Smart Istebna", page_icon="🌲", layout="wide")

st.title("🌲 Smart Istebna: Centrum Turystyki Zrównoważonej")
st.markdown("Kompleksowy system zarządzania turystyką. Wybierz odpowiedni moduł poniżej, aby rozpocząć.")

# Tworzymy 3 osobne zakładki
tab1, tab2, tab3 = st.tabs(["🗺️ Asystent Szlaku i Mapa", "🌱 Kalkulator i Grywalizacja", "📊 Panel Władz Gminy"])

# ==========================================
# ZAKŁADKA 1: ASYSTENT I MAPA
# ==========================================
with tab1:
    st.header("Interaktywna Mapa i Asystent Turysty")
    st.markdown("Omijaj tłumy i odkrywaj ukryte perełki naszej gminy! Pomożemy Ci wybrać odpowiednie miejsce.")
    
    col1, col2 = st.columns([1, 2]) # Podział na dwie kolumny (lewa węższa, prawa szersza)
    
    with col1:
        st.subheader("Czego dzisiaj szukasz?")
        typ_aktywnosci = st.selectbox("Preferowana aktywność:", ["Spokojny spacer (rodziny)", "Wymagający trekking", "Rower MTB", "Kultura i tradycja"])
        czas = st.slider("Ile masz czasu? [godziny]", 1, 8, 3)
        
        if st.button("Pokaż rekomendację 🧭", use_container_width=True):
            st.success("Wskazówka od AI: Zamiast zatłoczonego Złotego Gronia, polecamy dzisiaj spacer na Ochodzitę (mniej ludzi, piękne widoki) oraz wizytę u lokalnych koronczarek w Koniakowie!")
            
    with col2:
        # Prawdziwe współrzędne dla Istebnej, Koniakowa i Jaworzynki
        data = pd.DataFrame({
            'lat': [49.564, 49.548, 49.522, 49.544],
            'lon': [18.915, 18.948, 18.850, 18.953],
            'miejsce': ['Złoty Groń', 'Koniaków Koronki', 'Trójstyk', 'Ochodzita']
        })
        st.map(data, zoom=11)
        st.caption("Mapa kluczowych punktów w tzw. Trójwsi Beskidzkiej. Promujemy rozpraszanie ruchu turystycznego.")

# ==========================================
# ZAKŁADKA 2: KALKULATOR I ODZNAKI
# ==========================================
with tab2:
    st.header("Grywalizacja: Twój Ślad Węglowy")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Oceń swój wyjazd")
        transport = st.selectbox("Twój Transport:", ["Samochód spalinowy", "Pociąg / Autobus", "Rower / Pieszo"])
        jedzenie = st.selectbox("Twoje Jedzenie:", ["Jedzenie z supermarketu", "Lokalne produkty (oscypki, karczmy)"])
        smieci = st.radio("Czy zabierasz śmieci ze szlaku ze sobą?", ["Tak", "Zostawiam w koszach w lesie", "Czasem mi coś wypadnie"])
        
        if st.button("Oblicz i odbierz odznakę! 🏅", use_container_width=True):
            punkty_eko = 0
            if transport == "Rower / Pieszo": punkty_eko += 40
            elif transport == "Pociąg / Autobus": punkty_eko += 20
            
            if jedzenie == "Lokalne produkty (oscypki, karczmy)": punkty_eko += 30
            if smieci == "Tak": punkty_eko += 30
            
            # Zapisujemy punkty w pamięci sesji
            st.session_state['punkty'] = punkty_eko

    with col_b:
        st.subheader("Twój Status Eko-Turysty")
        # Pobieramy punkty (domyślnie 0, jeśli nikt nie kliknął przycisku)
        punkty = st.session_state.get('punkty', 0)
        
        # Pasek postępu
        st.progress(min(punkty / 100, 1.0))
        st.metric("Zgromadzone Punkty", f"{punkty} / 100")
        
        if punkty >= 80:
            st.success("🏅 ODZNAKA: Strażnik Beskidów!\n\nDziękujemy za dbanie o Istebną. Jesteś wzorem do naśladowania!")
            st.balloons()
        elif punkty >= 40:
            st.info("🥈 ODZNAKA: Świadomy Wędrowiec.\n\nJesteś na dobrej drodze, ale możesz zrobić jeszcze więcej dla natury.")
        elif punkty > 0:
            st.warning("🔴 UWAGA!\n\nTwój wpływ na środowisko jest bardzo negatywny. Przeanalizuj swoje wybory.")

# ==========================================
# ZAKŁADKA 3: DASHBOARD DLA GMINY
# ==========================================
with tab3:
    st.header("Panel Analityczny (Dla Wójta i Organizacji Turystycznych)")
    st.markdown("Interaktywny symulator decyzji politycznych oparty na prognozach algorytmicznych.")
    
    st.subheader("🛠️ Symulator Decyzji Gminnych")
    
    col_x, col_y = st.columns(2)
    with col_x:
        oplata = st.slider("Wysokość opłaty klimatycznej (PLN/noc):", 2.0, 10.0, 2.5, step=0.5)
    with col_y:
        zakaz = st.checkbox("Wprowadź strefę wolną od aut w centrum Istebnej", help="Zmniejsza smog, ale może początkowo odstraszyć część turystów jednodniowych.")
    
    # Prosta symulacja danych na potrzeby wykresu
    lata = [2024, 2025, 2026, 2027, 2028]
    budzet = [100 * oplata, 110 * oplata, 120 * oplata, 130 * oplata, 140 * oplata]
    smog = [100, 95, 90, 85, 80]
    
    # Magia symulacji: jeśli władze zaznaczą "zakaz wjazdu", algorytm zmienia wykresy
    if zakaz:
        smog = [100, 70, 50, 40, 30] # Drastyczny spadek smogu
        budzet = [b * 0.85 for b in budzet] # Chwilowy spadek wpływów o 15% z powodu braku aut
        
    df_symulacja = pd.DataFrame({
        "Wpływy do budżetu (tys. PLN)": budzet,
        "Poziom Smogu w Gminie (indeks)": smog
    }, index=lata)
    
    st.markdown("### 📈 Prognoza wpływu na gminę (Lata 2024-2028)")
    st.line_chart(df_symulacja)
    
    # Podsumowanie liczbowe pod wykresem
    met1, met2, met3 = st.columns(3)
    met1.metric("Szacowany Budżet w 2028", f"{int(budzet[-1])} tys. PLN", "+8%" if not zakaz else "-15%")
    met2.metric("Redukcja Smogu", f"{100 - int(smog[-1])}%", "spadek zanieczyszczeń", delta_color="inverse")
    met3.metric("Ruch Turystyczny", "Rośnie" if not zakaz else "Stabilizuje się", "Zrównoważony")
