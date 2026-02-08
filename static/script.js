// Обработка формы ИИ-подбора
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('aiSearchForm');
    const loader = document.getElementById('loader');
    
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Собираем данные формы
            const formData = {
                budget: parseInt(document.getElementById('budget').value),
                city: document.getElementById('city').value,
                rooms: parseInt(document.getElementById('rooms').value),
                purpose: document.getElementById('purpose').value
            };
            
            // Показываем лоадер
            form.style.display = 'none';
            loader.style.display = 'block';
            
            try {
                // Отправляем запрос к API
                const response = await fetch('/api/ai-recommend', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });
                
                if (!response.ok) {
                    throw new Error('Ошибка сервера');
                }
                
                const results = await response.json();
                
                // Сохраняем результаты в localStorage
                localStorage.setItem('aiResults', JSON.stringify(results));
                
                // Перенаправляем на страницу результатов
                window.location.href = '/results';
                
            } catch (error) {
                console.error('Ошибка:', error);
                alert('Произошла ошибка при поиске. Попробуйте снова.');
                form.style.display = 'block';
                loader.style.display = 'none';
            }
        });
    }
});
