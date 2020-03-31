from django.urls import path

from . import views

urlpatterns = [
    path('registration', views.registration_cover, name='rg'),
    path('login', views.login_cover, name='lg'),
    path('find_pieces', views.find_pieces_cover, name='fp'),
    path('verify', views.verify_cover, name='vf'),
    path('find_doc_by_lang', views.find_doc_by_lang_cover, name='fdbl'),
    path('get_from_db', views.get_from_db_cover, name='gfd'),
    path('get_from_db_for_chief', views.get_from_db_for_chief_cover, name='gfdfc'),
    path('get_users', views.get_users_cover, name='gu'),
    path('get_trans_and_docs', views.get_trans_and_docs_cover, name='gtad'),
    path('get_translator_stats', views.get_translator_stats_cover, name='gts'),
    path('get_file_stat', views.get_file_stat_cover, name='gfs'),
    path('', views.index, name='index')]
