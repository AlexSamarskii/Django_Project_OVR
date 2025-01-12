import os
from django.apps import AppConfig


class EventsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'events'
    
    def ready(self):
        print(os.environ)
        print("Метод ready() вызван")
        if os.environ.get('RUN_MAIN', None) != 'true':
            print("RUN_MAIN не равен 'true', метод ready() не будет выполняться полностью")
            return
        else:
            print("RUN_MAIN равен 'true', продолжаем выполнение метода ready()")
            
        from django.db.utils import OperationalError, ProgrammingError
        from django.core.exceptions import ObjectDoesNotExist
        from django.db import connections
        from .models import Category
        try:
            db_conn = connections['default']
            db_conn.ensure_connection()
            if not Category.objects.exists():
                print("Категории не существуют, создаём их")
                Category.objects.create(name='Музыка',
                description='Мероприятия, связанные с музыкой и концертами.')
                Category.objects.create(name='Искусство',
                description='Выставки, галереи и другие художественные события.')
                Category.objects.create(name='Спорт',
                description='Спортивные мероприятия и соревнования.')
            else:
                print("Категории уже существуют")
        except (OperationalError, ProgrammingError) as e:
            print(f"Ошибка при попытке создать категории: {e}")
            pass