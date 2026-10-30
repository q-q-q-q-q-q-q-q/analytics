import pandas as pd
from sqlalchemy import create_engine

DB_URL = 'postgresql://postgres:mysecretpassword@localhost:5432/postgres'
engine = create_engine(DB_URL)

try:

    print("Чтение данных из CSV")
    df = pd.read_csv('ecommerce_events.csv')

    print("Трансформация данных")
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])


    df = df.sort_values(by=['UserID', 'SessionID', 'Timestamp']).reset_index(drop=True)


    df['ProductID'] = df['ProductID'].fillna('unknown')
    df['Amount'] = df['Amount'].fillna(0)

    df.columns = ['user_id', 'session_id', 'timestamp', 'event_type', 'product_id', 'amount', 'outcome']

    print("Загрузка в PostgreSQL")
    # if_exists='replace' перезапишет таблицу, если вы запустите скрипт второй раз
    df.to_sql('raw_events', engine, if_exists='replace', index=False)

    print(f"Успешно загружено {len(df)} строк в таблицу 'raw_events'!")

except Exception as e:
    print(f"Ошибка: {e}")