import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from scipy.stats import chi2_contingency

# 1. Подключение к базе данных
DB_URL = 'postgresql://postgres:mysecretpassword@localhost:5432/postgres'
engine = create_engine(DB_URL)

print("Извлечение пользователей из БД...")
# Запрашиваем уникальных пользователей из нашей таблицы
query = "SELECT DISTINCT user_id FROM raw_events"
df_users = pd.read_sql(query, engine)

if df_users.empty:
    print("Таблица raw_events пуста. Сначала запустите etl.py")
    exit()

# 2. Разбиваем реальных пользователей из БД на группы A и B
np.random.seed(42)
df_users['group'] = np.random.choice(['A', 'B'], size=len(df_users), p=[0.5, 0.5])

# 3. Симулируем конверсии
# Допустим, мы внедрили фичу, и она повысила конверсию с 10% до 12%
df_users['converted'] = np.where(
    df_users['group'] == 'A',
    np.random.binomial(1, 0.10, len(df_users)),
    np.random.binomial(1, 0.12, len(df_users))
)

# 4. Считаем метрики
print("Результаты A/B-теста")
summary = df_users.groupby('group')['converted'].agg(['count', 'sum', 'mean'])
summary.columns = ['Пользователей', 'Покупок', 'Конверсия']
summary['Конверсия'] = (summary['Конверсия'] * 100).round(2).astype(str) + '%'
print(summary)
print("-" * 28)

# 5. Проверяем статистическую значимость
contingency_table = pd.crosstab(df_users['group'], df_users['converted'])
chi2, p_value, dof, expected = chi2_contingency(contingency_table)

print(f"p-value = {p_value:.4f}")

if p_value < 0.05:
    print("Разница статистически значима. Фичу можно внедрять.")
else:
    print("Разница не значима. Оставляем старую версию.")

# 6. Сохраняем результаты обратно в базу данных
print("Сохранение результатов в таблицу ab_test_results...")
df_users.to_sql('ab_test_results', engine, if_exists='replace', index=False)
print("Готово.")