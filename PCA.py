import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.preprocessing import MinMaxScaler
import streamlit as st
import plotly.express as px
from scipy.stats import bartlett
from factor_analyzer import calculate_kmo
from sklearn.decomposition import PCA
import numpy as np
from streamlit_echarts import st_echarts
import warnings

warnings.filterwarnings("ignore", message="The inverse of the variance-covariance matrix was calculated using the Moore-Penrose generalized matrix inversion")


def replace_NaN_values(df):
    
    knn_imputer = KNNImputer(n_neighbors=3)
    
    for column in df.columns:
        for geo, group in df.groupby(level='geo'):
            
            column_data = group[[column]].values
            imputed_column = knn_imputer.fit_transform(column_data)
            df.loc[(geo, slice(None)), column] = imputed_column
    
    df_imputed = df
    
    return df_imputed

def normalize_data(df):

    scaler = MinMaxScaler()
    
    df_scaled = pd.DataFrame(
        scaler.fit_transform(df),
        columns=df.columns,
        index=df.index
    )
    
    return df_scaled


def corr_matrix_plot(correlation_matrix):
    
    fig = px.imshow(
        correlation_matrix, 
        text_auto=True, 
        color_continuous_scale='RdBu_r',
        aspect="auto", 
        labels={'color': 'Correlation'} 
    )
    fig.update_layout(
        title='Correlation Matrix',
        title_x=0.5,
        width=800, 
        height=600 
    )

    st.plotly_chart(fig, use_container_width=True)

from factor_analyzer import calculate_bartlett_sphericity

def test_of_sphericity(correlation_matrix):
    
    chi_square_value, p_value = calculate_bartlett_sphericity(correlation_matrix)
    
    result = {
    "Statistic": ["Chi-Square Value", "P-Value"],
    "Value": [chi_square_value, p_value]
    }
    result_df = pd.DataFrame(result)

    st.table(result_df)
    

def KMO_measure(df):
    
    correlation_matrix = df.corr()

    kmo_all, kmo_model = calculate_kmo(correlation_matrix)
    
    st.write(f"Overall KMO: {kmo_model:.2f}")

    kmo_indicators = pd.Series(kmo_all, index=df.columns)
    kmo_df = pd.DataFrame(kmo_indicators, columns=['KMO']).reset_index()
    kmo_df.columns = ['Indicator', 'KMO']
    
    st.write("KMO for each Indicator:")
    st.table(kmo_df)


def principal_component_analysis(df):
    
    pca = PCA(n_components=4)
    pca.fit(df)

    eigenvalues = pca.explained_variance_
    explained_variance_ratio = pca.explained_variance_ratio_

    num_components = len(eigenvalues)
    
    results_df = pd.DataFrame({
        'Component': [f'PC{i+1}' for i in range(num_components)],
        'Eigenvalue': eigenvalues,
        'Proportion': explained_variance_ratio * 100,
    })
    results_df['Difference'] = results_df['Eigenvalue'].diff().fillna(0)
    results_df['Cumulative'] = results_df['Proportion'].cumsum()
    total_variance = np.sum(eigenvalues)
    results_df['PCw (%)'] = (results_df['Eigenvalue'] / total_variance) * 100
    results_df = results_df[['Component', 'Eigenvalue', 'Difference', 'Proportion', 'Cumulative', 'PCw (%)']]
    
    return results_df


def get_loadings_table(df):
    
    pca = PCA(n_components=4)
    pca.fit(df)

    loadings = pca.components_.T * np.sqrt(pca.explained_variance_)

    df_loadings = pd.DataFrame(loadings, columns=[f'μ{i+1}' for i in range(loadings.shape[1])], index=df.columns)
    st.table(df_loadings)


def get_final_ranking(df, pca_result_df):
    
    pca = PCA(n_components=4)
    pca.fit(df)
    
    eigenvalues = pca.explained_variance_
    
    num_components = len(eigenvalues)
    
    factor_scores = np.dot(df.values, pca.components_.T)
    factor_scores_df = pd.DataFrame(factor_scores, index=df.index, columns=[f'PC{i+1}' for i in range(num_components)])

    weights = pca_result_df['PCw (%)'].values[:num_components] / 100
    final_scores = np.dot(factor_scores_df.values, weights)
    final_scores_df = pd.DataFrame(final_scores, index=df.index, columns=['Final Score'])

    final_scores_df['region'] = final_scores_df.index.get_level_values('geo')
    final_scores_df['year'] = final_scores_df.index.get_level_values('time')

    region_ranks = final_scores_df.groupby('region')['Final Score'].mean().reset_index()
    region_ranks['Rank'] = region_ranks['Final Score'].rank(ascending=False)
    region_ranks = region_ranks.sort_values('Rank')
    
    geo_name = {
        "DEA2": "Cologne",
        "FI1B": "Helsinki",
        "SK03": "Zilina",
        "PT17": "Lisbon",
        "FR10": "Paris"
    }
    region_ranks['region'] = region_ranks['region'].replace(geo_name)
    
    color_mapping = {
        "Cologne": "#6272A4",
        "Helsinki": "#8BE9FD",
        "Zilina": "#FFB86C",
        "Lisbon": "#FF79C6",
        "Paris": "#BD93F9"
    }
    
    xaxis_list = region_ranks['region'].tolist() 
    yaxis_list = region_ranks['Final Score'].tolist()
    colors = [color_mapping[region] for region in xaxis_list] 

    series_data = [{"value": y, "itemStyle": {"color": c}} for y, c in zip(yaxis_list, colors)]
    
    option = {
        "title": {"text": "Ranking of InCITIES Observatory cities", "subtext": ""},
        "grid": {'top': '15%', 'right': '5%', 'bottom': '5%', 'left': '5%', 'containLabel': 'true'},
        "tooltip": {},
        "xAxis": {
            "type": 'value'
        },
        "yAxis": {
            "type": 'category',
            "data": xaxis_list
        },
        "series": [
            {
                "data": series_data,
                "type": 'bar',
                "orient": 'horizontal'
            }
        ]
    }
    
    st_echarts(options=option, height="500px")

from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt
    
def plot_dendogram(pivot_df, linkage_matrix):
    
    fig, ax = plt.subplots(figsize=(12, 8))
    dendrogram(linkage_matrix, labels=pivot_df.columns, orientation='top', leaf_rotation=90, ax=ax)
    ax.set_title('Hierarchical Clustering Dendrogram')
    ax.set_xlabel('Variables')
    ax.set_ylabel('Euclidean Distance')
    
    return fig

from scipy.cluster.hierarchy import fcluster

import seaborn as sns

def number_of_clusters(pivot_df, linkage_matrix):
    
    threshold = 4
    clusters = fcluster(linkage_matrix, threshold, criterion='distance')

    df = pd.DataFrame({'Variable': pivot_df.columns, 'Cluster': clusters})
    
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(pivot_df.T)

    df['PCA1'] = pca_result[:, 0]
    df['PCA2'] = pca_result[:, 1]

    plt.figure(figsize=(10, 8))
    sns.scatterplot(x='PCA1', y='PCA2', hue='Cluster', style='Cluster', data=df, palette='viridis', s=100)
    
    for i in range(df.shape[0]):
        plt.text(df.PCA1[i], df.PCA2[i], df.Variable[i], fontsize=9, alpha=0.7)

    plt.title('Distribution of Variables by Cluster')
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')
    plt.legend(title='Cluster')
    plt.grid()
    st.pyplot(plt)


def low_variance_filter(pivot_df):
    
    Z = 75  # Keeping variables contributing to 75% of the variance

    variances = pivot_df.var()
    sorted_variances = variances.sort_values(ascending=False)
    cumulative_variance = sorted_variances.cumsum() / sorted_variances.sum() * 100
    selected_variables = sorted_variances[cumulative_variance <= Z].index
    pivot_df_filtered = pivot_df[selected_variables]
    
    return pivot_df_filtered