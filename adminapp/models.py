from django.db import models

# Create your models here.
LEVEL_CHOICES = (
    ('Level1', 'Listen & Spell - Word'),
    ('Level2', 'Sentence Challenge'),
    ('Level3', 'Paragraph Perfection'),
)

class ListenSpellWord(models.Model):
    text = models.CharField(
        max_length=100, 
        help_text="The correct word/sentence/paragraph used in Listen & Spell mode"
    )
    audio = models.FileField(
        upload_to='audio/', 
        blank=True, 
        null=True, 
        help_text="Audio file generated via TTS or uploaded manually"
    )
    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default='Level1',
        help_text="Choose the difficulty/level of this challenge"
    )

    def __str__(self):
        return self.text
    

class Challenge(models.Model):
    CHALLENGE_TYPES = [
        ('Visionary', 'Visionary'),
        ('Technical', 'Technical'),
        ('Creative', 'Creative'),
        ('Leadership', 'Leadership'),
        ('Strategic Thinking', 'Strategic Thinking'),
        ('Team Building', 'Team Building'),
        ('Innovation', 'Innovation'),
        ('Decision Making', 'Decision Making'),
        ('Conflict Resolution', 'Conflict Resolution'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    challenge_type = models.CharField(max_length=20, choices=CHALLENGE_TYPES,null=True,blank=True)

    def __str__(self):
        return self.name