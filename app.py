"""
Flask приложение для агентства недвижимости с ИИ-подбором
"""
from flask import Flask, render_template, request, jsonify
import sqlite3
from ai_recommender import AIRecommender

app = Flask(__name__)

# Функция для подключения к БД
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')

@app.route('/catalog')
def catalog():
    """Каталог недвижимости"""
    conn = get_db_connection()
    
    # Получаем фильтры из URL
    city = request.args.get('city', '')
    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)
    rooms = request.args.get('rooms', type=int)
    property_type = request.args.get('type', '')
    
    # Строим SQL запрос с фильтрами
    query = "SELECT * FROM properties WHERE 1=1"
    params = []
    
    if city:
        query += " AND city = ?"
        params.append(city)
    if min_price:
        query += " AND price >= ?"
        params.append(min_price)
    if max_price:
        query += " AND price <= ?"
        params.append(max_price)
    if rooms:
        query += " AND rooms = ?"
        params.append(rooms)
    if property_type:
        query += " AND type = ?"
        params.append(property_type)
    
    properties = conn.execute(query, params).fetchall()
    
    # Получаем уникальные города для фильтра
    cities = conn.execute("SELECT DISTINCT city FROM properties ORDER BY city").fetchall()
    conn.close()
    
    return render_template('catalog.html', properties=properties, cities=cities)

@app.route('/ai-search')
def ai_search():
    """Страница ИИ-подбора"""
    conn = get_db_connection()
    cities = conn.execute("SELECT DISTINCT city FROM properties ORDER BY city").fetchall()
    conn.close()
    return render_template('ai_search.html', cities=cities)

@app.route('/api/ai-recommend', methods=['POST'])
def ai_recommend():
    """API endpoint для ИИ-подбора недвижимости"""
    data = request.json
    
    # Получаем все объекты из БД
    conn = get_db_connection()
    all_properties = conn.execute("SELECT * FROM properties").fetchall()
    conn.close()
    
    # Преобразуем в список словарей
    properties_list = [dict(prop) for prop in all_properties]
    
    # Используем ИИ-рекомендатель
    recommender = AIRecommender()
    recommendations = recommender.recommend(properties_list, data)
    
    return jsonify(recommendations)

@app.route('/results')
def results():
    """Страница результатов ИИ-подбора"""
    return render_template('results.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
