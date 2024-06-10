from django.urls import path
from . import views


urlpatterns =  [
    path('all-trades/', views.TradeListView.as_view(), name="all-trade"),
    path('add-trade/', views.create_trade, name="create-trade"),
    path('calculator/', views.calculator, name="calculator"),
    path('statistic/', views.statistic, name="statistic"),
    path('statistic/analysis/', views.trade_report, name="analysis"),
]