from django.contrib import admin
from django.urls import path,include
from instructorapp import views as insviews
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('instructor/dashboard/',insviews.ins_dashboard,name="ins_dashboard"),
    path('instructor/add-courses/',insviews.add_courses,name="add_courses"),
    path('instructor/view-courses/',insviews.view_courses,name="view_courses"),
    path('instructor/add-question/',insviews.add_question,name="add_question"),
    path('instructor/all-question/',insviews.all_questions,name="all_questions"),
    path('instructor/view-students/',insviews.view_students,name="view_students"),
    path('instructor/view-students-feedbacks/',insviews.view_student_feedbacks,name="view_student_feedbacks"),
    path('instructor/view-students-feedbacks-graph/',insviews.feedbacks_graph,name="ins_feedbacks_graph"),
    path('instructor/logout/',insviews.ins_logout,name="ins_logout"),
    path('instructor/edit-courses/<int:course_id>/',insviews.edit_course,name="edit_course"),


    path('remove-course/<int:course_id>/', insviews.remove_course, name='remove_course'),
    path('remove-question/<int:question_id>/', insviews.remove_question, name='remove_question'),

    path('instructor-mail-reply/rating/<int:rating>/<int:feedback_id>/', insviews.rating_view, name='ins_rating_view'),
    path('remove-feedback/<int:feedback_id>/', insviews.remove_feedback_ins, name='remove_feedback_ins'),




    path('instructor/add-mcqs-questions/', insviews.mcqs, name='mcqs'),
    path('instructor/add-descriptive-questions/', insviews.descriptive_questions, name='descriptive_questions'),
    path('instructor/add-image-questions/', insviews.imageQuestion, name='imageQuestion'),
    path('instructor/test-results/', insviews.ins_test_result, name='ins_test_result'),
    path('instructor/test-deatils/<int:test_id>/',insviews.ins_view_details,name="ins_full_test_deatils"),


    path('time/task/add/', insviews.time_task_add, name='time_task_add'),
    path('time/task/list/', insviews.time_task_list, name='time_task_list'),
    path('time/students/completed/', insviews.time_view_students, name='time_view_students'),
    path('time/task/delete/<int:task_id>/', insviews.time_delete_task, name='time_delete_task'),








    




                   
]