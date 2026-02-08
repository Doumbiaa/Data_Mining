import pandas as pd
import os

def get_rfm_data():
    """Charge les résultats RFM sauvegardés."""
    try:
        # Chemin absolu basé sur le répertoire du script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, 'rfm_model.pkl')
        
        print(f"DEBUG - Répertoire base: {base_dir}")
        print(f"DEBUG - Chemin fichier: {file_path}")
        print(f"DEBUG - Fichier existe (absolu): {os.path.exists(file_path)}")
        print(f"DEBUG - Fichier existe (relatif): {os.path.exists('rfm_model.pkl')}")
        print(f"DEBUG - Répertoire courant: {os.getcwd()}")
        print(f"DEBUG - Fichiers dans répertoire courant: {os.listdir('.')}")
        
        if os.path.exists(file_path):
            df = pd.read_pickle(file_path)
            print(f"DEBUG - DataFrame chargé: {len(df)} lignes")
            print(f"DEBUG - Type d'index: {type(df.index)}")
            print(f"DEBUG - Premiers IDs: {df.index[:5].tolist()}")
            return df
        
        # Fallback: chercher dans le répertoire courant
        if os.path.exists('rfm_model.pkl'):
            df = pd.read_pickle('rfm_model.pkl')
            print(f"DEBUG - DataFrame chargé (fallback): {len(df)} lignes")
            print(f"DEBUG - Type d'index: {type(df.index)}")
            print(f"DEBUG - Premiers IDs: {df.index[:5].tolist()}")
            return df
            
        print("DEBUG - Fichier rfm_model.pkl introuvable")
        return None
    except Exception as e:
        print(f"ERREUR chargement RFM: {e}")
        import traceback
        traceback.print_exc()
        return None

def get_client_info(customer_id, rfm_df):
    """Récupère les infos d'un client spécifique."""
    print(f"DEBUG - Recherche client: {customer_id} (type: {type(customer_id)})")
    
    if rfm_df is None:
        print("DEBUG - rfm_df est None")
        return None
    
    if rfm_df.empty:
        print("DEBUG - rfm_df est vide")
        return None
    
    print(f"DEBUG - Nombre de clients dans rfm_df: {len(rfm_df)}")
    print(f"DEBUG - Type d'index du DataFrame: {type(rfm_df.index)}")
    
    try:
        # Essayer float
        cid = float(customer_id)
        print(f"DEBUG - Test avec float: {cid}")
        if cid in rfm_df.index:
            print(f"DEBUG - Client trouvé avec float!")
            return rfm_df.loc[cid].to_dict()
    except Exception as e:
        print(f"DEBUG - Erreur avec float: {e}")
    
    try:
        # Essayer int
        cid = int(customer_id)
        print(f"DEBUG - Test avec int: {cid}")
        if cid in rfm_df.index:
            print(f"DEBUG - Client trouvé avec int!")
            return rfm_df.loc[cid].to_dict()
    except Exception as e:
        print(f"DEBUG - Erreur avec int: {e}")
    
    try:
        # Essayer string
        print(f"DEBUG - Test avec string: {customer_id}")
        if customer_id in rfm_df.index:
            print(f"DEBUG - Client trouvé avec string!")
            return rfm_df.loc[customer_id].to_dict()
    except Exception as e:
        print(f"DEBUG - Erreur avec string: {e}")
    
    print(f"DEBUG - Client {customer_id} non trouvé après tous les tests")
    return None
