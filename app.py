import pandas as pd               # pandas : bibliothèque pour manipuler des tableaux (DataFrame)
import seaborn as sns             # seaborn : librairie de visualisation (basée sur matplotlib)
import matplotlib.pyplot as plt   # matplotlib : pour créer des figures personnalisées
import streamlit as st            # streamlit : framework pour créer des applications web interactives en Python

# Configuration de la page Streamlit -----------------------------------------
st.set_page_config(page_title="💼 Analyse des Salaires", layout="wide")
# st.set_page_config : configure des paramètres globaux de l'app Streamlit.
# page_title : le texte qui apparaît dans l'onglet du navigateur.
# layout="wide" : demande un affichage large (utilise toute la largeur de la page) — pratique pour tableaux / graphiques côte à côte.

# Titre principal de l'application -------------------------------------------
st.title("💼 Tableau de bord interactif – Analyse des salaires des employés")
# st.title : affiche le titre principal en haut. Tu peux utiliser des emojis pour rendre l'UI plus engageante.

# Upload du fichier ----------------------------------------------------------
fichier = st.file_uploader("📂 Importer un fichier CSV contenant les salaires", type=['csv'])
# st.file_uploader : widget qui permet à l'utilisateur d'uploader un fichier.
# argument 'type' : on limite aux fichiers .csv pour éviter d'autres formats par erreur.
# la variable 'fichier' contient un objet semblable à un buffer si un fichier est importé, sinon None.

if fichier is not None:
    # Lecture du CSV en DataFrame pandas
    df = pd.read_csv(fichier)
    st.subheader("👀 Aperçu des données importées")
    st.dataframe(df.head())
    # pd.read_csv : lit le fichier CSV en mémoire comme un DataFrame.
    # st.dataframe : affiche un tableau interactif dans l'app (avec scroll, tri possible).

    # Nettoyage basique des données ----------------------------------------
    df['Salaire'] = pd.to_numeric(df['Salaire'], errors='coerce')
    # pd.to_numeric convertit la colonne en numérique ; errors='coerce' transforme les valeurs invalides en NaN.
    df = df.dropna(subset=['Salaire'])
    # dropna(subset=['Salaire']) : supprime les lignes où Salaire est manquant (NaN).

    # Statistiques descriptives ---------------------------------------------
    st.subheader("📈 Statistiques sur les salaires")
    st.write(df['Salaire'].describe())
    # describe() renvoie count, mean, std, min, quartiles, max ; st.write affiche proprement.

    # Widget : slider pour filtrer par seuil -------------------------------
    seuil = st.slider(
        "Sélectionner un seuil de salaire (monnaie locale)",
        int(df['Salaire'].min()),
        int(df['Salaire'].max()),
        int(df['Salaire'].median())
    )
    # st.slider : contrôle interactif. Arguments : label, min, max, valeur par défaut.
    # On cast en int parce que slider attend des entiers — explique la conversion.

    st.markdown(f"### 👔 Employés gagnant plus de **{seuil:,}**")
    df_filtre = df[df['Salaire'] > seuil]   # filtrage de pandas (boolean indexing)
    st.dataframe(df_filtre)
    # Ici on affiche la table filtrée. Très utile pour montrer l'impact du slider.

    # Catégorisation (colonne calculée) -----------------------------------
    def categorie_salaire(s):
        if s < 200000:
            return "Faible revenu"
        elif s < 400000:
            return "Revenu moyen"
        else:
            return "Haut revenu"

    df['Catégorie'] = df['Salaire'].apply(categorie_salaire)
    # On ajoute une nouvelle colonne 'Catégorie' en appliquant une fonction ligne par ligne.
    # Montre la différence entre colonne calculée (persistée dans df) et mesure DAX (Power BI) si tu veux.

    st.subheader("📊 Répartition des catégories de salaire")
    st.bar_chart(df['Catégorie'].value_counts())
    # st.bar_chart : méthode simple pour tracer un graphique à barres. Ici on donne la série value_counts().

    # Histogramme avec seaborn / matplotlib --------------------------------
    st.subheader("📉 Distribution des salaires")
    fig, ax = plt.subplots()
    sns.histplot(df['Salaire'], kde=True, ax=ax, color="orange")
    st.pyplot(fig)
    # On crée une figure Matplotlib pour plus de contrôle. st.pyplot affiche la figure dans Streamlit.

    # Moyenne par département ----------------------------------------------
    st.subheader("🏢 Salaire moyen par département")
    salaire_par_dept = df.groupby("Département")["Salaire"].mean().sort_values(ascending=False)
    st.bar_chart(salaire_par_dept)
    # groupby + mean calcule le salaire moyen par département ; sort_values pour trier la série.

    # Bouton de téléchargement ---------------------------------------------
    st.download_button(
        "📥 Télécharger la liste filtrée (CSV)",
        df_filtre.to_csv(index=False).encode('utf-8'),
        file_name='agents_filtres.csv',
        mime='text/csv'
    )
    # st.download_button : crée un bouton qui permet à l'utilisateur de télécharger un fichier généré à la volée.
    # On encode en utf-8 pour garantir l'encodage, et on donne un nom de fichier.

else:
    st.info("👈 Importez un fichier CSV pour commencer l’analyse.")
    # Si aucun fichier n'est uploadé, on affiche un message d'information.

