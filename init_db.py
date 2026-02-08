"""
Скрипт для инициализации базы данных и заполнения тестовыми данными
"""
import sqlite3

def init_database():
    # Подключение к БД (создаст файл, если не существует)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Удаляем таблицу если существует
    cursor.execute('DROP TABLE IF EXISTS properties')
    
    # Создаём таблицу недвижимости
    cursor.execute('''
        CREATE TABLE properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            city TEXT NOT NULL,
            address TEXT NOT NULL,
            type TEXT NOT NULL,
            price INTEGER NOT NULL,
            rooms INTEGER NOT NULL,
            area REAL NOT NULL,
            floor INTEGER,
            total_floors INTEGER,
            description TEXT,
            image_url TEXT
        )
    ''')
    
    # Тестовые данные
    test_properties = [
        # Москва
        ('Современная 2-комнатная квартира', 'Москва', 'ул. Арбат, 15', 'apartment', 
         12000000, 2, 65.5, 5, 10, 'Квартира в центре Москвы с евроремонтом', 
         'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=400'),
        
        ('Просторная 3-комнатная квартира', 'Москва', 'Ленинский проспект, 42', 'apartment',
         18000000, 3, 95.0, 8, 16, 'Панорамные окна, парковка', 
         'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=400'),
        
        ('Студия в новостройке', 'Москва', 'ул. Маршала Жукова, 78', 'apartment',
         7500000, 1, 35.0, 12, 20, 'Новостройка, чистовая отделка',
         'https://images.unsplash.com/photo-1502672260066-6bc35f0af07e?w=400'),
        
        ('Уютная 1-комнатная квартира', 'Москва', 'Проспект Мира, 120', 'apartment',
         9000000, 1, 42.0, 3, 9, 'Тихий район, рядом метро',
         'https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=400'),
        
        # Санкт-Петербург
        ('Квартира с видом на Неву', 'Санкт-Петербург', 'Невский проспект, 88', 'apartment',
         15000000, 2, 70.0, 6, 8, 'Историческое здание, вид на реку',
         'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=400'),
        
        ('Светлая 3-комнатная', 'Санкт-Петербург', 'ул. Рубинштейна, 12', 'apartment',
         13500000, 3, 85.0, 4, 5, 'Высокие потолки, историческая квартира',
         'https://images.unsplash.com/photo-1484154218962-a197022b5858?w=400'),
        
        ('Современная студия', 'Санкт-Петербург', 'Васильевский остров, 25', 'apartment',
         6500000, 1, 30.0, 15, 25, 'Новый дом, развитая инфраструктура',
         'https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=400'),
        
        # Казань
        ('Комфортная 2-комнатная', 'Казань', 'ул. Баумана, 45', 'apartment',
         6000000, 2, 58.0, 7, 12, 'Центр города, евроремонт',
         'https://images.unsplash.com/photo-1554995207-c18c203602cb?w=400'),
        
        ('Семейная 3-комнатная', 'Казань', 'проспект Победы, 152', 'apartment',
         7500000, 3, 78.0, 5, 9, 'Тихий район, хорошие школы рядом',
         'https://images.unsplash.com/photo-1556020685-ae41abfc9365?w=400'),
        
        ('Уютная студия', 'Казань', 'ул. Пушкина, 26', 'apartment',
         3500000, 1, 28.0, 10, 17, 'Новостройка, идеально для студента',
         'https://images.unsplash.com/photo-1567767292278-a4f21aa2d36e?w=400'),
        
        # Екатеринбург
        ('Просторная квартира', 'Екатеринбург', 'ул. Малышева, 73', 'apartment',
         8000000, 2, 67.0, 9, 14, 'Свежий ремонт, балкон',
         'https://images.unsplash.com/photo-1565402170291-8491f14678db?w=400'),
        
        ('Большая 3-комнатная', 'Екатеринбург', 'ул. Ленина, 38', 'apartment',
         10000000, 3, 92.0, 6, 10, 'Элитный дом, консьерж',
         'https://images.unsplash.com/photo-1613977257363-707ba9348227?w=400'),
        
        ('Компактная студия', 'Екатеринбург', 'ул. 8 Марта, 120', 'apartment',
         4200000, 1, 32.0, 11, 16, 'Хорошая транспортная доступность',
         'https://images.unsplash.com/photo-1560185007-5f0bb1866cab?w=400'),
        
        # Новосибирск
        ('Светлая 2-комнатная', 'Новосибирск', 'Красный проспект, 82', 'apartment',
         5500000, 2, 60.0, 4, 9, 'Центр, рядом парк',
         'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=400'),
        
        ('Квартира для семьи', 'Новосибирск', 'ул. Крылова, 45', 'apartment',
         7000000, 3, 80.0, 8, 12, 'Большая кухня, лоджия',
         'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=400'),
        
        # Дома
        ('Загородный дом', 'Москва', 'Рублевское шоссе, 25км', 'house',
         45000000, 5, 250.0, 2, 2, 'Таунхаус, участок 6 соток',
         'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400'),
        
        ('Коттедж у озера', 'Санкт-Петербург', 'Приозерское шоссе, 15км', 'house',
         35000000, 4, 200.0, 2, 2, 'Свой берег, баня, гараж',
         'https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=400'),
    ]
    
    # Вставляем данные
    cursor.executemany('''
        INSERT INTO properties (title, city, address, type, price, rooms, area, 
                               floor, total_floors, description, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', test_properties)
    
    conn.commit()
    conn.close()
    
    print("✅ База данных успешно инициализирована!")
    print(f"✅ Добавлено {len(test_properties)} объектов недвижимости")

if __name__ == '__main__':
    init_database()
