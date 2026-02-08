import pandas as pd
import os

# Render + local : dossier racine de l'application
RFM_PATH = os.path.join(os.getcwd(), "rfm_model.pkl")

def get_rfm_data():
    """Charge les résultats RFM sauvegardés."""
    try:
        if os.path.exists(RFM_PATH):
            return pd.read_pickle(RFM_PATH)
        else:
            print("❌ rfm_model.pkl introuvable :", RFM_PATH)
            return None
    except Exception as e:
        print("❌ Erreur chargement RFM :", e)
        return None

def get_client_info(customer_id, rfm_df):
    """Récupère les infos d'un client spécifique."""
    try:
        cid = float(customer_id)
        if rfm_df is not None and cid in rfm_df.index:
            return rfm_df.loc[cid].to_dict()
    except Exception as e:
        print("❌ Erreur client RFM :", e)
    return None
