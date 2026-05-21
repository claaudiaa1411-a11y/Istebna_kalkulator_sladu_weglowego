import streamlit as st

st.set_page_config(page_title="Eko-Kalkulator: Istebna", page_icon="🌲", layout="centered")

st.title("🌲 Twój Ślad Węglowy w Istebnej")
st.markdown("Sprawdź, jak Twój pobyt w Beskidzie Śląskim wpływa na środowisko. Zaznacz poniżej swoje wybory z ostatniego wyjazdu!")

st.divider()

st.subheader("🚗 1. Jak tu dotarłeś?")
transport = st.selectbox(
    "Wybierz główny środek transportu:",
    ["Samochód spalinowy (sam sam/a)", "Samochód spalinowy (z rodziną/znajomymi)", "Pociąg / Autobus", "Samochód elektryczny", "Rower / Pieszo"]
)
dystans = st.slider("Ile kilometrów w jedną stronę pokonałeś?", 10, 500, 100, step=10)

st.subheader("🏡 2. Gdzie spałeś?")
nocleg = st.radio(
    "Wybierz typ zakwaterowania:",
    ["Duży hotel (np. z basenem)", "Pensjonat / Willa", "Lokalna Agroturystyka", "Namiot / Schronisko"]
)
dni = st.slider("Ile nocy spędziłeś w Istebnej?", 1, 14, 3)

st.subheader("🧀 3. Co jadłeś i jak spędzałeś czas?")
jedzenie = st.selectbox(
    "Skąd pochodziło Twoje jedzenie?",
    ["Głównie supermarkety i jedzenie z zewnątrz", "Mieszane", "Głównie lokalne produkty (oscypki, karczmy regionalne)"]
)
aktywnosc = st.radio(
    "Jaka była Twoja główna aktywność?",
    ["Jazda autem po okolicy (np. na Równicę, do Wisły)", "Wyciągi narciarskie / Quady", "Spacery / Rower / Biegówki"]
)

st.divider()

if st.button("🌱 Oblicz mój ślad węglowy!", use_container_width=True):
    wynik_co2 = 0
    
    if "sam sam/a" in transport: wynik_co2 += dystans * 0.2
    elif "z rodziną" in transport: wynik_co2 += dystans * 0.1
    elif "Pociąg" in transport: wynik_co2 += dystans * 0.05
    elif "elektryczny" in transport: wynik_co2 += dystans * 0.08
    
    if "Duży hotel" in nocleg: wynik_co2 += dni * 15
    elif "Pensjonat" in nocleg: wynik_co2 += dni * 8
    elif "Agroturystyka" in nocleg: wynik_co2 += dni * 4
    elif "Namiot" in nocleg: wynik_co2 += dni * 1
        
    if "supermarkety" in jedzenie: wynik_co2 += 10
    if "lokalne" in jedzenie: wynik_co2 -= 5
    
    if "Jazda autem" in aktywnosc: wynik_co2 += 20
    elif "Spacery" in aktywnosc: wynik_co2 += 0

    st.success(f"### 📊 Twój szacunkowy ślad węglowy to: **{wynik_co2:.1f} kg CO2**")
    
    if wynik_co2 < 20:
        st.info("💚 Jesteś Eko-Bohaterem! Twój wyjazd miał minimalny wpływ na naturę. Lasy w Istebnej Ci dziękują!")
        st.balloons()
    elif wynik_co2 < 60:
        st.warning("🟡 Nie jest źle, ale jest miejsce na poprawę. Może następnym razem wybierzesz pociąg do Wisły i stamtąd rower?")
    else:
        st.error("🔴 Twój ślad węglowy jest wysoki! Aby to zrekompensować, powinieneś posadzić w tym roku co najmniej jedno drzewo.")
