"""
Script para gerar as imagens ilustrativas do tutorial de PCA com Python.
Executa PCA no dataset de decatlo olímpico e salva os gráficos na pasta imagens/.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'imagens')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Carregar dados ---
url = 'https://raw.githubusercontent.com/nik-pi/Datasets/main/decathlon.csv'
df = pd.read_csv(url, index_col='Athlete')

# --- 1. Imagem: Dados originais em 2D (100m vs Long Jump) ---
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(df['100m'], df['Long Jump'], c='#37B6BD', s=80, alpha=0.7, edgecolors='white')
ax.set_xlabel('100m (s)', fontsize=12)
ax.set_ylabel('Salto em Distância (m)', fontsize=12)
ax.set_title('Dados Originais: 100m vs Salto em Distância', fontsize=14, weight='bold')
ax.spines[['right', 'top']].set_visible(False)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '01_dados_originais_2d.png'), dpi=150, bbox_inches='tight')
plt.close()

# --- Escalar dados ---
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df)

# --- 2. Imagem: Autovetores sobre dados centrados ---
pca_full = PCA()
pca_full.fit(scaled_data)

fig, ax = plt.subplots(figsize=(8, 6))
# Projetar em 2 primeiras colunas (100m e 110m Hurdle) apenas para visualização
ax.scatter(scaled_data[:, 0], scaled_data[:, 1], c='#AAD8D3', s=80, alpha=0.7, edgecolors='gray')

mean = np.mean(scaled_data[:, :2], axis=0)
for i, (evec, eval_) in enumerate(zip(pca_full.components_[:2, :2], pca_full.explained_variance_[:2])):
    ax.annotate('', xy=mean + evec * np.sqrt(eval_) * 2,
                xytext=mean,
                arrowprops=dict(arrowstyle='->', color='#E74C3C' if i == 0 else '#3498DB', lw=3))
    ax.text(mean[0] + evec[0] * np.sqrt(eval_) * 2.2,
            mean[1] + evec[1] * np.sqrt(eval_) * 2.2,
            f'PC{i+1}', fontsize=14, weight='bold',
            color='#E74C3C' if i == 0 else '#3498DB')

ax.set_xlabel('100m (padronizado)', fontsize=12)
ax.set_ylabel('110m Barreiras (padronizado)', fontsize=12)
ax.set_title('Autovetores (Componentes Principais)', fontsize=14, weight='bold')
ax.spines[['right', 'top']].set_visible(False)
ax.grid(True, alpha=0.3)
ax.set_aspect('equal')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '02_autovetores.png'), dpi=150, bbox_inches='tight')
plt.close()

# --- 3. Imagem: Variância Explicada ---
expl_var = pca_full.explained_variance_ratio_
df_expl_var = pd.DataFrame(
    data=zip(range(1, len(expl_var) + 1), expl_var, expl_var.cumsum()),
    columns=['PC', 'Variância Explicada (%)', 'Variância Acumulada (%)']
).set_index('PC').mul(100).round(1)

fig, ax = plt.subplots(figsize=(9, 6))
bars = ax.bar(x=df_expl_var.index, height=df_expl_var['Variância Explicada (%)'],
              label='Variância Explicada', width=0.8, color='#AAD8D3', edgecolor='gray')
ax.plot(df_expl_var.index, df_expl_var['Variância Acumulada (%)'],
        label='Variância Acumulada', marker='o', c='#37B6BD', lw=2.5, markersize=8)
ax.axhline(y=80, color='#E74C3C', linestyle='--', alpha=0.6, label='Limiar 80%')
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 1,
            f'{height:.1f}%', ha='center', va='bottom', fontsize=9)
ax.set_ylim(0, 110)
ax.set_ylabel('Variância Explicada (%)', fontsize=12)
ax.set_xlabel('Componente Principal', fontsize=12)
ax.set_title('Variância Explicada por Componente Principal', fontsize=14, weight='bold')
ax.legend(fontsize=10)
ax.grid(True, axis='y', alpha=0.3)
ax.spines[['right', 'top']].set_visible(False)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '03_variancia_explicada.png'), dpi=150, bbox_inches='tight')
plt.close()

# --- 4. Imagem: Heatmap de Loadings ---
pca2 = PCA(n_components=2)
X_r = pca2.fit_transform(scaled_data)

fig, ax = plt.subplots(figsize=(10, 4))
sns.heatmap(
    pca2.components_,
    cmap='coolwarm',
    yticklabels=[f'PC{x}' for x in range(1, pca2.n_components_ + 1)],
    xticklabels=list(df.columns),
    linewidths=1,
    annot=True,
    fmt=',.2f',
    cbar_kws={"shrink": 0.8, "orientation": 'horizontal'},
    ax=ax
)
ax.set_aspect("equal")
ax.set_title('Pesos (Loadings) por Variável e Componente', fontsize=14, weight='bold')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '04_heatmap_loadings.png'), dpi=150, bbox_inches='tight')
plt.close()

# --- 5. Imagem: Scatterplot dos Loadings ---
loadings = pd.DataFrame(
    pca2.components_.T,
    columns=['PC1', 'PC2'],
    index=df.columns
)

fig, ax = plt.subplots(figsize=(10, 8))
ax.scatter(x=loadings['PC1'], y=loadings['PC2'], c='#37B6BD', s=100, zorder=5)
ax.axvline(x=0, c="gray", lw=0.8, linestyle='--')
ax.axhline(y=0, c="gray", lw=0.8, linestyle='--')
for label, x_val, y_val in zip(loadings.index, loadings['PC1'], loadings['PC2']):
    ax.annotate(label, (x_val, y_val), textcoords="offset points",
                xytext=(0, 12), ha='center', fontsize=10, weight='bold')
ax.set_xlabel('PC1', fontsize=12)
ax.set_ylabel('PC2', fontsize=12)
ax.set_title('Correlação entre Variáveis nos Componentes Principais', fontsize=14, weight='bold')
ax.spines[['right', 'top']].set_visible(False)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '05_scatterplot_loadings.png'), dpi=150, bbox_inches='tight')
plt.close()

# --- 6. Imagem: Dados transformados por PCA ---
X_r_df = pd.DataFrame(X_r, columns=['PC1', 'PC2'], index=df.index)

fig, ax = plt.subplots(figsize=(10, 8))
sns.scatterplot(data=X_r_df, x='PC1', y='PC2', ax=ax, s=120, alpha=0.7, color='#37B6BD', edgecolor='white')
for label, row in X_r_df.iterrows():
    ax.annotate(label, (row['PC1'], row['PC2']),
                textcoords="offset points", xytext=(5, 5),
                fontsize=7, alpha=0.8)
ax.set_title('Atletas Projetados nos Componentes Principais', fontsize=14, weight='bold')
ax.set_xlabel('Componente Principal 1', fontsize=12)
ax.set_ylabel('Componente Principal 2', fontsize=12)
ax.spines[['right', 'top']].set_visible(False)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '06_dados_transformados_pca.png'), dpi=150, bbox_inches='tight')
plt.close()

# --- 7. Imagem: Diagrama conceitual das etapas do PCA ---
fig, ax = plt.subplots(figsize=(12, 3))
ax.set_xlim(0, 10)
ax.set_ylim(0, 2)
ax.axis('off')

etapas = [
    ('1. Centralizar\nDados', '#3498DB'),
    ('2. Matriz de\nCovariância', '#2ECC71'),
    ('3. Decomposição\nEigenvalues', '#E67E22'),
    ('4. Selecionar\nComponentes', '#9B59B6'),
    ('5. Projetar\nDados', '#E74C3C'),
]

for i, (txt, cor) in enumerate(etapas):
    x = 1 + i * 2
    rect = plt.Rectangle((x - 0.8, 0.3), 1.6, 1.2, facecolor=cor, alpha=0.85,
                          edgecolor='white', linewidth=2, zorder=2)
    ax.add_patch(rect)
    ax.text(x, 0.9, txt, ha='center', va='center', fontsize=10,
            weight='bold', color='white', zorder=3)
    if i < len(etapas) - 1:
        ax.annotate('', xy=(x + 1.0, 0.9), xytext=(x + 0.85, 0.9),
                    arrowprops=dict(arrowstyle='->', color='gray', lw=2))

ax.set_title('Etapas da Análise de Componentes Principais (PCA)', fontsize=14, weight='bold', pad=10)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '07_etapas_pca.png'), dpi=150, bbox_inches='tight')
plt.close()

print("✓ Todas as 7 imagens foram geradas com sucesso na pasta imagens/")
for f in sorted(os.listdir(OUTPUT_DIR)):
    if f.endswith('.png'):
        print(f"  - {f}")
