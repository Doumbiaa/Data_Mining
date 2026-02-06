import io
import base64
import matplotlib.pyplot as plt
import networkx as nx

def fig_to_base64(fig):
    """Convertit un graphique Matplotlib en image encodée pour le Web."""
    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight', dpi=100)
    img.seek(0)
    plt.close(fig)
    return base64.b64encode(img.getvalue()).decode('utf-8')

def generate_support_plot(rules_df):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(rules_df['support'], bins=20, color='orange', edgecolor='black', alpha=0.7)
    ax.set_title("Distribution du Support")
    ax.set_xlabel("Support (Fréquence d'achat)")
    ax.set_ylabel("Nombre de règles")
    return fig_to_base64(fig)

def generate_lift_plot(rules_df):
    top_10 = rules_df.sort_values(by='lift', ascending=False).head(10).copy()
    top_10['label'] = top_10['antecedents'].apply(lambda x: ', '.join(list(x))[:25] + '...')
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top_10['label'], top_10['lift'], color='#28a745')
    ax.set_title("Top 10 : Force de l'association (Lift)")
    ax.invert_yaxis()
    return fig_to_base64(fig)

def generate_scatter_plot(rules_df):
    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(rules_df['support'], rules_df['confidence'], 
                         c=rules_df['lift'], cmap='viridis', s=100, alpha=0.7, edgecolor='k')
    plt.colorbar(scatter, ax=ax, label='Lift')
    ax.set_title("Support vs Confiance")
    ax.set_xlabel("Support")
    ax.set_ylabel("Confiance")
    ax.grid(True, linestyle='--', alpha=0.5)
    return fig_to_base64(fig)

def generate_network_plot(rules_df):
    rules_net = rules_df.sort_values(by='lift', ascending=False).head(15)
    G = nx.DiGraph()
    for _, row in rules_net.iterrows():
        ant = list(row['antecedents'])[0][:15]
        con = list(row['consequents'])[0][:15]
        G.add_edge(ant, con, weight=row['lift'])
    
    fig, ax = plt.subplots(figsize=(12, 10))
    pos = nx.spring_layout(G, k=1.5, seed=42)
    nx.draw_networkx_nodes(G, pos, node_color='#4834d4', node_size=1500, alpha=0.9, ax=ax)
    nx.draw_networkx_edges(G, pos, width=2, edge_color='#bdc3c7', arrowsize=25, 
                           arrowstyle='-|>', connectionstyle='arc3,rad=0.1', ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=9, font_weight='bold', ax=ax)
    plt.axis('off')
    return fig_to_base64(fig)