import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# 1. Carregando o dataset nativo para garantir execução universal imediata

data = load_breast_cancer()

X = pd.DataFrame(data.data, columns=data.feature_names)

y = data.target  # 0: Maligno, 1: Benigno

# 2. Divisão da base de dados em Treinamento (70%) e Teste (30%)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 3. Criação e Treinamento do Modelo (CART)

# max_depth=3 foi definido para manter a árvore legível e as regras apresentáveis

clf = DecisionTreeClassifier(criterion='gini', max_depth=3, random_state=42)

clf.fit(X_train, y_train)

# 4. Previsões

y_pred = clf.predict(X_test)

# 5. Avaliação e Métricas

print("="*50)

print("MÉTRICAS DE DESEMPENHO (Base de Teste)")

print("="*50)

print(f"Acurácia : {accuracy_score(y_test, y_pred):.4f}")

print(f"Precision: {precision_score(y_test, y_pred):.4f}")

print(f"Recall   : {recall_score(y_test, y_pred):.4f}")

print(f"F1-Score : {f1_score(y_test, y_pred):.4f}")

# 6. Extração das Regras

print("\n" + "="*50)

print("REGRAS DA ÁRVORE DE DECISÃO (CART)")

print("="*50)

regras = export_text(clf, feature_names=list(X.columns))

print(regras)