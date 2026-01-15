from django.contrib import admin
from django.urls import path,include
from userapp import views as views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('contact/',views.contact,name='contact'),
    path('register/',views.user_register,name='user_register'),
    # path('resend/otp/', views.resend_otp, name='resend_otp'),
    path('login/', views.user_login, name='user_login'),
    path('otp/', views.user_otp, name='user_otp'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path("logout/",views.user_logout,name="user_logout"),
    path("profile/", views.user_profile,name="user_profile"),
    path('admin-login',views.admin_login,name="admin_login"),





    # Game mode URLs
    path('choose/', views.choose_story_mode, name='choose_story_mode'),
    path('solo/', views.solo_story_mode, name='solo_story_mode'),
    path('collaborative/', views.collaborative_story_mode, name='collaborative_story_mode'),
    path('challenge/', views.challenge_story_mode, name='challenge_story_mode'),
    # path('submit-story/', views.submit_story, name='submit_story'),

    # Placeholder URLs for starting stories in each mode
    path('solo/start/', views.start_solo_story, name='start_solo_story'),
    path('collaborative/start/', views.start_collaborative_story, name='start_collaborative_story'),
    path('challenge/start/', views.start_challenge_story, name='start_challenge_story'),




    path('instructor-login/',views.instructor_login,name="instructor_login"),
    path('instructor-register/',views.instructor_register,name="instructor_register"),
    path('instructor/ins-otp/',views.ins_otp,name="instructorotp"),


    


    path('test/choose/',views.test_choose,name="test_choose"),
    path('add_topic/<int:course_id>/', views.add_topic, name='add_topic'),
    path('student/my-courses/',views.my_courses,name="my_courses"),
     path('student/test-result/',views.test_result,name="test_result"),
    path('student/test/<int:course_id>/',views.test,name="test"),
    path('process_question/', views.process_question, name='process_question'),

    path('student/test-deatils/<int:test_id>/',views.view_details,name="view_details"),


    path('leadership/', views.leadership_challenges_page, name='leadership_page'),
    path('show_feedback/', views.show_feedback, name='show_feedback'),




    path('communication/challenge/', views.user_listen_spell, name='communication_challenge'),


    path('start-reflection/', views.start_reflection, name='start_reflection'),
    path('generate-question/', views.generate_question, name='generate_question'),
    path('submit-answer/', views.submit_answer, name='submit_answer'),
    path('view-feedback/', views.view_feedback, name='view_feedback'),





    path('time-game/', views.time_game_view, name='time_game'),
    path('time-game/success/', views.time_game_success_view, name='time_game_success'),
    path('complete-task/<int:task_id>/', views.complete_task, name='complete_task'),
    path('view-completed-tasks/', views.view_completed_tasks, name='view_completed_tasks'),

    path('feedback/', views.feedback, name='feedback'),



                   
]