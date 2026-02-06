# recommender.py

def get_recommendations(product_name, rules_df, n=5):
    """
    Logique métier pour extraire les recommandations à partir des règles d'association.
    """
    # 1. Sécurité : Vérifier si le modèle existe
    if rules_df is None or rules_df.empty:
        return []
        
    # 2. Normalisation de la saisie
    product_name = str(product_name).upper().strip()
    
    # 3. Filtrage des règles
    # On cherche le produit dans les antécédents (le "Si acheté...")
    mask = rules_df['antecedents'].apply(lambda x: product_name in [str(i).upper() for i in x])
    preds = rules_df[mask]
    
    if preds.empty:
        return []
    
    # 4. Tri par pertinence (Lift)
    # Le lift mesure la force du lien entre deux produits
    if 'lift' in preds.columns:
        preds = preds.sort_values(by='lift', ascending=False)
    
    # 5. Extraction des résultats uniques (Conséquents)
    recos = []
    for cq in preds['consequents']:
        for item in cq:
            item_str = str(item)
            # On évite de suggérer le produit saisi et les doublons
            if item_str.upper() != product_name and item_str not in recos:
                recos.append(item_str)
                
    return recos[:n]