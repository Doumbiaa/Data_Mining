from flask import Flask, render_template, request, jsonify, redirect, url_for
import pickle
import os
import pandas as pd
import numpy as np

# --- IMPORTS DE VOS MODULES PERSONNALISÉS ---
from recommender import get_recommendations
from visuel_apriori import (generate_lift_plot, generate_network_plot, 
                            generate_support_plot, generate_scatter_plot)

from customer_segment import get_rfm_data, get_client_info
from visuel_rfm import (generate_recence_montant_plot, generate_frequence_montant_plot, 
                        generate_segment_distribution_plot, generate_heatmap_rf_plot)

# Import du module K-Means que nous avons créé
import clustering_kmeans as ck 

app = Flask(__name__)

# --- CHARGEMENT DES MODÈLES (APRIORI) ---
rules = None
if os.path.exists('rules.pkl'):
    with open('rules.pkl', 'rb') as f:
        rules = pickle.load(f)

# --- ROUTES ---

# 1. Page d'accueil principale (Ne pas toucher)
@app.route('/')
def home():
    return render_template('index.html')

# 2. Système de Recommandation (Apriori)
@app.route('/recommandation', methods=['GET', 'POST'])
def index_apriori():
    recommendations = None
    query = ""
    if request.method == 'POST':
        query = request.form.get('product', '').upper().strip()
        if rules is not None and query != "":
            recommendations = get_recommendations(query, rules)
    return render_template('index_apriori.html', query=query, recos=recommendations)

@app.route('/visualisation_apriori')
def visualisation_apriori():
    if rules is None:
        return "Modèle Apriori introuvable."
    return render_template('visualisation_apriori.html', 
                           plot_support=generate_support_plot(rules), 
                           plot_lift=generate_lift_plot(rules), 
                           plot_network=generate_network_plot(rules),
                           plot_scatter=generate_scatter_plot(rules))

# 3. Segmentation Clients (RFM classique)
@app.route('/rfm', methods=['GET', 'POST'])
def index_rfm():
    rfm_df = get_rfm_data()
    client_info = None
    customer_id = ""
    if request.method == 'POST':
        customer_id = request.form.get('customer_id', '').strip()
        if rfm_df is not None:
            client_info = get_client_info(customer_id, rfm_df)
    return render_template('index_rfm.html', info=client_info, cid=customer_id)

@app.route('/visualisation_rfm')
def visualisation_rfm():
    rfm_df = get_rfm_data()
    if rfm_df is None: return "Données RFM introuvables."
    return render_template('visualisation_rfm.html', 
                           plot_rec_mon=generate_recence_montant_plot(rfm_df),
                           plot_freq_mon=generate_frequence_montant_plot(rfm_df),
                           plot_dist=generate_segment_distribution_plot(rfm_df),
                           plot_heatmap=generate_heatmap_rf_plot(rfm_df))

# 4. Clustering IA (K-Means)
# Route pour le formulaire de prédiction individuelle
@app.route('/kmeans')
def index_kmeans():
    return render_template('index_kmeans.html')

# Route API pour traiter la prédiction du formulaire K-Means
@app.route('/predict', methods=['POST'])
def predict_kmeans():
    try:
        data = request.get_json()
        # Appel de la fonction dans clustering_kmeans.py
        cluster = ck.predict_cluster(data['frequence'], data['quantite'], data['montant'])
        return jsonify({
            'success': True,
            'message': f"Le client appartient au Segment {cluster}"
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# Route pour les graphiques techniques K-Means
@app.route('/visualisation_kmeans')
def visualisation_kmeans():
    # Appel de la fonction de récupération des visuels (PCA, Pie, etc.)
    plots = ck.get_kmeans_visuals()
    if plots is None:
        return "Erreur lors de la génération des visuels K-Means."
    
    # On passe le dictionnaire de plots au template
    return render_template('visualisation_kmeans.html', **plots)

if __name__ == '__main__':
    app.run(debug=True)