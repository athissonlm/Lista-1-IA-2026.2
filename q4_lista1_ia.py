import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.metrics import accuracy_score, classification_report

# 1. Carregando a base de dados nativa
data = load_breast_cancer()
df = pd.DataFrame(data.data, columns=data.feature_names)
df['Diagnostico_Real'] = data.target  # 0: Maligno, 1: Benigno

# 2. Definindo a Base de Regras (Extraída via RIPPER)
def classificar_tumor(instancia):
    """
    Classifica o tumor avaliando as regras lógicas em cascata.
    """
    # Regra 1
    if instancia['worst perimeter'] <= 105.9 and instancia['worst concave points'] <= 0.14:
        return 1  # Classe 1 (Benigno)
        
    # Regra 2
    elif instancia['mean concave points'] <= 0.05 and instancia['worst radius'] <= 16.22 and instancia['area error'] <= 32.74:
        return 1  # Classe 1 (Benigno)
        
    # Regra 3
    elif instancia['worst texture'] <= 25.04 and instancia['worst area'] <= 844.4:
        return 1  # Classe 1 (Benigno)
        
    # Regra 4 (Fallback default)
    else:
        return 0  # Classe 0 (Maligno)
    
# O df.apply() percorre o DataFrame inteiro passando cada linha (axis=1) para a nossa função
df['Previsao_Regras'] = df.apply(classificar_tumor, axis=1)

# 4. Avaliando os resultados
print("\n" + "="*50)
print("MÉTRICAS DO SISTEMA")
print("="*50)
acuracia = accuracy_score(df['Diagnostico_Real'], df['Previsao_Regras'])
print(f"Acurácia Geral : {acuracia:.4f} ({acuracia*100:.2f}%)\n")

print("Relatório de Classificação Detalhado:")
print(classification_report(df['Diagnostico_Real'], df['Previsao_Regras'], target_names=['Maligno (0)', 'Benigno (1)']))

# 5. Mostrando uma amostra visual do DataFrame para comprovação
print("="*50)
print("AMOSTRA DOS DADOS: DIAGNÓSTICO REAL vs PREVISÃO DA REGRA")
print("="*50)
# Selecionamos apenas as colunas que importam para as regras e os resultados
colunas_visuais = [
    'worst perimeter', 
    'worst concave points', 
    'mean concave points', 
    'Diagnostico_Real', 
    'Previsao_Regras'
]

# Exibe 10 linhas aleatórias da tabela para você ver a regra funcionando na prática
print(df[colunas_visuais].sample(10, random_state=42).to_string())