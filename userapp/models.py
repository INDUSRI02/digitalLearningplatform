from django.db import models
from instructorapp.models import *
from adminapp.models import *
from django.utils import timezone

# Create your models here.
class User(models.Model):
    full_name = models.CharField(max_length=100, verbose_name="User Name")
    email = models.EmailField(verbose_name="Email")
    password = models.CharField(max_length=128, verbose_name="Password")
    phone_number = models.CharField(max_length=15, verbose_name="Phone Number")
    age = models.CharField(max_length=15, verbose_name="Age")
    address = models.TextField(verbose_name="Address")
    photo = models.ImageField(upload_to='profiles/', verbose_name="Upload Profile", null=True, blank=True)
    otp = models.CharField(max_length=6, default='000000', help_text='Enter OTP for verification')
    otp_status = models.CharField(max_length=15, default='Not Verified', help_text='OTP status')
    status = models.CharField(max_length=15, default='Accepted')
    points = models.IntegerField(default=0, verbose_name="Points",null=True,blank=True)
    grade_level = models.CharField(
        max_length=2,
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')],
        help_text="Grade level for which this task is assigned",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.full_name
    



class TaskCompletion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to User model
    task = models.ForeignKey(TaskModel, on_delete=models.CASCADE)  # Link to Task model
    completion_date = models.DateTimeField(auto_now_add=True)  # Store the date the task was completed

    class Meta:
        db_table = 'Task_Completion'

    def __str__(self):
        return f"{self.user.full_name} - {self.task.title} - Completed on {self.completion_date}"









class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255)
    user_email = models.EmailField()
    rating = models.IntegerField()
    additional_comments = models.TextField()
    sentiment = models.CharField(max_length=20, null=True)  # Add this field to store the sentiment
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'feedback'



        
class Reflection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user who provided the answer
    category = models.CharField(max_length=100)  # The category the user selected
    question = models.TextField()  # The generated question
    answer = models.TextField()  # The user's answer
    feedback = models.TextField()  # Feedback from the Perplexity API
    timestamp = models.DateTimeField(auto_now_add=True)  # Time when the answer was submitted

    def __str__(self):
        return f"Reflection by {self.user.username} on {self.category} at {self.timestamp}"
    






class GameProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='Level1')
    incorrect_attempts = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    current_question = models.IntegerField(default=0)
    completed_challenges = models.ManyToManyField(ListenSpellWord, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.current_level}"
    

class Answer(models.Model):
    student_name = models.ForeignKey(User, related_name="answers_from_student", on_delete=models.CASCADE) 
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    answer_text = models.TextField()
    feedback = models.TextField(null=True, blank=True)  # Store feedback from the Perplexity API
    rating = models.IntegerField(null=True, blank=True)  # Store rating out of 10
    submission_date = models.DateTimeField(default=timezone.now)  # Date and time of submission

    def __str__(self):
        return f'{self.student_name} - {self.challenge.name}'



class CollaborativeStory(models.Model):
    prompt = models.TextField()  # The prompt for the story
    user_1 = models.ForeignKey(User, related_name="user_1", on_delete=models.CASCADE)  # User 1
    user_2 = models.ForeignKey(User, related_name="user_2", on_delete=models.CASCADE)  # User 2
    user_1_story = models.TextField(null=True, blank=True)  # Story from User 1
    user_2_story = models.TextField(null=True, blank=True)  # Story from User 2
    feedback = models.TextField(null=True, blank=True)  # Feedback after collaboration

    def __str__(self):
        return f"Collaborative story between {self.user_1} and {self.user_2}"
    











class CartModel(models.Model):
    cart_user=models.ForeignKey(User,on_delete=models.CASCADE)
    cart_booking=models.ForeignKey(Addcourse,on_delete=models.CASCADE)

    class Meta:
        db_table='cart_details'



class StudentCourses(models.Model):
    student = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='student_courses')
    course = models.ForeignKey(Addcourse,on_delete=models.SET_NULL,null=True)

    class Meta:
        db_table = 'student_courses_details'




class UserTestModel(models.Model):
    test_user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='user_results')
    test_name = models.CharField(max_length=155,unique=True)
    test_date = models.DateField(auto_now_add=True)
    test_marks = models.IntegerField(default=0)

    class Meta:
        db_table = 'User_tests_details'


class ResultModel(models.Model):
    result_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    test_id = models.IntegerField(null=True)
    test_name = models.CharField(max_length=509)
    question = models.CharField(max_length=999)
    useranswer = models.CharField(max_length=999,null=True)
    correctanswer = models.CharField(max_length=999)
    marks=models.IntegerField()
    result_date = models.DateField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'Student_Result_Details'






class StudentFeedback(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    user_email = models.EmailField()
    rating = models.IntegerField()
    additional_comments = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'student_feedback'



