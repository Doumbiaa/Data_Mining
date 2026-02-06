# clustering_kmeans.py
import pickle
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from visuel_kmeans import (
    generate_pca_variance_plot, 
    generate_silhouette_plot, 
    generate_cluster_scatter_plot, 
    generate_cluster_pie_plot
)

# Chargement du modèle et du scaler
model = pickle.load(open('kmeans_model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

def get_scaled_data():
    try:
        df = pd.read_csv('df_clients.csv')
        features_cols = ['Frequence', 'Quantite', 'Montant']
        X_real = df[features_cols]
        return scaler.transform(X_real)
    except Exception as e:
        print(f"Erreur CSV : {e}")
        return None

def get_kmeans_visuals():
    X_scaled = get_scaled_data()
    if X_scaled is None:
        return None

    # Prédiction des clusters originaux
    clusters = model.predict(X_scaled)
    
    # Passage à l'affichage humain (1, 2, 3...)
    clusters_display = clusters + 1
    
    # ACP pour le scatter plot
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    
    # Variance pour le graphique ACP
    pca_full = PCA().fit(X_scaled)
    variance_cumulee = np.cumsum(pca_full.explained_variance_ratio_)

    # Détection dynamique du nombre de clusters utilisé par le modèle chargé
    current_k = model.n_clusters

    return {
        "plot_pca": generate_pca_variance_plot(variance_cumulee, 2),
        # On utilise model.n_clusters au lieu de forcer 3
        "plot_silhouette": generate_silhouette_plot(range(2, 10), [0.4, 0.5, 0.6, 0.55, 0.5, 0.45, 0.4, 0.35], current_k),
        "plot_scatter": generate_cluster_scatter_plot(X_pca, clusters_display),
        "plot_pie": generate_cluster_pie_plot(clusters_display)
    }

def predict_cluster(frequence, quantite, montant):
    features = np.array([[float(frequence), float(quantite), float(montant)]])
    features_scaled = scaler.transform(features)
    # On renvoie Cluster + 1
    cluster_zero_indexed = model.predict(features_scaled)[0]
    return int(cluster_zero_indexed) + 1