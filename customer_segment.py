import pandas as pd
import os

# 🔹 Chemin absolu vers le dossier du fichier
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RFM_PATH = os.path.join(BASE_DIR, "rfm_model.pkl")

def get_rfm_data():
    """Charge les résultats RFM sauvegardés."""
    if os.path.exists(RFM_PATH):
        return pd.read_pickle(RFM_PATH)
    return None


def get_client_info(customer_id, rfm_df):
    """Récupère les infos d'un client spécifique."""
    try:
        # Conversion en float car les IDs clients sont souvent stockés ainsi
        cid = float(customer_id)
        if cid in rfm_df.index:
            return rfm_df.loc[cid].to_dict()
    except:
        pass
    return None
