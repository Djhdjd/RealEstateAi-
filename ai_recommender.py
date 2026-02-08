"""
ИИ-модуль для подбора недвижимости
Использует scoring-систему для ранжирования объектов
"""

class AIRecommender:
    def __init__(self):
        pass
    
    def recommend(self, properties, user_preferences):
        """
        Главная функция рекомендации
        
        Args:
            properties: список всех объектов недвижимости
            user_preferences: словарь с предпочтениями пользователя
        
        Returns:
            список рекомендованных объектов с объяснениями
        """
        budget = user_preferences.get('budget', 0)
        city = user_preferences.get('city', '')
        rooms = user_preferences.get('rooms', 0)
        purpose = user_preferences.get('purpose', 'buy')  # buy или rent
        
        scored_properties = []
        
        for prop in properties:
            # Фильтруем по базовым критериям
            if not self._matches_basic_criteria(prop, city, purpose):
                continue
            
            # Вычисляем score (баллы)
            score = 0
            explanations = []
            
            # 1. Проверка бюджета (самый важный критерий)
            price = prop['price']
            if price <= budget:
                # Чем ближе к бюджету, тем выше балл
                price_ratio = price / budget if budget > 0 else 0
                score += 40 * price_ratio
                explanations.append(f"✓ Цена {price:,} ₽ в пределах бюджета")
            else:
                # Превышение бюджета - штраф
                overage = ((price - budget) / budget) * 100
                score -= overage
                explanations.append(f"⚠ Цена превышает бюджет на {overage:.0f}%")
            
            # 2. Соответствие количества комнат
            if prop['rooms'] == rooms:
                score += 30
                explanations.append(f"✓ Точное совпадение: {rooms} комнат(ы)")
            elif abs(prop['rooms'] - rooms) == 1:
                score += 15
                explanations.append(f"≈ Близко: {prop['rooms']} комнат(ы) вместо {rooms}")
            else:
                explanations.append(f"○ {prop['rooms']} комнат(ы)")
            
            # 3. Бонус за оптимальную площадь (30-35 м² на комнату)
            optimal_area = rooms * 32.5
            area_diff = abs(prop['area'] - optimal_area)
            if area_diff < 20:
                area_bonus = 20 * (1 - area_diff / 20)
                score += area_bonus
                explanations.append(f"✓ Оптимальная площадь {prop['area']} м²")
            else:
                explanations.append(f"○ Площадь {prop['area']} м²")
            
            # 4. Бонус за тип недвижимости
            if purpose == 'buy' and prop['type'] == 'apartment':
                score += 10
                explanations.append("✓ Квартира - ликвидный актив")
            elif purpose == 'rent' and prop['type'] == 'apartment':
                score += 5
                explanations.append("✓ Квартира - удобна для аренды")
            
            # Добавляем в результаты
            scored_properties.append({
                'property': dict(prop),
                'score': round(score, 2),
                'explanations': explanations,
                'match_level': self._get_match_level(score)
            })
        
        # Сортируем по score (от большего к меньшему)
        scored_properties.sort(key=lambda x: x['score'], reverse=True)
        
        # Возвращаем топ-10
        return scored_properties[:10]
    
    def _matches_basic_criteria(self, prop, city, purpose):
        """Проверка базовых критериев фильтрации"""
        # Город должен совпадать
        if city and prop['city'] != city:
            return False
        
        # Проверка доступности (можно расширить логику)
        # Например, для аренды только определенные типы
        return True
    
    def _get_match_level(self, score):
        """Определяет уровень соответствия по баллам"""
        if score >= 80:
            return 'Отличное совпадение'
        elif score >= 60:
            return 'Хорошее совпадение'
        elif score >= 40:
            return 'Среднее совпадение'
        else:
            return 'Слабое совпадение'
