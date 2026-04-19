"""
Script para gerar as imagens ilustrativas do tutorial sobre Correlações
(Pearson, Kendall e Spearman) e Matriz de Correlograma.

Executa análises de correlação no dataset de decatlo olímpico e salva os
gráficos na pasta imagens/.
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'imagens')
os.makedirs(OUTPUT_DIR, exist_ok=True)

sns.set_style('whitegrid')
RNG = np.random.default_rng(42)

# --- Carregar dados ---
url = 'https://raw.githubusercontent.com/nik-pi/Datasets/main/decathlon.csv'
df = pd.read_csv(url, index_col='Athlete')

# =============================================================================
# 1. Tipos de Relação (linear, monotônica não-linear, não-monotônica)
# =============================================================================
n = 80
x = np.linspace(0, 10, n)

# Linear (com ruído)
y_linear = 2 * x + 3 + RNG.normal(0, 2, n)
# Monotônica não-linear (exponencial crescente)
y_mono = np.exp(x / 2) + RNG.normal(0, 5, n)
# Não-monotônica (parabólica)
y_nmono = (x - 5) ** 2 + RNG.normal(0, 2, n)

datasets = [
    ('Relação Linear', x, y_linear, '#37B6BD'),
    ('Monotônica Não-Linear', x, y_mono, '#E67E22'),
    ('Não-Monotônica', x, y_nmono, '#9B59B6'),
]

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
for ax, (titulo, xs, ys, cor) in zip(axes, datasets):
    r_p, _ = stats.pearsonr(xs, ys)
    r_k, _ = stats.kendalltau(xs, ys)
    r_s, _ = stats.spearmanr(xs, ys)
    ax.scatter(xs, ys, c=cor, alpha=0.75, edgecolors='white', s=70)
    ax.set_title(titulo, fontsize=13, weight='bold')
    ax.set_xlabel('X', fontsize=11)
    ax.set_ylabel('Y', fontsize=11)
    ax.text(
        0.03, 0.97,
        f'Pearson  r = {r_p:+.2f}\nKendall  τ = {r_k:+.2f}\nSpearman ρ = {r_s:+.2f}',
        transform=ax.transAxes, va='top', ha='left',
        fontsize=11, family='monospace',
        bbox=dict(boxstyle='round,pad=0.4', fc='white', ec='gray', alpha=0.9),
    )
    ax.spines[['right', 'top']].set_visible(False)

fig.suptitle('Como cada coeficiente reage a diferentes tipos de relação',
             fontsize=14, weight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '01_tipos_relacoes.png'),
            dpi=150, bbox_inches='tight')
plt.close()

# =============================================================================
# 2-4. Correlogramas individuais (Pearson, Kendall, Spearman)
# =============================================================================
metodos = [
    ('pearson', 'Correlograma — Pearson (r)', '02_correlograma_pearson.png'),
    ('kendall', 'Correlograma — Kendall (τ)', '03_correlograma_kendall.png'),
    ('spearman', 'Correlograma — Spearman (ρ)', '04_correlograma_spearman.png'),
]

matrizes = {}
for metodo, titulo, nome_arq in metodos:
    corr = df.corr(method=metodo)
    matrizes[metodo] = corr

    # Máscara para esconder o triângulo superior (redundante)
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)

    fig, ax = plt.subplots(figsize=(9, 7.5))
    sns.heatmap(
        corr, mask=mask, cmap='coolwarm', center=0, vmin=-1, vmax=1,
        annot=True, fmt='.2f', linewidths=0.5, square=True,
        cbar_kws={'shrink': 0.75, 'label': 'Coeficiente'}, ax=ax,
    )
    ax.set_title(titulo, fontsize=14, weight='bold', pad=12)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, nome_arq),
                dpi=150, bbox_inches='tight')
    plt.close()

# =============================================================================
# 5. Comparação lado a lado dos três correlogramas
# =============================================================================
fig, axes = plt.subplots(1, 3, figsize=(20, 6.5))
for ax, (metodo, titulo, _) in zip(axes, metodos):
    corr = matrizes[metodo]
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
    sns.heatmap(
        corr, mask=mask, cmap='coolwarm', center=0, vmin=-1, vmax=1,
        annot=True, fmt='.2f', linewidths=0.5, square=True,
        cbar=False, annot_kws={'size': 8}, ax=ax,
    )
    ax.set_title(titulo.split('—')[-1].strip(), fontsize=13, weight='bold')
    ax.tick_params(axis='x', rotation=45)
    ax.tick_params(axis='y', rotation=0)
    for lbl in ax.get_xticklabels():
        lbl.set_horizontalalignment('right')

fig.suptitle('Comparação: Pearson × Kendall × Spearman',
             fontsize=15, weight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '05_comparacao_correlogramas.png'),
            dpi=150, bbox_inches='tight')
plt.close()

# =============================================================================
# 6. Diferença absoluta |Pearson - Spearman| (detecta não-linearidades)
# =============================================================================
diff = (matrizes['pearson'] - matrizes['spearman']).abs()
mask = np.triu(np.ones_like(diff, dtype=bool), k=1)

fig, ax = plt.subplots(figsize=(9, 7.5))
sns.heatmap(
    diff, mask=mask, cmap='magma_r', vmin=0, vmax=max(0.3, diff.values.max()),
    annot=True, fmt='.2f', linewidths=0.5, square=True,
    cbar_kws={'shrink': 0.75, 'label': '|r_Pearson − ρ_Spearman|'}, ax=ax,
)
ax.set_title('Divergência entre Pearson e Spearman\n(valores altos sugerem relações não-lineares ou outliers)',
             fontsize=13, weight='bold', pad=12)
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '06_diferenca_pearson_spearman.png'),
            dpi=150, bbox_inches='tight')
plt.close()

# =============================================================================
# 7. Quarteto de Anscombe — limites da correlação de Pearson
# =============================================================================
anscombe = {
    'I':   (np.array([10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]),
            np.array([8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68])),
    'II':  (np.array([10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]),
            np.array([9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74])),
    'III': (np.array([10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]),
            np.array([7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73])),
    'IV':  (np.array([8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8]),
            np.array([6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89])),
}

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
for ax, (nome, (xs, ys)) in zip(axes.flat, anscombe.items()):
    r_p, _ = stats.pearsonr(xs, ys)
    r_k, _ = stats.kendalltau(xs, ys)
    r_s, _ = stats.spearmanr(xs, ys)
    ax.scatter(xs, ys, c='#37B6BD', s=90, alpha=0.85, edgecolors='white')
    # Linha de regressão
    m, b = np.polyfit(xs, ys, 1)
    xr = np.linspace(xs.min(), xs.max(), 50)
    ax.plot(xr, m * xr + b, color='#E74C3C', lw=1.8, alpha=0.8)
    ax.set_title(f'Conjunto {nome}', fontsize=13, weight='bold')
    ax.text(
        0.03, 0.97,
        f'Pearson  r = {r_p:+.2f}\nKendall  τ = {r_k:+.2f}\nSpearman ρ = {r_s:+.2f}',
        transform=ax.transAxes, va='top', ha='left',
        fontsize=10, family='monospace',
        bbox=dict(boxstyle='round,pad=0.4', fc='white', ec='gray', alpha=0.9),
    )
    ax.set_xlabel('X'); ax.set_ylabel('Y')
    ax.spines[['right', 'top']].set_visible(False)

fig.suptitle('Quarteto de Anscombe — a mesma Pearson, histórias diferentes',
             fontsize=15, weight='bold', y=1.00)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '07_anscombe.png'),
            dpi=150, bbox_inches='tight')
plt.close()

print("✓ Imagens de correlação geradas com sucesso em:", OUTPUT_DIR)
for f in sorted(os.listdir(OUTPUT_DIR)):
    if f.endswith('.png') and ('correlograma' in f or 'tipos_relacoes' in f
                                or 'comparacao_correlogramas' in f
                                or 'diferenca_pearson' in f or 'anscombe' in f):
        print(f"  - {f}")
