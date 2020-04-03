from django.urls import path

from . import views

urlpatterns = [
    path('registration', views.registration_cover, name='rg'),
    path('login', views.login_cover, name='lg'),
    path('find_pieces', views.find_pieces_cover, name='fps'),
    path('verify', views.verify_cover, name='vf'),
    path('find_doc_by_lang', views.find_doc_by_lang_cover, name='fdbl'),
    path('get_from_db', views.get_from_db_cover, name='gfd'),
    path('get_from_db_for_chief', views.get_from_db_for_chief_cover, name='gfdfc'),
    path('get_users', views.get_users_cover, name='gu'),
    path('get_trans_and_docs', views.get_trans_and_docs_cover, name='gtad'),
    path('get_translator_stats', views.get_translator_stats_cover, name='gts'),
    path('get_file_stat', views.get_file_stat_cover, name='gfs'),
    path('get_pieces_stat', views.get_pieces_stat_cover, name='gps'),
    path('', views.index, name='index'),
    path('verify_file', views.verify_file_cover, name='vff'),
    path('update_importance', views.update_importance_cover, name='ui'),
    path('update_docs', views.update_docs_cover, name='ud'),
    path('update_pieces', views.update_pieces_cover, name='up'),
    path('update_translating_pieces', views.update_translating_pieces_cover, name='utp'),
    path('let_my_people_pass', views.let_my_people_pass, name='lmpg'),
    path('check_user', views.check_user, name='cu'),
    path('find_piece', views.find_piece, name='fp')
]
