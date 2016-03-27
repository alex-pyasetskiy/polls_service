from django.conf.urls import url, include

from . import views

from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'questions', views.QuestionViewSet)

api_urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]