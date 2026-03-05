from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.utils.translation import gettext as _
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse

import os
import random
import requests

from userapp.models import *
from adminapp.models import *


def generate_otp(length=4):
    otp = "".join(random.choices("0123456789", k=length))
    return otp


def user_logout(request):
    logout(request)
    request.session.flush()
    messages.info(request, _("Logout successful."))
    return redirect("user_login")

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

def index(request):
    feedbacks = Feedback.objects.all().order_by('-submitted_at')
    return render(request, 'index.html', {'feedbacks': feedbacks})      




def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('name')
        password = request.POST.get('password')
        if username == 'admin' and password == 'admin':
            messages.success(request, 'Login Successful')
            return redirect('admin_dashboard_latest')
        else:
            messages.error(request, 'Invalid details !')
            return redirect('admin_login')
    return render(request,'admin_login.html')





def contact(request):
    return render(request,'contact.html')



def user_register(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone_number = request.POST.get("phone_number")
        age = request.POST.get("age")
        address = request.POST.get("address")
        photo = request.FILES.get("photo")

        # email check
        if User.objects.filter(email=email).exists():
            messages.error(request, _("An account with this email already exists."))
            return redirect("user_register")

        # create user
        otp = generate_otp()

        user = User.objects.create(
            full_name=full_name,
            email=email,
            password=password,
            phone_number=phone_number,
            age=age,
            address=address,
            photo=photo,
            otp=otp,
            otp_status="Not Verified",
        )

        # send OTP
        subject = _("OTP Verification for Account Activation")
        message = _(
            "Hello %(name)s,\n\nYour OTP for account activation is: %(otp)s"
        ) % {"name": full_name, "otp": otp}

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        request.session["id_for_otp_verification_user"] = user.pk
        messages.success(request, _("OTP sent to your email and phone number."))
        return redirect("user_otp")

    return render(request, "user-register.html")


def user_otp(request):
    otp_user_id = request.session.get("id_for_otp_verification_user")

    if not otp_user_id:
        messages.error(request, _("No OTP session found. Please try again."))
        return redirect("user_register")

    if request.method == "POST":
        entered_otp = (
            request.POST.get("first", "")
            + request.POST.get("second", "")
            + request.POST.get("third", "")
            + request.POST.get("fourth", "")
        )

        try:
            user = User.objects.get(id=otp_user_id)
        except User.DoesNotExist:
            messages.error(request, _("User not found. Please try again."))
            return redirect("user_register")

        if user.otp == entered_otp:
            user.otp_status = "Verified"
            user.save()

            messages.success(request, _("OTP verification successful."))
            return redirect("user_login")

        messages.error(request, _("Incorrect OTP. Please try again."))
        return redirect("user_otp")

    return render(request, "user-otp.html")


def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, _("No user found."))
            return redirect("user_login")

        # password check
        if user.password != password:
            messages.error(request, _("Incorrect password."))
            return redirect("user_login")

        # admin approval check
        if user.status != "Accepted":
            messages.warning(request, _("Your account is not accepted by admin yet."))
            return redirect("user_login")

        # otp check
        if user.otp_status != "Verified":
            new_otp = generate_otp()
            user.otp = new_otp
            user.otp_status = "Not Verified"
            user.save()

            send_mail(
                _("New OTP for Verification"),
                _("Your new OTP is: %(otp)s") % {"otp": new_otp},
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            request.session["id_for_otp_verification_user"] = user.pk
            messages.warning(
                request,
                _("OTP not verified. A new OTP has been sent."),
            )
            return redirect("user_otp")

        # SUCCESS LOGIN
        request.session.flush()
        request.session["user_id_after_login"] = user.pk

        messages.success(request, _("Login successful."))
        return redirect("user_dashboard")

    return render(request, "user-login.html")


def user_dashboard(request):
    return render(request,"user_dashboard.html")



def user_profile(request):
    user_id  = request.session.get('user_id_after_login')
    print(user_id)
    user = User.objects.get(pk= user_id)
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        try:
            profile = request.FILES['profile']
            user.photo = profile
        except MultiValueDictKeyError:
            profile = user.photo
        password = request.POST.get('password')
        location = request.POST.get('location')
        user.user_name = name
        user.email = email
        user.phone_number = phone
        user.password = password
        user.address = location
        user.save()
        messages.success(request , 'updated succesfully!')
        return redirect('user_profile')
    return render(request,'user-profile.html',{'user':user})



import requests





def generate_story_prompt():
    try:
        
        headers = {
            "Authorization": f"Bearer {settings.PERPLEXITY_API_KEY}",
            "Content-Type": "application/json"
        }

        
        prompt_request = {
            "model": "sonar",  
            "messages": [
                {"role": "system", "content": "Generate a random, short story prompt (maximum two lines) without genre, character, or specific theme."},
                {"role": "user", "content": "Please generate a random, creative story prompt."}
            ],
            "temperature": 0.7  
        }

        
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            json=prompt_request,
            headers=headers
        )

        
        if response.status_code == 200:
            result = response.json()
            
            generated_prompt = result['choices'][0]['message']['content'].strip()
            
            
            prompt_lines = generated_prompt.split('\n')
            short_prompt = '\n'.join(prompt_lines[:2])  
            
            return short_prompt
        else:
            return "Error generating prompt. Please try again later."
    except Exception as e:
        return f"An error occurred: {str(e)}"









def choose_story_mode(request):
    return render(request, 'storyweave/storyweave_choose_mode.html')








def solo_story_mode(request):
    
    prompt = generate_story_prompt()
    request.session['story_prompt'] = prompt  
    
    feedback = None
    if request.method == 'POST':
        story = request.POST.get('story', '')  
        if story:
            feedback = generate_feedback(story, prompt)  

    return render(request, 'storyweave/storyweave_solo_mode.html', {'prompt': prompt, 'feedback': feedback})












def generate_feedback(story, prompt):
    try:
        
        headers = {
            "Authorization": f"Bearer {settings.PERPLEXITY_API_KEY}",
            "Content-Type": "application/json"
        }

        
        feedback_request = {
            "model": "sonar",
            "messages": [
                {"role": "system", "content": f"Provide brief feedback on how well the following story matches the prompt: '{prompt}' with no any extra things or symbols just the feedback as pure text no symbols "},
                {"role": "user", "content": f"Story: {story}"}
            ],
            "temperature": 0.5  
        }

        
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            json=feedback_request,
            headers=headers
        )

        if response.status_code == 200:
            result = response.json()
            feedback = result['choices'][0]['message']['content'].strip()

            
            feedback_lines = feedback.split("\n")[:4]  
            formatted_feedback = "\n".join(feedback_lines).strip()

           

            return formatted_feedback
        else:
            return "Error generating feedback. Please try again later.", ""
    except Exception as e:
        return f"An error occurred: {str(e)}", ""
def collaborative_story_mode(request):
    print("Collaborative Story Mode view accessed...")  
    
    
    prompt = generate_story_prompt()

    
    current_user_id = request.session.get('user_id_after_login')
    users = User.objects.exclude(id=current_user_id)  

    print(f"Prompt generated and users fetched: {users}")  

    
    collaborative_story = CollaborativeStory.objects.filter(user_1_id=current_user_id, user_2__isnull=True).first()

    if collaborative_story:
        
        feedback = "You have already submitted your story part. Waiting for your collaborator to complete their part."
        return render(request, 'storyweave/storyweave_collaborative_mode.html', {
            'prompt': prompt,
            'users': users,
            'feedback': feedback,
        })

    if request.method == 'POST':
        selected_user_id = request.POST.get('selected_user')
        story_part = request.POST.get('story_part')
        
        
        selected_user = User.objects.get(id=selected_user_id)
        current_user = User.objects.get(id=current_user_id)

        
        collaborative_story = CollaborativeStory(
            prompt=prompt,
            user_1=current_user,
            user_2=selected_user,
            user_1_story=story_part,  
            user_2_story=None,  
        )
        collaborative_story.save()

        
        feedback = "Your story part has been submitted successfully. Now, waiting for your collaborator to submit their story part."
        
        return render(request, 'storyweave/storyweave_collaborative_mode.html', {
            'prompt': prompt,
            'users': users,
            'feedback': feedback,
        })

    return render(request, 'storyweave/storyweave_collaborative_mode.html', {'prompt': prompt, 'users': users})






def challenge_story_mode(request):
    return render(request, 'storyweave/storyweave_challenge_mode.html')


def start_solo_story(request):
    return render(request, 'storyweave/storyweave_solo_mode.html')  

def start_collaborative_story(request):
    return render(request, 'storyweave/storyweave_collaborative_mode.html')  

def start_challenge_story(request):
    return render(request, 'storyweave/storyweave_challenge_mode.html')  


















def instructor_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('Password')
        try:
            ins = InstructorRegModel.objects.get(email=email)
            if ins.password == password:
                if ins.otp_status == 'Verified':
                    if ins.status == 'Accepted':
                        messages.success(request, 'Login successful!')
                        request.session['ins_id_after_login'] = ins.pk
                        return redirect('ins_dashboard')
                    else:
                        messages.error(request, 'Account not yet accepted')
                        return redirect('instructor_login')
                else:
                    otp = generate_otp()
                    ins.otp = otp
                    ins.save()
                    subject = 'OTP Verification for Account Activation'
                    otp_message = f'Your OTP for verification is: {ins.otp}'
                    message = f'Hello {ins.full_name},\n\nYou are attempting to log in to your account. {otp_message}\n\nIf you did not request this OTP, please ignore this message.'
                    from_email = settings.EMAIL_HOST_USER
                    recipient_list = [ins.email]
                    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                    messages.success(request, 'Otp sent to mail and phone number!')
                    return redirect('instructorotp')
            else:
                messages.error(request, 'Incorrect Password')
                return redirect('instructor_login')
        except InstructorRegModel.DoesNotExist:
            messages.error(request, 'No User Found')
            return redirect('instructor_register')
    return render(request, "instructor-login.html")










def instructor_register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        location = request.POST.get('address')
        profile = request.FILES.get('profile')
        gender = request.POST.get('gender')
        try:
            InstructorRegModel.objects.get(email=email)
            messages.info(request, 'Email Already Exists!')
            return redirect('instructor_login')
        except InstructorRegModel.DoesNotExist:
            otp = generate_otp()
            ins = InstructorRegModel.objects.create(full_name=name, email=email, phone_number=phone, photo=profile, password=password, address=location, otp=otp)
            print(ins)
            subject = 'OTP Verification for Account Activation'
            otp_message = f'Your OTP for verification is: {ins.otp}'
            message = f'Hello {ins.full_name},\n\nYou are attempting to Register an Account. {otp_message}\n\nIf you did not request this OTP, please ignore this message.'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [ins.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            request.session['ins_id'] = ins.instructor_id
            messages.info(request, 'OTP Sent To Email and Phone!')
            return redirect('instructorotp')
    return render(request,"instructor-register.html")





def ins_otp(request):
    ins_id = request.session.get('ins_id')
    if request.method == "POST":
        otp_entered = request.POST.get('ins_otp')
        if not otp_entered:
            messages.error(request, 'Please enter the OTP')
            print("OTP not entered")
            return redirect('instructorotp')
        try:
            instructor = InstructorRegModel.objects.get(pk=ins_id)
            if str(instructor.otp) == otp_entered:
                instructor.otp_status = 'Verified'
                instructor.save()
                
                messages.success(request, 'OTP verification successful!')
                return redirect('instructor_login')
            else:
                messages.error(request, 'Invalid OTP entered')
                print("Invalid OTP entered")
                return redirect('instructorotp')
        except instructor.DoesNotExist:
            messages.error(request, 'Invalid Instructor')
            print("Invalid Instructor")
            return redirect('instructor_register')
    return render(request,"ins-otp.html")














def test_choose(request):
    all_courses = Addcourse.objects.all()
    for course_name in all_courses:
        print(course_name.course_name)
    return render(request,"onlinetest/choose.html", {'all_courses': all_courses})




def add_topic(request, course_id):
    # Check if user ID is stored in the session, indicating that the user is logged in
    user_id = request.session.get("user_id_after_login")
    
    if not user_id:
        # If the user is not logged in (no user ID in session), show an error and redirect to login
        messages.error(request, "You must be logged in to add a topic.")
        return redirect('login')  # Adjust this to the actual login URL name
    
    try:
        # Retrieve the logged-in user using the session's user_id
        student = User.objects.get(pk=user_id)
        
        # Fetch the course (topic) using the provided course_id
        course = Addcourse.objects.get(pk=course_id)

        # Check if the user has already added the course
        if not StudentCourses.objects.filter(student=student, course=course).exists():
            # If the course is not added, add it to the StudentCourses model
            StudentCourses.objects.create(student=student, course=course)
            messages.success(request, f"The Topic '{course.course_name}' has been added to your topics successfully.")
        else:
            # If the course is already added, show an info message
            messages.info(request, f"You've already added the course '{course.course_name}'.")

        # After completing the action, redirect to the 'test_choose' page
        return redirect('test_choose')  # Adjust this to the actual URL name for the page you want to redirect to

    except Addcourse.DoesNotExist:
        # If the course is not found, show an error message and redirect
        messages.error(request, "Course not found.")
        return redirect('test_choose')  # Adjust this to the actual URL name
    



def my_courses(request):
    student_id = request.session.get('user_id_after_login')
    if student_id is None:
        messages.warning(request, "No student found, please login again!")
        return redirect('user_login')

    student_courses = StudentCourses.objects.filter(student_id=student_id)
    for student_course in student_courses:
        question_count = Question.objects.filter(course=student_course.course).count()
        descriptive_question_count = DescriptiveQuestion.objects.filter(course=student_course.course).count()
        image_question_count = ImageQuestion.objects.filter(course=student_course.course).count()
        total_question_count = question_count + descriptive_question_count + image_question_count
        student_course.total_question_count = total_question_count
    context = {
        'student_courses': student_courses,
    }
    return render(request, "onlinetest/my_courses.html", context)



from django.core.paginator import Paginator


def test_result(request):
    student_id = request.session.get('user_id_after_login')
    if student_id is not None:
        student_tests = UserTestModel.objects.filter(test_user_id=student_id).order_by('-id')
        paginator = Paginator(student_tests, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "onlinetest/test_result.html", {'page_obj': page_obj})
    else:
        messages.error(request, "USer not logged in or session data missing")
        return redirect("user_login")




import string
from django.utils import timezone


def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))






def test(request, course_id):
    request.session['course_id'] = course_id
    
    course = Addcourse.objects.get(course_id=course_id)
    request.session['answered_questions'] = [] 
    current_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    random_string = generate_random_string(4)
    test_name = f"Test for {course.course_name} ({current_time} {random_string})"
    student_id = request.session.get('user_id_after_login')
    user_test = UserTestModel.objects.create(test_name=test_name, test_user_id=student_id)
    request.session['user_test_id'] = user_test.pk
    return redirect('process_question')





from fuzzywuzzy import fuzz
from random import shuffle



def process_question(request):
    print("Inside process_question view")
    course_id = request.session.get('course_id')
    answered_questions = request.session.get('answered_questions', [])
    print("Answered Questions:", answered_questions)
    if len(answered_questions) >= 10:
            print("Test completed.")
            messages.success(request,"Questions Completed !")
            return redirect('test_result')
    else:
        question_qs = list(Question.objects.filter(course_id=course_id).order_by('?')[:10])
        descriptive_qs = list(DescriptiveQuestion.objects.filter(course_id=course_id).order_by('?')[:10])
        image_qs = list(ImageQuestion.objects.filter(course_id=course_id).order_by('?')[:10])
        all_questions = question_qs + descriptive_qs + image_qs
        shuffle(all_questions)
        first_question = all_questions[0]
        


    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        question_method = request.POST.get('question_method')
        print("Question ID:", question_id)
        print("Question Method:", question_method)
        student_answer = None
        
        
        
        
        if question_method == "mcqs":
            student_answer = request.POST.get(f'question_{question_id}_answer')
            print("Student Answer (MCQs):", student_answer)
            question = Question.objects.get(pk=question_id)
            correct_answer = question.correct_answer
            print("Correct Answer (MCQs):", correct_answer)
            is_correct = student_answer == correct_answer
            print("Is Correct (MCQs):", is_correct)
            question_type = question.question_type
            print("Question Type (MCQs):", question_type)
        elif question_method == "descriptive":
            student_answer = request.POST.get('descriptive_answer')
            print("Student Answer (Descriptive):", student_answer)
            question = DescriptiveQuestion.objects.get(pk=question_id)
            correct_answer = question.correct_answer
            print("Correct Answer (Descriptive):", correct_answer)
            similarity_percentage = fuzz.partial_ratio(student_answer.lower(), correct_answer.lower())
            is_correct = similarity_percentage >= 85 
            print("Is Correct (Descriptive):", is_correct)
            question_type = question.question_type
            print("Question Type (Descriptive):", question_type)
        elif question_method == "image":
            student_answer = request.POST.get('image_answer') 
            print("Student Answer (Image):", student_answer)
            question = ImageQuestion.objects.get(pk=question_id)
            correct_answer = question.correct_answer
            print("Correct Answer (Image):", correct_answer)
            similarity_percentage = fuzz.partial_ratio(student_answer.lower(), correct_answer.lower())
            is_correct = similarity_percentage >= 85  
            print("Is Correct (Image):", is_correct)
            question_type = question.question_type 
            print("Question Type (Image):", question_type)
        
        user_test_id = request.session.get('user_test_id')
        user_test = UserTestModel.objects.get(pk=user_test_id)
        
        test_marks = 1 if is_correct else 0
        user_test.test_marks += test_marks
        user_test.save()
        
        
        
        student_id = request.session.get('user_id_after_login')
        result = ResultModel.objects.create(
            user_id=student_id,
            test_id=user_test.pk,
            test_name=user_test.test_name,
            question=question.question_text,
            useranswer=student_answer,
            correctanswer=correct_answer,
            marks=test_marks
        )
        # print("All Questions:", all_questions)
        answered_questions.append((int(question_id),question_type, is_correct))
        request.session['answered_questions'] = answered_questions

        # answered_questions = request.session.get('answered_questions', [])
        # print(answered_questions,"hey look here ")
        if len(answered_questions) >= 10:
            print("Test completed.")
            messages.success(request,"Question Completed !")
            return redirect('test_result')
        else:
            if len(answered_questions) > 1:
                print("Last 2 Answered Questions:", answered_questions[-2:])
                last_two_correct_answers = [answered_questions[-2][-1], answered_questions[-1][-1]]
                last_question_type = answered_questions[-1][1]
                print("Last Answered Question Type:", last_question_type,last_two_correct_answers)
                if last_two_correct_answers == [True, True]:
                    if last_question_type == 'easy':
                        next_question_type = 'medium'
                    elif last_question_type == 'medium':
                        next_question_type = 'hard'
                    else:
                        next_question_type = 'hard'  
                elif last_two_correct_answers == [False, False]:
                    if last_question_type == 'easy':
                        next_question_type = 'easy'
                    elif last_question_type == 'medium':
                        next_question_type = 'easy'
                    else:
                        next_question_type = 'medium'
                else:
                    next_question_type = last_question_type 
                answered_question_ids = [q[0] for q in answered_questions]
                question_qs = list(Question.objects.filter(course_id=course_id, question_type=next_question_type).exclude(pk__in=answered_question_ids).order_by('?')[:10])
                descriptive_qs = list(DescriptiveQuestion.objects.filter(course_id=course_id, question_type=next_question_type).exclude(pk__in=answered_question_ids).order_by('?')[:10])
                image_qs = list(ImageQuestion.objects.filter(course_id=course_id, question_type=next_question_type).exclude(pk__in=answered_question_ids).order_by('?')[:10])
                all_questions = question_qs + descriptive_qs + image_qs
                
                shuffle(all_questions)
                if all_questions:
                    next_question = all_questions[0]
                else:
                    messages.error(request, "No more questions available.")
                    return redirect('test_result')
            else:
                print("Answered Questions:", answered_questions)
                last_question_type = answered_questions[-1][1]
                print("Last Answered Question Type:", last_question_type)
                answered_question_ids = [q[0] for q in answered_questions]
                question_qs = list(Question.objects.filter(course_id=course_id, question_type=last_question_type).exclude(pk__in=answered_question_ids).order_by('?')[:10])
                descriptive_qs = list(DescriptiveQuestion.objects.filter(course_id=course_id, question_type=last_question_type).exclude(pk__in=answered_question_ids).order_by('?')[:10])
                image_qs = list(ImageQuestion.objects.filter(course_id=course_id, question_type=last_question_type).exclude(pk__in=answered_question_ids).order_by('?')[:10])
                all_questions = question_qs + descriptive_qs + image_qs
                
                shuffle(all_questions)
                if all_questions:
                    next_question = all_questions[0]
                else:
                    messages.error(request, "No more questions available.")
                    return redirect('test_result')
                print(next_question, "this is the next question !")
            return render(request, 'onlinetest/process-question.html', {'random_question': next_question})
    else:
        return render(request, 'onlinetest/process-question.html', {'random_question': first_question})









def view_details(request, test_id):
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

    return render(request, "onlinetest/view-fulltest-deatils.html", 
                  {'results_details': results_details,
                   "total_marks_final":total_marks_final,
                   "correct_Answers":correct_Answers,
                   "wrong_Answers":wrong_Answers,
                   "percantage":percantage,})







def leadership_challenges_page(request):
    challenges = Challenge.objects.all().order_by('?')  # Randomize challenges
    student_id = request.session.get('user_id_after_login')

    if request.method == "POST":
        challenge_id = request.POST.get('challenge_id')
        answer_text = request.POST.get('answer_text')
        student_name = student_id  # Assuming student_id is the user who is logged in

        # Get the challenge object
        challenge = Challenge.objects.get(id=challenge_id)

        # Call the Perplexity API to get feedback and rating
        feedback, rating = fetch_perplexity_feedback(challenge.description, answer_text)

        # Print feedback to the terminal
        print(f"Feedback for Challenge ID {challenge_id}: {feedback}")
        print(f"Rating: {rating}/10")

        # Get the user who submitted the answer
        user = User.objects.get(id=student_name)

        # Store the answer, feedback, rating, and submission date in the Answer model
        Answer.objects.create(
            student_name=user,
            challenge=challenge,
            answer_text=answer_text,
            feedback=feedback,
            rating=rating,  # Save the extracted rating
            submission_date=timezone.now()
        )

        messages.success(request, "Answer submitted successfully!")
        return redirect("show_feedback")
    
    return render(request, 'leadership/leadership_page.html', {'challenges': challenges})


def show_feedback(request):
    student_id = request.session.get('user_id_after_login')
    
    # Get all answers (feedback) for the current user, ordered by submission date (latest first)
    user_answers = Answer.objects.filter(student_name_id=student_id).order_by('-submission_date')
    
    return render(request, 'leadership/show_feedback.html', {'user_answers': user_answers})

def fetch_perplexity_feedback(challenge_description, answer_text):
    try:
        headers = {
            "Authorization": f"Bearer {settings.PERPLEXITY_API_KEY}",
            "Content-Type": "application/json"
        }

        prompt_request = {
            "model": "sonar",
            "messages": [
                {"role": "system", "content": "Provide feedback for the user's answer based on the challenge description."},
                {"role": "user", "content": f"Challenge: {challenge_description}\nAnswer: {answer_text}"}
            ],
            "temperature": 0.7
        }

        # Make the API request
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            json=prompt_request,
            headers=headers
        )

        if response.status_code == 200:
            result = response.json()
            feedback = result['choices'][0]['message']['content'].strip()

            # Extract rating from feedback
            rating = extract_rating(feedback)

            # Clean feedback: Remove any symbols or numeric ratings
            feedback_cleaned = clean_feedback(feedback)

            return feedback_cleaned, rating
        else:
            return "Error generating feedback. Please try again later.", 0
    except Exception as e:
        return f"An error occurred: {str(e)}", 0



def clean_feedback(feedback):
    """
    This function ensures the feedback is in plain text, removing any symbols or numeric ratings.
    It will also ensure the feedback does not contain unwanted characters and splits feedback into points.
    """
    # Remove numbers and symbols (optional based on feedback formatting)
    feedback = feedback.replace("Rating:", "").replace("/10", "")

    # Ensure the feedback contains only pure textual content
    feedback = ''.join([char if char.isalnum() or char.isspace() or char in ['.', ',', '?', '!'] else '' for char in feedback])

    # Split the feedback into points based on the full stop (.)
    feedback_points = feedback.split('.')
    feedback_points = [point.strip() for point in feedback_points if point.strip()]  # Remove empty points

    return feedback_points


def extract_rating(feedback):
    # This function assumes that the feedback includes a rating in the format "Rating: X/10"
    if "Rating:" in feedback:
        try:
            rating_str = feedback.split("Rating:")[1].strip()
            rating = int(rating_str.split("/")[0].strip())
            return rating
        except ValueError:
            return 0
    return 0












def unified_login(request):
    
    if request.method == "POST":
        email = (request.POST.get("email") or "").strip()
        password = (request.POST.get("password") or "").strip()

        if not email or not password:
            messages.error(request, _("Please enter both email and password."))
            return redirect("login")

        email = email.lower()

        # ADMIN
        admin_ids = ["admin", "admin@gmail.com"]
        if email in admin_ids and password == "admin":
            request.session.flush()
            request.session["admin_logged_in"] = True
            request.session["role"] = "admin"
            messages.success(request, _("Admin login successful."))
            return redirect("admin_dashboard_latest")

        # STUDENT
        try:
            user = User.objects.get(email=email)

            if user.password != password:
                messages.error(request, _("Incorrect password."))
                return redirect("login")

            if user.status != "Accepted":
                messages.warning(request, _("Your account is not accepted yet."))
                return redirect("login")

            if user.otp_status != "Verified":
                new_otp = generate_otp()
                user.otp = new_otp
                user.otp_status = "Not Verified"
                user.save()

                send_mail(
                    _("New OTP for Verification"),
                    _("Your new OTP is: %(otp)s") % {"otp": new_otp},
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )

                request.session["id_for_otp_verification_user"] = user.pk
                messages.warning(request, _("OTP not verified. New OTP sent."))
                return redirect("user_otp")

            request.session.flush()
            request.session["user_id_after_login"] = user.pk
            request.session["role"] = "student"
            messages.success(request, _("Login successful."))
            return redirect("user_dashboard")

        except User.DoesNotExist:
            pass

        # INSTRUCTOR
        try:
            ins = InstructorRegModel.objects.get(email=email)

            if ins.password != password:
                messages.error(request, _("Incorrect password."))
                return redirect("login")

            if ins.status != "Accepted":
                messages.warning(request, _("Instructor not approved yet."))
                return redirect("login")

            if ins.otp_status != "Verified":
                otp = generate_otp()
                ins.otp = otp
                ins.save()

                send_mail(
                    _("OTP Verification"),
                    _("Your OTP is: %(otp)s") % {"otp": otp},
                    settings.EMAIL_HOST_USER,
                    [ins.email],
                    fail_silently=False,
                )

                request.session["ins_id"] = ins.pk
                messages.warning(request, _("OTP verification required."))
                return redirect("instructorotp")

            request.session.flush()
            request.session["ins_id_after_login"] = ins.pk
            request.session["role"] = "instructor"
            messages.success(request, _("Instructor login successful."))
            return redirect("ins_dashboard")

        except InstructorRegModel.DoesNotExist:
            pass

        messages.error(request, _("No user found with these credentials."))
        return redirect("login")

    return render(request, "unified-login.html")
    
    
def signup_router(request):
    """
    Simple router page where user chooses:
    - Student
    - Instructor
    """

    if request.method == "POST":
        role = request.POST.get("role")

        if role == "student":
            return redirect("user_register")

        if role == "instructor":
            return redirect("instructor_register")

        messages.error(request, _("Please select a valid role."))
        return redirect("signup")

    return render(request, "signup-router.html")

def user_listen_spell(request):
    # Authentication check
    user_id = request.session.get("user_id_after_login")
    if not user_id:
        return redirect("user_login")
    
    user = User.objects.get(id=user_id)

    # Handle game restart
    if 'restart_game' in request.GET:
        reset_game(request, user)
        return redirect('communication_challenge')

    # Handle POST submissions (user answering the question)
    if request.method == "POST":
        current_word_id = request.session.get('current_listen_spell_word_id')
        if not current_word_id:
            messages.error(request, "No active word found")
            return redirect('communication_challenge')

        word = ListenSpellWord.objects.get(id=current_word_id)
        user_answer = request.POST.get('user_answer', '').strip().lower()
        correct_answer = word.text.strip().lower()

        incorrect = request.session.get('incorrect_answer_count', 0)

        if user_answer == correct_answer:
            user.points += 10
            level_key = f'{word.level}_correct_answers'
            correct_count = request.session.get(level_key, 0) + 1
            request.session[level_key] = correct_count

            if correct_count >= 3:
                # Advance to next level if applicable
                next_level = {'Level1': 'Level2', 'Level2': 'Level3'}.get(word.level)
                if next_level:
                    request.session['current_level'] = next_level
                    messages.success(request, f"Advanced to {next_level}!")
                else:
                    messages.success(request, "All levels completed!")
                request.session.pop(level_key, None)

            user.save()
            messages.success(request, "Correct answer!")
            return redirect('communication_challenge')

        else:
            incorrect += 1
            request.session['incorrect_answer_count'] = incorrect
            user.points = max(0, user.points - 5)
            user.save()

            if incorrect >= 3:
                messages.error(request, "Game Over! Please restart the game.")
                return redirect('communication_challenge')

            messages.error(request, "Incorrect answer. Try again.")
            return redirect('communication_challenge')

    # Handle GET requests
    level = request.session.get('current_level', 'Level1')
    words = ListenSpellWord.objects.filter(level=level)

    if not words.exists():
        messages.error(request, "No words available")
        return redirect('user_dashboard')

    word = random.choice(words)
    request.session['current_listen_spell_word_id'] = word.id

    # Get current level stats
    correct_answers = request.session.get(f'{level}_correct_answers', 0)
    total_questions_in_level = 3  # Assuming 3 questions per level
    remaining_questions = total_questions_in_level - correct_answers

    context = {
        'word': word,
        'incorrect_answer_count': request.session.get('incorrect_answer_count', 0),
        'points': user.points,
        'current_level': level,
        'correct_answers': correct_answers,
        'remaining_questions': remaining_questions,
        'total_questions': total_questions_in_level
    }

    return render(request, 'communication/communication_challenge.html', context)

def reset_game(request, user):
    # Reset game session and user points
    request.session.pop('incorrect_answer_count', None)
    request.session.pop('current_level', None)
    request.session.pop('current_listen_spell_word_id', None)
    for level in ['Level1', 'Level2', 'Level3']:
        request.session.pop(f'{level}_correct_answers', None)
    user.points = 0
    user.save()













def generate_question(request):
    if request.method == 'POST':
        # Get the selected category
        category = request.POST.get('category')

        # Generate the question using the Perplexity API
        question = generate_question_from_perplexity(category)

        # Render the response page with the generated question
        return render(request, 'reflection/question_page.html', {'question': question, 'category': category})
    
    return HttpResponse("Invalid request", status=400)

def generate_question_from_perplexity(category):
    try:
        headers = {
            "Authorization": f"Bearer {settings.PERPLEXITY_API_KEY}",
            "Content-Type": "application/json"
        }

        prompt_request = {
            "model": "sonar",
            "messages": [
                {"role": "system", "content": f"Generate a question based on the following category: {category}."},
                {"role": "user", "content": f"Please generate a reflective question related to {category}."}
            ],
            "temperature": 0.7
        }

        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            json=prompt_request,
            headers=headers
        )

        if response.status_code == 200:
            result = response.json()
            generated_question = result['choices'][0]['message']['content'].strip()
            return generated_question
        else:
            return "Error generating question. Please try again later."
    except Exception as e:
        return f"An error occurred: {str(e)}"



def start_reflection(request):
    return render(request, 'reflection/start_reflection.html')



def submit_answer(request):
    # Get the current logged-in user from the session
    user_id = request.session.get("user_id_after_login")
    
    if user_id:
        # Retrieve the user instance from the database
        user = User.objects.get(id=user_id)

        if request.method == 'POST':
            # Get the user input (answer) and other necessary data
            answer = request.POST.get('answer')
            category = request.POST.get('category')  # The category the user selected
            question = request.POST.get('question')  # The generated question from API
            
            # Get the feedback from Perplexity API based on the answer and category
            feedback = generate_feedback_from_perplexity(answer, category)

            # Save the reflection data in the database
            reflection = Reflection(
                user=user,
                category=category,
                question=question,
                answer=answer,
                feedback=feedback
            )
            reflection.save()

            # Use Django's messaging framework to send a success message
            messages.success(request, 'Your answer has been successfully recorded.')

            # Redirect to a new page where the user can see their feedback
            return redirect('view_feedback')

    # If the user is not found or the request is invalid
    messages.error(request, 'Invalid request or user not found.')
    return redirect('start_reflection')  # Redirect to the reflection start page or any appropriate page


def generate_feedback_from_perplexity(answer, category):
    """Generate feedback for the user's answer using the Perplexity API."""
    try:
        headers = {
            "Authorization": f"Bearer {settings.PERPLEXITY_API_KEY}",
            "Content-Type": "application/json"
        }

        prompt_request = {
            "model": "sonar",
            "messages": [
                {"role": "system", "content": f"Provide feedback on the following answer related to {category}."},
                {"role": "user", "content": f"Answer: {answer}. Provide reflective feedback."}
            ],
            "temperature": 0.7
        }

        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            json=prompt_request,
            headers=headers
        )

        if response.status_code == 200:
            result = response.json()
            generated_feedback = result['choices'][0]['message']['content'].strip()
            return generated_feedback
        else:
            return "Error generating feedback. Please try again later."
    except Exception as e:
        return f"An error occurred while fetching feedback: {str(e)}"
    









def view_feedback(request):
    # Get the current logged-in user from the session
    user_id = request.session.get("user_id_after_login")

    if user_id:
        # Retrieve the user instance from the database
        user = User.objects.get(id=user_id)

        # Get all Reflection objects related to the logged-in user, ordered by the latest (descending)
        reflections = Reflection.objects.filter(user=user).order_by('-timestamp')  # Order by timestamp

        return render(request, 'reflection/view_feedback.html', {'reflections': reflections})

    else:
        messages.error(request, 'User not found or not logged in.')
        return redirect('start_reflection')
    




def time_game_view(request):
    user_id = request.session.get("user_id_after_login")

    # Check if user is logged in
    if user_id:
        if request.method == "POST":
            grade_level = request.POST.get('grade_level')

            try:
                user = User.objects.get(pk=user_id)
                user.grade_level = grade_level  # Set the selected grade level
                user.save()  # Save changes to the database
                
                # Add a success message
                messages.success(request, 'Grade level updated successfully!')
                
                # Redirect to a success page (can be a new page or the same page)
                return redirect('time_game_success')  # Redirect to a success page

            except User.DoesNotExist:
                return HttpResponse("User not found.", status=404)
        
        # Render the form when the request is GET
        return render(request, "time_game.html")

    # If user is not logged in, redirect to the login page
    return redirect("user_login")








def time_game_success_view(request):
    user_id = request.session.get("user_id_after_login")

    if user_id:
        user = User.objects.get(pk=user_id)

        # Get all tasks for the logged-in user's grade level
        tasks = TaskModel.objects.filter(grade_level=user.grade_level, status='Pending')

        # Pass the tasks to the template
        return render(request, 'time_game_success.html', {
            'tasks': tasks,
            'user': user
        })

    return redirect("user_login")








def complete_task(request, task_id):
    user_id = request.session.get("user_id_after_login")

    if user_id:
        # Fetch the task and user
        task = get_object_or_404(TaskModel, pk=task_id)
        user = User.objects.get(pk=user_id)

        # Mark the task as completed
        task.status = 'Completed'
        task.save()

        # Store the completion in TaskCompletion model
        TaskCompletion.objects.create(user=user, task=task, completion_date=timezone.now())

        # Add a success message
        messages.success(request, f"Task '{task.title}' marked as completed!")

        # Redirect back to the success page
        return redirect('time_game_success')  # Redirect to the success page or anywhere you'd like

    return redirect("user_login")










def view_completed_tasks(request):
    user_id = request.session.get("user_id_after_login")

    if user_id:
        user = User.objects.get(pk=user_id)

        # Get all completed tasks for the logged-in user
        completed_tasks = TaskCompletion.objects.filter(user=user)

        return render(request, 'view_completed_tasks.html', {
            'completed_tasks': completed_tasks
        })

    return redirect("user_login") 












from io import TextIOWrapper
import pickle
import joblib
from transformers import AlbertTokenizerFast
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Feedback, User


print("Loading tokenizer...")
loaded_tokenizer = AlbertTokenizerFast.from_pretrained(
    "amazone review/albert_tokenizer"
)


print("Loading label encoder...")
label_encoder = joblib.load('amazone review/label_encoder.joblib')


print("Loading model architecture...")
model_architecture_path = 'amazone review/bylstm_model_architecture.json'
with open(model_architecture_path, 'r') as json_file:
    loaded_model_json = json_file.read()


print("Loading model weights...")
model_weights_path = 'amazone review/bylstm_model_weights.h5'
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights(model_weights_path)

max_len = 256


def predict_sentiment(text):
    print(f"Predicting sentiment for text: {text}")

    
    print(f"Tokenizing and padding input text...")
    sequences = [loaded_tokenizer.encode(text, max_length=max_len, truncation=True, padding='max_length')]
    padded_sequences = pad_sequences(sequences, maxlen=max_len, padding='post', truncating='post')

    
    print(f"Making prediction using the model...")
    predictions = loaded_model.predict(padded_sequences)
    print(f"Model prediction output: {predictions}")

    
    predicted_label = label_encoder.inverse_transform(predictions.argmax(axis=1))[0]
    print(f"Predicted sentiment label: {predicted_label}")
    
    
    return predicted_label






def feedback(request):
    user_id = request.session.get('user_id_after_login')
    print(f"User ID from session: {user_id}")

    if request.method == 'POST':
        print(f"Processing POST request...")
        
        user = get_object_or_404(User, pk=user_id)

      
        user_name = request.POST.get('user_name')
        user_email = request.POST.get('user_email')
        rating = request.POST.get('rating')
        additional_comments = request.POST.get('additional_comments')

        print(f"Feedback form data: user_name={user_name}, user_email={user_email}, rating={rating}, additional_comments={additional_comments}")

        
        print(f"Performing sentiment analysis...")
        sentiment = predict_sentiment(additional_comments)  
        print(f"Predicted sentiment: {sentiment}")

        
        
        if sentiment == 1:
            sentiment_label = "neutral"
        elif sentiment == 2:
            sentiment_label = "positive"
        else:
            sentiment_label = "negative"
        
        print(f"Mapped sentiment label: {sentiment_label}")

        
        print(f"Saving feedback to the database...")
        feedback = Feedback.objects.create(
            user=user,
            user_name=user_name,
            user_email=user_email,
            rating=rating,
            additional_comments=additional_comments,
            sentiment=sentiment_label  
        )
        print(f"Feedback saved: {feedback}")

        
        messages.success(request, "Your feedback has been submitted successfully.")
        return redirect('feedback')

    print("Returning feedback page...")
    return render(request, "user-feedback.html")
