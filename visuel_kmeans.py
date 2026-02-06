# visuel_kmeans.py
import io
import base64
import matplotlib.pyplot as plt
import numpy as np

def fig_to_base64(fig):
    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight', dpi=100)
    img.seek(0)
    plt.close(fig)
    return base64.b64encode(img.getvalue()).decode('utf-8')

def generate_pca_variance_plot(variance_cumulee, n_comp_95):
    fig, ax = plt.subplots(figsize=(8,5))
    ax.plot(variance_cumulee, marker='o', color='#2c3e50', linewidth=2)
    ax.axhline(y=0.95, color='red', linestyle='--', label='Seuil 95%')
    ax.set_title("Analyse ACP - Variance Expliquée", fontweight='bold')
    ax.set_xlabel("Nombre de composantes")
    ax.set_ylabel("Ratio de variance cumulé")
    ax.legend()
    ax.grid(True, alpha=0.3)
    return fig_to_base64(fig)

def generate_silhouette_plot(k_range, scores, best_k):
    fig, ax = plt.subplots(figsize=(8,5))
    ax.plot(k_range, scores, marker='o', color='#e67e22', linewidth=2)
    ax.axvline(x=best_k, color='red', linestyle='--', label=f"K optimal sélectionné = {best_k}")
    ax.set_title("Méthode de la Silhouette", fontweight='bold')
    ax.set_xlabel("Nombre de clusters (k)")
    ax.set_ylabel("Score de Silhouette")
    ax.legend()
    ax.grid(True, alpha=0.3)
    return fig_to_base64(fig)

def generate_cluster_scatter_plot(X_pca, clusters):
    fig, ax = plt.subplots(figsize=(8,6))
    
    # On définit des couleurs fixes pour éviter toute confusion
    colors = ['#FF5733', '#33FF57', '#3357FF'] 
    unique_clusters = sorted(np.unique(clusters))
    
    for i, cluster_id in enumerate(unique_clusters):
        mask = (clusters == cluster_id)
        ax.scatter(X_pca[mask, 0], X_pca[mask, 1], 
                   label=f'Cluster {int(cluster_id)}', 
                   c=colors[i % len(colors)], 
                   alpha=0.7, edgecolors='w', s=60)

    ax.set_title("Projection spatiale des Segments (PCA)", fontweight='bold')
    ax.set_xlabel("Composante Principale 1")
    ax.set_ylabel("Composante Principale 2")
    ax.legend(title="Segments")
    ax.grid(True, alpha=0.2)
    return fig_to_base64(fig)

def generate_cluster_pie_plot(clusters):
    fig, ax = plt.subplots(figsize=(6,6))
    unique, counts = np.unique(clusters, return_counts=True)
    
    # Couleurs pastels pour le camembert
    colors = ['#ff9999','#66b3ff','#99ff99']
    
    ax.pie(counts, 
           labels=[f'Cluster {int(i)}' for i in unique], 
           autopct='%1.1f%%', 
           startangle=140, 
           colors=colors,
           explode=[0.05] * len(unique), # Détache légèrement les parts
           shadow=True)
    
    ax.set_title("Répartition des segments clients", fontweight='bold')
    return fig_to_base64(fig)