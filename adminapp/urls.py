from django.urls import path
from adminapp import views as view


urlpatterns = [
   

    # admin dashboard    
    path('dashboard/', view.admin_dashboard, name='admin_dashboard'),
    path("logout/", view.admin_logout, name="admin_logout"),

    # Listen & Spell management URLs
    path('listen_spell/add/', view.admin_listen_spell_add, name='admin_listen_spell_add'),
    path('listen_spell/list/', view.admin_listen_spell_list, name='admin_listen_spell_list'),
    path('listen_spell/details/<int:word_id>/', view.admin_listen_spell_details, name='admin_listen_spell_details'),
    path('listen_spell/delete/<int:word_id>/', view.admin_listen_spell_delete, name='admin_listen_spell_delete'),







    path('courses-admin/dashboard/',view.admin_dashboard_latest,name="admin_dashboard_latest"),
    path('courses-admin/pending-instructors/',view.pending_ins,name="pending_ins"),
    path('courses-admin/all-instructors/',view.all_ins,name="all_ins"),
    path('courses-admin/all-students/',view.all_students,name="all_students"),
    path('courses-admin/view-feedbacks/',view.view_feedbacks,name="view_feedbacks"),
    path('courses-admin/feedback-graph/',view.feedbacks_graph,name="feedbacks_graph"),


    path('accept_instructor/<int:instructor_id>/', view.accept_instructor, name='accept_instructor'),
    path('delete_ins/<int:id>/', view.delete_instructor, name='delete_ins'),
    path('all-students/', view.all_students, name='all_students'),
    path('remove-student/<int:id>/', view.remove_student, name='remove_student'),
    path('remove-feedback/<int:feedback_id>/', view.remove_feedback, name='remove_feedback'),



    path('add_challenge/', view.add_challenge, name='add_challenge'),
    path('manage_challenges/', view.manage_challenges, name='manage_challenges'),
    path('view_answers/', view.view_answers, name='view_answers'),

    path('delete_challenge/<int:challenge_id>/', view.delete_challenge, name='delete_challenge'),








    


]