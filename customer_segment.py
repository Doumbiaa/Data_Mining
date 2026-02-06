import pandas as pd
import os

def get_rfm_data():
    """Charge les résultats RFM sauvegardés."""
    if os.path.exists('rfm_model.pkl'):
        return pd.read_pickle('rfm_model.pkl')
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