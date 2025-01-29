from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from todo import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = DefaultRouter()
router.register('todos', views.TaskViewSet)
router.register('priorities', views.PriorityViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),   
    path('api/todos/toggleStatus/<int:pk>/', views.ToggleTodoStatusView.as_view()),
    path('api/logout/', views.LogoutView.as_view()),
    
]
