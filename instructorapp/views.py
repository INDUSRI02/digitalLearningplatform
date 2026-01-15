from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import logout
import os
from userapp.models import *
from instructorapp.models import *
from django.utils.datastructures import MultiValueDictKeyError
import random
import urllib.request
import urllib.parse
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.conf import settings



EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# Create your views here.

def ins_logout(request):
    logout(request)
    messages.info(request,"Logout Successfully ")
    return redirect('instructor_login')




def ins_dashboard(request):
    current_logined_ins = request.session.get('ins_id_after_login')
    total_courses = Addcourse.objects.filter(instructor=current_logined_ins).count()
    total_questions = (
        Question.objects.filter(instructor=current_logined_ins).count() +
        DescriptiveQuestion.objects.filter(instructor=current_logined_ins).count() +
        ImageQuestion.objects.filter(instructor=current_logined_ins).count()
    )
    total_students = User.objects.count()
    context = {
        'total_students': total_students,
        'total_courses': total_courses,
        'total_questions': total_questions,
    }
    return render(request, 'instructor/ins_index.html', context)



def add_courses(request):
    current_logined_ins = request.session.get('ins_id_after_login')
    if request.method == 'POST':
        instructor_id = current_logined_ins
        course_name = request.POST.get('courseName')
        if Addcourse.objects.filter(instructor_id=instructor_id, course_name=course_name).exists():
            messages.error(request, 'Course with the same name already exists')
            return redirect('add_courses')
        else:
            course_image = request.FILES.get('courseImage')
            course_category = request.POST.get('courseCategory')
            course_language = request.POST.get('courseLanguage')
            course_description = request.POST.get('courseDescription')
            video_url = request.POST.get('videourl')
            duration_weeks = request.POST.get('courseDuration')
            price = request.POST.get('coursePrice')
            course = Addcourse.objects.create(
                instructor_id=instructor_id,
                course_name=course_name,
                course_image=course_image,
                course_category=course_category,
                course_language=course_language,
                course_description=course_description,
                video_url=video_url,
                duration_weeks=duration_weeks,
                price=price
            )
            messages.success(request,"Subject Added Successfully")
            return redirect('add_courses')
    return render(request, "instructor/add-courses.html")




def view_courses(request):
    current_logined_ins = request.session.get('ins_id_after_login')
    courses = Addcourse.objects.filter(instructor_id=current_logined_ins)
    paginator = Paginator(courses, 5) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, "instructor/view-courses.html", context)



def add_question(request):
    current_instructor_id = request.session.get('ins_id_after_login')
    instructor_courses = Addcourse.objects.filter(instructor_id=current_instructor_id)
    if request.method == 'POST':
        course_id = request.POST.get('courseSelect')
        course = Addcourse.objects.get(pk=course_id)
        question_text = request.POST.get('questionText')
        option_a = request.POST.get('optionA')
        option_b = request.POST.get('optionB')
        option_c = request.POST.get('optionC')
        option_d = request.POST.get('optionD')
        correct_answer = request.POST.get('correctAnswer')
        question_type = request.POST.get('questionType')
        Question.objects.create(
            instructor_id=current_instructor_id,
            course=course,
            question_text=question_text,
            option_a=option_a,
            option_b=option_b,
            option_c=option_c,
            option_d=option_d,
            correct_answer=correct_answer,
            question_type=question_type,
        )
        messages.success(request, "Question Added Successfully")
        return redirect('add_question')  
    return render(request, "instructor/add-questions.html", {'instructor_courses': instructor_courses})



def all_questions(request):
    current_instructor_id = request.session.get('ins_id_after_login')
    question_queryset = Question.objects.filter(instructor_id=current_instructor_id)
    descriptive_question_queryset = DescriptiveQuestion.objects.filter(instructor_id=current_instructor_id)
    image_question_queryset = ImageQuestion.objects.filter(instructor_id=current_instructor_id)
    all_questions_queryset = list(question_queryset) + list(descriptive_question_queryset) + list(image_question_queryset)
    all_questions_queryset.sort(key=lambda x: x.id, reverse=True)
    paginator = Paginator(all_questions_queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "instructor/all-questions.html", {'page_obj': page_obj})





def remove_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.delete()
    messages.info(request,"Deleted Successfully !")
    return redirect('all_questions') 



def view_students(request):
    current_instructor_id = request.session.get('ins_id_after_login')
    if current_instructor_id is None:
        return HttpResponse("Instructor ID not found in session")
    course_students = StudentCourses.objects.filter(course__instructor=current_instructor_id).values('course__course_name').annotate(num_students=Count('student'))
    return render(request, "instructor/view-students.html", {'course_students': course_students})



def view_student_feedbacks(request):
    current_instructor_id = request.session.get('ins_id_after_login')
    courses = Addcourse.objects.filter(instructor_id=current_instructor_id)
    course_names = courses.values_list('course_name', flat=True)
    feedbacks = StudentFeedback.objects.filter(course_name__in=course_names)
    paginator = Paginator(feedbacks, 5) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, "instructor/view-feedbacks.html", context)



def feedbacks_graph(request):
    current_instructor_id = request.session.get('ins_id_after_login')
    instructor_courses = Addcourse.objects.filter(instructor_id=current_instructor_id)
    course_names = [course.course_name for course in instructor_courses]
    feedbacks = StudentFeedback.objects.filter(course_name__in=course_names)
    rating_counts = {
        'rating1': feedbacks.filter(rating=1).count(),
        'rating2': feedbacks.filter(rating=2).count(),
        'rating3': feedbacks.filter(rating=3).count(),
        'rating4': feedbacks.filter(rating=4).count(),
        'rating5': feedbacks.filter(rating=5).count(),
    }
    return render(request, "instructor/feedback-graph.html", {'rating_counts': rating_counts})





def edit_course(request, course_id):
    course_details = Addcourse.objects.get(pk=course_id)
    if request.method == 'POST':
        course_details.course_name = request.POST.get('courseName') if request.POST.get('courseName') else course_details.course_name
        course_details.course_image = request.FILES['courseImage'] if 'courseImage' in request.FILES else course_details.course_image
        course_details.course_category = request.POST.get('courseCategory') if request.POST.get('courseCategory') else course_details.course_category
        course_details.course_language = request.POST.get('courseLanguage') if request.POST.get('courseLanguage') else course_details.course_language
        course_details.course_description = request.POST.get('courseDescription') if request.POST.get('courseDescription') else course_details.course_description
        course_details.video_url = request.POST.get('videourl') if request.POST.get('videourl') else course_details.video_url
        course_details.duration_weeks = request.POST.get('courseDuration') if request.POST.get('courseDuration') else course_details.duration_weeks
        course_details.price = request.POST.get('coursePrice') if request.POST.get('coursePrice') else course_details.price
        course_details.save()
        messages.success(request,"Updated successfully !")
        return redirect('view_courses')
    return render(request, "instructor/edit-courses.html", {'course_details': course_details})




def remove_course(request, course_id):
    course = get_object_or_404(Addcourse, pk=course_id)
    course.delete()
    messages.error(request,"Deleted Successfully !")
    return redirect('view_courses')






def rating_view(request, rating, feedback_id):
    try:
        feedback = StudentFeedback.objects.get(pk=feedback_id)
        user = feedback.student
        if rating == 1 or rating == 2:
            subject = 'Improvement Feedback'
            message = 'Hello,\n\nThank you for your feedback. We have taken note of your suggestions and will work towards improving our services. Your input is valuable to us.'
        elif rating == 3:
            subject = 'Appreciation for Feedback'
            message = 'Hello,\n\nThank you for your feedback. We appreciate your suggestions and will strive to make improvements based on your input.'
        elif rating == 4 or rating == 5:
            subject = 'Appreciation for Feedback'
            message = 'Hello,\n\nThank you for your feedback. We are delighted to hear about your positive experience. Your satisfaction is our priority.'
        else:
            messages.error(request, 'Invalid rating provided.')
            return redirect('admin_view_feedbacks')
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        messages.success(request, 'Email sent successfully!')
    except StudentFeedback.DoesNotExist:
        messages.error(request, 'Feedback does not exist.')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
    return redirect('view_student_feedbacks')




def remove_feedback_ins(request, feedback_id):
    feedback = get_object_or_404(StudentFeedback, pk=feedback_id)
    feedback.delete()
    messages.info(request,"Feedback deleted Successfully ")
    return redirect('view_student_feedbacks') 




def mcqs(request):
    current_instructor_id = request.session.get('ins_id_after_login')
    instructor_courses = Addcourse.objects.filter(instructor_id=current_instructor_id)
    if request.method == 'POST':
        course_id = request.POST.get('courseSelect')
        course = Addcourse.objects.get(pk=course_id)
        question_text = request.POST.get('questionText')
        option_a = request.POST.get('optionA')
        option_b = request.POST.get('optionB')
        option_c = request.POST.get('optionC')
        option_d = request.POST.get('optionD')
        correct_answer = request.POST.get('correctAnswer')
        question_type = request.POST.get('questionType')
        Question.objects.create(
            instructor_id=current_instructor_id,
            course=course,
            question_text=question_text,
            option_a=option_a,
            option_b=option_b,
            option_c=option_c,
            option_d=option_d,
            correct_answer=correct_answer,
            question_type=question_type,
        )
        messages.success(request, "Question Added Successfully")
        return redirect('mcqs')
    return render(request,"instructor/mcqs-question.html",{'instructor_courses':instructor_courses})





def descriptive_questions(request):
    current_instructor_id = request.session.get('ins_id_after_login')
    instructor_courses = Addcourse.objects.filter(instructor_id=current_instructor_id)
    if request.method == 'POST':
        course_id = request.POST.get('courseSelect')
        course = Addcourse.objects.get(pk=course_id)
        question_text = request.POST.get('questionText')
        question_type = request.POST.get('questionType')
        correct_answer = request.POST.get('descriptive_answer')
        DescriptiveQuestion.objects.create(
            instructor_id=current_instructor_id,
            course=course,
            question_text=question_text,
            correct_answer=correct_answer,
            question_type=question_type,
        )
        messages.success(request, "Question Added Successfully")
        return redirect('descriptive_questions')
    return render(request,"instructor/descriptive-questions.html",{'instructor_courses':instructor_courses})


def imageQuestion(request):
    current_instructor_id = request.session.get('ins_id_after_login')
    instructor_courses = Addcourse.objects.filter(instructor_id=current_instructor_id)
    if request.method == 'POST':
        course_id = request.POST.get('courseSelect')
        course = Addcourse.objects.get(pk=course_id)
        image = request.FILES.get('Image')
        question_text = request.POST.get('questionText')
        question_type = request.POST.get('questionType')
        correct_answer = request.POST.get('image_answer')
        ImageQuestion.objects.create(
            instructor_id=current_instructor_id,
            course=course,
            image=image,
            question_text=question_text,
            correct_answer=correct_answer,
            question_type=question_type,
        )
        messages.success(request, "Question Added Successfully")
        return redirect('imageQuestion')
    return render(request,"instructor/image-questions.html",{'instructor_courses':instructor_courses})




def ins_test_result(request):
    instructor_id =  request.session.get('ins_id_after_login')
    if instructor_id is not None:
        instructor_courses = Addcourse.objects.filter(instructor_id=instructor_id)
        student_ids = StudentCourses.objects.filter(course__in=instructor_courses).values_list('student_id', flat=True)
        student_tests = UserTestModel.objects.filter(test_user_id__in=student_ids).order_by('-id')
        paginator = Paginator(student_tests, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "instructor/test-results.html", {'page_obj': page_obj})
    else:
        messages.error(request, "Instructor not logged in or session data missing")
        return redirect("instructor_login")
    



def ins_view_details(request, test_id):
    test_results = ResultModel.objects.filter(test_id=test_id)
    total_marks = UserTestModel.objects.get(pk=test_id)
    total_marks_final = total_marks.test_marks
    correct_Answers = total_marks_final
    wrong_Answers = 10 - int(correct_Answers)
    percantage = (correct_Answers/10*100)
    results_details = []

    
    for result in test_results:
        results_details.append({
            'test_name': result.test_name,
            'question': result.question,
            'user_answer': result.useranswer,
            'correct_answer': result.correctanswer,
            'marks': result.marks
        })

        print("Correct Answer:", result.correctanswer)

    return render(request, "instructor/full-test-details.html", 
                  {'results_details': results_details,
                   "total_marks_final":total_marks_final,
                   "correct_Answers":correct_Answers,
                   "wrong_Answers":wrong_Answers,
                   "percantage":percantage,})













def time_task_add(request):
    instructor_id = request.session.get('ins_id_after_login')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        grade_level = request.POST.get('grade_level')
        status = 'Pending'  # You can modify this depending on your use case
        
        # Check if all fields are filled
        if not title or not description or not due_date or not grade_level:
            messages.error(request, 'All fields are required.')
            return redirect('time_task_add')
        
        try:
            # Get the instructor from the database
            instructor = InstructorRegModel.objects.get(instructor_id=instructor_id)

            # Create and save the new task
            task = TaskModel.objects.create(
                title=title,
                description=description,
                due_date=due_date,
                grade_level=grade_level,
                status=status,
                assigned_by=instructor  # Link to the instructor
            )

            messages.success(request, 'Task has been successfully added!')
            return redirect('time_task_list')  # Redirect after saving the task
        except InstructorRegModel.DoesNotExist:
            messages.error(request, 'Instructor not found. Please try again.')
            return redirect('time_task_add')

    return render(request, 'time/task_add.html')



def time_task_list(request):
    instructor_id = request.session.get('ins_id_after_login')
    
    if instructor_id:
        # Filter tasks by the current logged-in instructor
        tasks = TaskModel.objects.filter(assigned_by__instructor_id=instructor_id)
    else:
        tasks = []  # If the instructor is not logged in, return an empty list
    
    return render(request, 'time/task_list.html', {'tasks': tasks})

def time_delete_task(request, task_id):
    # Ensure the current logged-in instructor owns the task
    instructor_id = request.session.get('ins_id_after_login')
    
    task = get_object_or_404(TaskModel, id=task_id)
    
    if task.assigned_by.instructor_id != instructor_id:
        messages.error(request,"you are not authorized !")
        return redirect("time_task_list")

    # Delete the task
    task.delete()
    
    messages.success(request, 'Task deleted successfully.')
    return redirect('time_task_list')  


def time_view_students(request):
    # Fetch all TaskCompletion objects
    task_completions = TaskCompletion.objects.all()

    # Pass the task completions to the template
    return render(request, 'time/view_students.html', {'task_completions': task_completions})