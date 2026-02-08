import pandas as pd
import os

def get_rfm_data():
    """Charge les résultats RFM sauvegardés."""
    try:
        # Chemin absolu basé sur le répertoire du script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, 'rfm_model.pkl')
        
        if os.path.exists(file_path):
            return pd.read_pickle(file_path)
        
        # Fallback: chercher dans le répertoire courant
        if os.path.exists('rfm_model.pkl'):
            return pd.read_pickle('rfm_model.pkl')
            
        return None
    except Exception as e:
        print(f"Erreur chargement RFM: {e}")
        return None

def get_client_info(customer_id, rfm_df):
    """Récupère les infos d'un client spécifique."""
    if rfm_df is None or rfm_df.empty:
        return None
    
    try:
        # Essayer float
        cid = float(customer_id)
        if cid in rfm_df.index:
            return rfm_df.loc[cid].to_dict()
    except:
        pass
    
    try:
        # Essayer int
        cid = int(customer_id)
        if cid in rfm_df.index:
            return rfm_df.loc[cid].to_dict()
    except:
        pass
    
    try:
        # Essayer string
        if customer_id in rfm_df.index:
            return rfm_df.loc[customer_id].to_dict()
    except:
        pass
    
    return None
