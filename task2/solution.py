import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def task2():
    # Загрузка данных
    transactions = pd.read_csv('data/transactions.csv', nrows=1000000)
    tr_mcc_codes = pd.read_csv('data/tr_mcc_codes.csv', sep=';')
    tr_types = pd.read_csv('data/tr_types.csv', sep=';')
    customers_gender_train = pd.read_csv('data/gender_train.csv')

    # Соединение таблиц
    df = pd.merge(transactions, customers_gender_train, on='customer_id', how='left')
    df = pd.merge(df, tr_mcc_codes, on='mcc_code', how='inner')
    df = pd.merge(df, tr_types, on='tr_type', how='inner')

    # Создание нового столбца
    df['mcc_code+tr_type'] = df['mcc_code'].astype(str) + df['tr_type'].astype(str)

    # Фильтрация положительных сумм
    df = df[df['amount'] > 0]

    # Группировка и фильтрация
    grouped = df.groupby('mcc_code+tr_type').agg(
        mean_amount=('amount', 'mean'),
        count=('amount', 'count')
    ).reset_index()

    filtered = grouped[(grouped['count'] >= 5) & (grouped['count'] <= 35)]

    # Построение графика ядерной оценки плотности
    plt.figure(figsize=(10, 6))
    sns.kdeplot(filtered['mean_amount'], fill=True)
    plt.title('Ядерная оценка плотности средних значений сумм транзакций')
    plt.xlabel('Средняя сумма транзакции')
    plt.ylabel('Плотность')
    plt.grid(True)
    plt.show()