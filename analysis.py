def description(data):
    """
    Fonction qui retourne les statistiques descriptives d'un DataFrame
    
    Paramètres:
    -----------
    data : pandas.DataFrame
        Le DataFrame à analyser
    
    Retourne:
    ---------
    dict : Dictionnaire contenant les statistiques descriptives
    """
    
    # Dimension
    dimension = data.shape
    
    # Le pourcentage de valeurs manquantes
    pct_manquantes = (data.isnull().sum() / data.shape[0] * 100).sort_values(ascending=False)
    
    # Les lignes dupliquées
    pct_dupliquees = data.duplicated().sum() / data.shape[0] * 100
    
    # Quantité négative (si la colonne existe)
    qty_negative = (data['Quantity'] < 0).sum() if 'Quantity' in data.columns else None
    
    # Les commandes annulées (si la colonne existe)
    commandes_annulees = (data['InvoiceNo'].astype(str).str.startswith('C')).sum() if 'InvoiceNo' in data.columns else None
    
    # Affichage des résultats
    print("="*70)
    print("STATISTIQUES DESCRIPTIVES DU DATASET")
    print("="*70)
    
    print(f"\nDimension du dataset: {dimension[0]} lignes x {dimension[1]} colonnes")
    
    print(f"\nLignes dupliquées: {data.duplicated().sum()} ({pct_dupliquees:.2f}%)")
    
    print("\nPourcentage de valeurs manquantes par colonne:")
    if pct_manquantes[pct_manquantes > 0].empty:
        print("  Aucune valeur manquante détectée")
    else:
        for col, pct in pct_manquantes[pct_manquantes > 0].items():
            print(f"  {col}: {pct:.2f}%")
    
    if qty_negative is not None:
        print(f"\nQuantités négatives: {qty_negative}")
    
    if commandes_annulees is not None:
        print(f"\nCommandes annulées (InvoiceNo commençant par 'C'): {commandes_annulees}")
    
    print("="*70)
    
    # Retourner un dictionnaire avec toutes les informations
    return {
        'dimension': dimension,
        'pct_valeurs_manquantes': pct_manquantes,
        'lignes_dupliquees': data.duplicated().sum(),
        'pct_lignes_dupliquees': pct_dupliquees,
        'quantites_negatives': qty_negative,
        'commandes_annulees': commandes_annulees
    }


# Exemple d'utilisation:
# stats = description(data)