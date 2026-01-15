from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from adminapp.models import ListenSpellWord
from gtts import gTTS
from io import BytesIO
from django.core.files.base import ContentFile
from userapp.models import *
from instructorapp.models import *
from django.core.paginator import Paginator



def admin_logout(request):
    request.session.flush() 
    messages.success(request, "Logged out successfully.")
    return redirect("admin_login") 



def admin_dashboard(request):
    return render(request, "admin_dashboard.html")




def admin_listen_spell_add(request):
    if request.method == "POST":
        text = request.POST.get("text", "").strip()
        level = request.POST.get("level", "Level1")  # Default to Level1 if not specified
        
        if not text:
            messages.error(request, "Word text is required.")
            return redirect("admin_listen_spell_add")
        
        try:
            # Use gTTS to generate audio from text
            tts = gTTS(text)
            audio_bytes = BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
            filename = f"{text.lower().replace(' ', '_')}.mp3"
            
            # Create a new ListenSpellWord entry and store the level also
            word = ListenSpellWord.objects.create(text=text, level=level)
            word.audio.save(filename, ContentFile(audio_bytes.read()))
            
            messages.success(request, f"Word '{word.text}' added successfully with generated audio at level {word.level}.")
            return redirect("admin_listen_spell_list")
        except Exception as e:
            messages.error(request, f"Error generating audio: {e}")
            return redirect("admin_listen_spell_add")
    
    return render(request, "admin_listen_spell_add.html")



def admin_listen_spell_delete(request, word_id):
    word = get_object_or_404(ListenSpellWord, id=word_id)
    word.delete()
    messages.success(request, f"Word '{word.text}' deleted successfully.")
    return redirect("admin_listen_spell_list")


def admin_listen_spell_list(request):
    words = ListenSpellWord.objects.all()
    return render(request, "admin_listen_spell_list.html", {"words": words})


def admin_listen_spell_details(request, word_id):
    word = get_object_or_404(ListenSpellWord, id=word_id)
    return render(request, "admin_listen_spell_details.html", {"word": word})




























# ##############################################




# Create your views here.
def admin_dashboard_latest(request):
    total_students = User.objects.count()
    total_instructors = InstructorRegModel.objects.count()
    pending_instructors = InstructorRegModel.objects.filter(status='Pending').count()
    total_feedbacks = Feedback.objects.count()
    context = {
        'total_students': total_students,
        'total_instructors': total_instructors,
        'pending_instructors': pending_instructors,
        'total_feedbacks': total_feedbacks,
    }
    return render(request, "admin_index.html", context)


def pending_ins(request):
    pending_instructors = InstructorRegModel.objects.filter(status='Pending')
    paginator = Paginator(pending_instructors, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, "pending-Instructors.html", context)



def accept_instructor(request, instructor_id):
    instructor = InstructorRegModel.objects.get(pk=instructor_id)
    instructor.status = 'Accepted'
    instructor.save()
    messages.success(request,"Accepted !")
    return redirect('pending_ins')






def all_ins(request):
    accepted_instructors = InstructorRegModel.objects.filter(status='Accepted')
    paginator = Paginator(accepted_instructors, 5) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, "all-Instructors.html", context)


def delete_instructor(request, id):
    instructor = get_object_or_404(InstructorRegModel, pk=id)
    instructor.delete()
    messages.success(request, f"Instructor {instructor.full_name} deleted successfully.")
    return redirect('all_ins')




def all_students(request):
    all_students = User.objects.all()
    paginator = Paginator(all_students, 5) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "all-students.html", {'students': page_obj})


def remove_student(request, id):
    student = User.objects.get(pk=id)
    student_name = student.full_name 
    student.delete()
    messages.success(request, f"{student_name} has been successfully removed.")
    return redirect('all_students')



def view_feedbacks(request):
    feedbacks_list = Feedback.objects.all()
    paginator = Paginator(feedbacks_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin-view-feedbacks.html', {'page_obj': page_obj})



def remove_feedback(request, feedback_id):
    feedback = Feedback.objects.get(pk=feedback_id)
    feedback.delete()
    messages.success(request, 'Feedback removed successfully.')
    return redirect('view_feedbacks')






def feedbacks_graph(request):
    rating_counts = {
        'rating1': Feedback.objects.filter(rating=1).count(),
        'rating2': Feedback.objects.filter(rating=2).count(),
        'rating3': Feedback.objects.filter(rating=3).count(),
        'rating4': Feedback.objects.filter(rating=4).count(),
        'rating5': Feedback.objects.filter(rating=5).count(),
    }
    return render(request,"graph-feedback.html", {'rating_counts': rating_counts})












def add_challenge(request):
    if request.method == "POST":
        challenge_name = request.POST.get('challenge_name')
        challenge_type = request.POST.get('challenge_type')
        challenge_description = request.POST.get('challenge_description')
        Challenge.objects.create(
            name=challenge_name,
            challenge_type=challenge_type,
            description=challenge_description
        )
        messages.success(request,"Challenge Deleted Successfully !")
        return redirect('add_challenge') 
    return render(request, 'add_challenge.html')



def manage_challenges(request):
    challenges = Challenge.objects.all()
    return render(request, 'manage_challenges.html', {'challenges': challenges})




def delete_challenge(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)
    challenge.delete()
    messages.success(request,"Challenge Added Successfully !")
    return redirect('manage_challenges')



def view_answers(request):
    answers = Answer.objects.all()
    return render(request, 'view_answers.html', {'answers': answers})


















