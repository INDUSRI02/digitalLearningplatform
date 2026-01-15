from django.db import models

# Create your models here.
class InstructorRegModel(models.Model):
    instructor_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=55)
    email = models.EmailField(max_length=100,help_text="Enter Email")
    phone_number = models.BigIntegerField(null=True)
    gender =models.CharField(max_length=50,default=False)
    # experience = models.CharField(max_length=100)
    # category = models.CharField(help_text='Select Category',max_length=50,default='category')   
    password = models.CharField(max_length=100,help_text="Enter Password")
    photo = models.ImageField(default=False)
    status = models.CharField(default='Pending',max_length=100, null=True)
    reg_date = models.DateField(auto_now_add=True, null=True)
    address = models.CharField(max_length=255)
    otp = models.CharField(max_length=6,default=0) 
    otp_status = models.CharField(max_length=15, default='Not Verified')
    

    class Meta:
        db_table = 'Instructor_Details'


class TaskModel(models.Model):
    task_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_by = models.ForeignKey(InstructorRegModel, on_delete=models.CASCADE, related_name='assigned_tasks')
    grade_level = models.CharField(
        max_length=2,
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')],
        help_text="Grade level for which this task is assigned"
    )
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending')

    class Meta:
        db_table = 'Task_Details'

class Addcourse(models.Model):
    course_id = models.AutoField(primary_key=True)
    instructor = models.ForeignKey(InstructorRegModel, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=255)
    course_image = models.ImageField(upload_to='course_images/')
    course_category = models.CharField(max_length=100)
    course_language = models.CharField(max_length=100)
    course_description = models.TextField(null=True,blank=True)
    video_url = models.URLField(null=True,blank=True)
    duration_weeks = models.IntegerField(null=True,blank=True)
    price = models.IntegerField(default=0,help_text='Enter fee ',null=True,blank=True)
    added_date = models.DateField(auto_now_add=True, null=True)



    class Meta:
        db_table = 'Courses_details'





class Question(models.Model):
    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'
    QUESTION_TYPES = [
        (EASY, 'Easy'),
        (MEDIUM, 'Medium'),
        (HARD, 'Hard'),
    ]

    instructor = models.ForeignKey(InstructorRegModel, on_delete=models.CASCADE)
    course = models.ForeignKey(Addcourse, on_delete=models.CASCADE)
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, null=True)
    question_method = models.CharField(max_length=20,default="mcqs")

    class Meta:
        db_table = 'Questions'




class DescriptiveQuestion(models.Model):
    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'
    QUESTION_TYPES = [
        (EASY, 'Easy'),
        (MEDIUM, 'Medium'),
        (HARD, 'Hard'),
    ]

    instructor = models.ForeignKey(InstructorRegModel, on_delete=models.CASCADE)
    course = models.ForeignKey(Addcourse, on_delete=models.CASCADE)
    question_text = models.TextField()
    correct_answer = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, null=True)
    question_method = models.CharField(max_length=20, default="descriptive")

    class Meta:
        db_table = 'DescriptiveQuestions'





class ImageQuestion(models.Model):
    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'
    QUESTION_TYPES = [
        (EASY, 'Easy'),
        (MEDIUM, 'Medium'),
        (HARD, 'Hard'),
    ]

    instructor = models.ForeignKey(InstructorRegModel, on_delete=models.CASCADE)
    course = models.ForeignKey(Addcourse, on_delete=models.CASCADE)
    question_text = models.TextField()
    image = models.ImageField(upload_to='image_questions/', null=True, blank=True)
    correct_answer = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, null=True)
    question_method = models.CharField(max_length=20, default="image")

    class Meta:
        db_table = 'ImageQuestions'