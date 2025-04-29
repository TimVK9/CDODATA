from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    CreateView,
    InventoryList,
    InventoryUpdate,
    InventoryItemtDelet,  
    import_excel,
    ObjectDetail,



)




urlpatterns = [
    path('', InventoryList.as_view(), name='home'),
    path('create/', CreateView.as_view(), name='create'),
    path('update/<int:pk>/', InventoryUpdate.as_view(), name='update'),  
    path('delete/<int:pk>/', InventoryItemtDelet.as_view(), name='delete'),  
    path('import/', import_excel, name='import_excel'),
    path('detail/<int:pk>/', ObjectDetail.as_view(), name='detail')  
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )



# 2. Используйте более понятные названия классов (например, InventoryItemDelete вместо InventoryItemtDelete)
# 3. Группируйте импорты по категориям (встроенные модули, сторонние библиотеки, локальные импорты)
# 4. Добавьте документацию к паттернам URL
# 5. Рассмотрите возможность использования include() для модульности
