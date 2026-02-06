import io
import base64
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

def fig_to_base64(fig):
    """Convertit un graphique Matplotlib en image encodée pour le Web."""
    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight', dpi=100)
    img.seek(0)
    plt.close(fig)
    return base64.b64encode(img.getvalue()).decode('utf-8')

def generate_recence_montant_plot(rfm):
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(rfm["Recence"], rfm["Montant"], alpha=0.5, color='#3498db')
    ax.set_xlabel("Récence")
    ax.set_ylabel("Montant")
    ax.set_title("Récence vs Montant")
    ax.grid(True, linestyle='--', alpha=0.6)
    return fig_to_base64(fig)

def generate_frequence_montant_plot(rfm):
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(rfm["Frequence"], rfm["Montant"], alpha=0.5, color='#2ecc71')
    ax.set_xlabel("Fréquence")
    ax.set_ylabel("Montant")
    ax.set_title("Fréquence vs Montant")
    ax.grid(True, linestyle='--', alpha=0.6)
    return fig_to_base64(fig)

def generate_segment_distribution_plot(rfm):
    fig, ax = plt.subplots(figsize=(8, 5))
    counts = rfm["Segment"].value_counts().sort_values()
    
    # Création d'une palette de couleurs avec matplotlib
    colors = cm.viridis(np.linspace(0, 1, len(counts)))
    
    counts.plot(kind="barh", ax=ax, color=colors)
    ax.set_title("Répartition des segments RFM")
    ax.set_xlabel("Nombre de clients")
    return fig_to_base64(fig)

def generate_heatmap_rf_plot(rfm):
    pivot_rf = rfm.pivot_table(
        index="R_Score",
        columns="F_Score",
        values="Montant",
        aggfunc="mean"
    ).fillna(0) # On remplace les vides par 0

    fig, ax = plt.subplots(figsize=(7, 6))
    
    # Utilisation de imshow pour simuler une heatmap
    im = ax.imshow(pivot_rf, cmap="YlGnBu", aspect='auto')
    
    # Ajouter les labels sur les axes
    ax.set_xticks(np.arange(len(pivot_rf.columns)))
    ax.set_yticks(np.arange(len(pivot_rf.index)))
    ax.set_xticklabels(pivot_rf.columns)
    ax.set_yticklabels(pivot_rf.index)
    
    # Ajouter les valeurs numériques à l'intérieur (Annotations)
    for i in range(len(pivot_rf.index)):
        for j in range(len(pivot_rf.columns)):
            text = ax.text(j, i, int(pivot_rf.iloc[i, j]),
                           ha="center", va="center", color="black", fontsize=9)

    ax.set_title("Heatmap R vs F (Montant moyen)")
    ax.set_xlabel("F_Score")
    ax.set_ylabel("R_Score")
    fig.colorbar(im, ax=ax, label="Montant moyen (€)")
    
    return fig_to_base64(fig)