import pandas as pd

def task1():
    # Шаг 1. Загрузка данных
    transactions = pd.read_csv('data/transactions.csv', nrows=1000000)
    tr_mcc_codes = pd.read_csv('data/tr_mcc_codes.csv', sep=';')
    tr_types = pd.read_csv('data/tr_types.csv', sep=';')
    customers_gender_train = pd.read_csv('data/gender_train.csv')

    print(f"transactions: {len(transactions)} строк")  # ожидается 1_000_000
    print(f"gender_train: {len(customers_gender_train)} строк")
    print(f"tr_mcc_codes: {len(tr_mcc_codes)} строк")
    print(f"tr_types: {len(tr_types)} строк")

    # Шаг 2. Объединение с gender_train (left join)
    df = pd.merge(transactions, customers_gender_train, on='customer_id', how='left')
    print(f"После merge с gender_train (left): {len(df)} строк")

    # Шаг 3. Объединение с tr_mcc_codes (inner join)
    mcc_match = df['mcc_code'].isin(tr_mcc_codes['mcc_code'])
    print(f"mcc_code совпадает у: {mcc_match.sum()} строк")
    df = df[mcc_match]
    df = pd.merge(df, tr_mcc_codes, on='mcc_code', how='inner')
    print(f"После merge с tr_mcc_codes (inner): {len(df)} строк")

    # Шаг 4. Объединение с tr_types (inner join)
    type_match = df['tr_type'].isin(tr_types['tr_type'])
    print(f"tr_type совпадает у: {type_match.sum()} строк")
    df = df[type_match]
    df = pd.merge(df, tr_types, on='tr_type', how='inner')
    print(f"После merge с tr_types (inner): {len(df)} строк")

    # 🔐 Проверка на соответствие условию
    expected_rows = 999584
    if len(df) != expected_rows:
        print(f"ВНИМАНИЕ: ожидалось {expected_rows} строк, получено: {len(df)}")
    else:
        print("Количество строк совпадает с условием задачи!")

    # Шаг 5. Новый столбец через .astype(str)
    df['mcc_code+tr_type'] = df['mcc_code'].astype(str) + df['tr_type'].astype(str)

    # Шаг 6. Фильтрация положительных значений
    df = df[df['amount'] > 0]

    # Шаг 7. Группировка и агрегация
    grouped = df.groupby('mcc_code+tr_type').agg(
        mean_amount=('amount', 'mean'),
        count=('amount', 'count')
    ).reset_index()

    filtered = grouped[(grouped['count'] >= 5) & (grouped['count'] <= 35)]

    # Шаг 8. Вывод результата
    result = filtered['mean_amount'].mean()
    result_rounded = round(result, 2)
    print(f"Результат: {result_rounded}")

    return result_rounded
