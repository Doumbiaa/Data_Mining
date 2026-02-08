import pandas as pd
import os

# Chemin absolu vers le dossier du fichier
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RFM_PATH = os.path.join(BASE_DIR, "rfm_model.pkl")

def get_rfm_data():
    """Charge les résultats RFM sauvegardés."""
    try:
        if os.path.exists(RFM_PATH):
            rfm_df = pd.read_pickle(RFM_PATH)

            # Sécurité minimale
            if rfm_df is None or rfm_df.empty:
                print("RFM vide ou invalide")
                return None

            return rfm_df

        print("Fichier rfm_model.pkl introuvable")
        return None

    except Exception as e:
        print("Erreur chargement RFM :", e)
        return None


def get_client_info(customer_id, rfm_df):
    """Récupère les infos d'un client spécifique."""
    try:
        if rfm_df is None:
            return None

        # IDs clients stockés en float
        cid = float(customer_id)

        # ✅ Recherche dans la colonne CustomerID au lieu de l'index
        client = rfm_df[rfm_df['CustomerID'] == cid]

        if client.empty:
            return None

        # Retourne le dictionnaire de ce client
        return client.iloc[0].to_dict()

    except Exception as e:
        print("Erreur client RFM :", e)
        return None
