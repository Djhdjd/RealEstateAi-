"""
Тест ИИ-рекомендателя
"""
import sqlite3
from ai_recommender import AIRecommender

# Получаем данные из БД
conn = sqlite3.connect('database.db')
conn.row_factory = sqlite3.Row
properties = conn.execute("SELECT * FROM properties").fetchall()
conn.close()

# Преобразуем в список словарей
properties_list = [dict(prop) for prop in properties]

# Создаём рекомендатель
recommender = AIRecommender()

# Тестовый запрос 1: средний бюджет, Москва, 2 комнаты
print("=" * 60)
print("ТЕСТ 1: Поиск 2-комнатной квартиры в Москве")
print("=" * 60)
test_preferences_1 = {
    'budget': 10000000,
    'city': 'Москва',
    'rooms': 2,
    'purpose': 'buy'
}

results_1 = recommender.recommend(properties_list, test_preferences_1)
print(f"\n💡 Найдено {len(results_1)} вариантов\n")

for i, item in enumerate(results_1[:3], 1):
    prop = item['property']
    print(f"#{i} {prop['title']}")
    print(f"   Цена: {prop['price']:,} ₽ | {prop['rooms']} комн. | {prop['area']} м²")
    print(f"   Score: {item['score']:.1f} баллов - {item['match_level']}")
    print(f"   Объяснения:")
    for exp in item['explanations']:
        print(f"     • {exp}")
    print()

# Тестовый запрос 2: бюджетный вариант, Казань, 1 комната
print("\n" + "=" * 60)
print("ТЕСТ 2: Поиск студии в Казани (бюджетный)")
print("=" * 60)
test_preferences_2 = {
    'budget': 4000000,
    'city': 'Казань',
    'rooms': 1,
    'purpose': 'buy'
}

results_2 = recommender.recommend(properties_list, test_preferences_2)
print(f"\n💡 Найдено {len(results_2)} вариантов\n")

for i, item in enumerate(results_2[:3], 1):
    prop = item['property']
    print(f"#{i} {prop['title']}")
    print(f"   Цена: {prop['price']:,} ₽ | {prop['rooms']} комн. | {prop['area']} м²")
    print(f"   Score: {item['score']:.1f} баллов - {item['match_level']}")
    print()

print("=" * 60)
print("✅ Тест завершён успешно!")
print("=" * 60)
