from django.db import models
from django.utils import timezone
import uuid


class ValentinePlan(models.Model):
    """Store generated Valentine plans"""
    
    RELATIONSHIP_CHOICES = [
        ('girlfriend', 'Girlfriend'),
        ('boyfriend', 'Boyfriend'),
        ('crush', 'Crush'),
        ('best_friend', 'Best Friend'),
        ('self_love', 'Self Love'),
    ]
    
    VIBE_CHOICES = [
        ('romantic', 'Romantic'),
        ('funny', 'Funny'),
        ('crazy', 'Crazy'),
        ('spiritual', 'Spiritual'),
        ('filmy', 'Filmy'),
    ]
    
    PLAN_TYPE_CHOICES = [
        ('Rose Day', 'Rose Day (Feb 7) 🌹'),
        ('Propose Day', 'Propose Day (Feb 8) 💍'),
        ('Chocolate Day', 'Chocolate Day (Feb 9) 🍫'),
        ('Teddy Day', 'Teddy Day (Feb 10) 🧸'),
        ('Promise Day', 'Promise Day (Feb 11) 🤝'),
        ('Hug Day', 'Hug Day (Feb 12) 🤗'),
        ('Kiss Day', 'Kiss Day (Feb 13) 💋'),
        ('Valentine Day', 'Valentine\'s Day (Feb 14) 💘'),
        ('Full Week', 'Full Valentine Week (Feb 7-14) 💖'),
    ]
    
    # Unique identifier
    plan_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    share_code = models.CharField(max_length=200, unique=True, db_index=True)
    
    # User inputs
    your_name = models.CharField(max_length=100)
    partner_name = models.CharField(max_length=100, blank=True, default='')
    relationship_type = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES)
    city = models.CharField(max_length=100)
    budget = models.IntegerField()
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPE_CHOICES)
    vibe = models.CharField(max_length=20, choices=VIBE_CHOICES)
    
    # Personalization fields
    about_partner = models.TextField(blank=True, null=True, help_text="Tell us about them")
    about_yourself = models.TextField(blank=True, null=True, help_text="Tell us about you")
    special_request = models.TextField(blank=True, null=True, help_text="Any special suggestions?")
    
    # Generated content
    plan_content = models.TextField()
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    view_count = models.IntegerField(default=0)
    is_anonymous = models.BooleanField(default=False)  # For confession mode
    
    # IP tracking (optional, for analytics)
    creator_ip = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['share_code']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.your_name} → {self.partner_name} ({self.relationship_type})"
    
    def increment_views(self):
        """Increment view count"""
        self.view_count += 1
        self.save(update_fields=['view_count'])


class Reaction(models.Model):
    """Store reactions to shared plans"""
    
    REACTION_CHOICES = [
        ('loved', '❤️ Loved it'),
        ('shocked', '😳 Shocked'),
        ('emotional', '🥹 Emotional'),
        ('laughing', '😂 Laughing'),
        ('crying', '😭 Crying'),
    ]
    
    plan = models.ForeignKey(ValentinePlan, on_delete=models.CASCADE, related_name='reactions')
    reaction_type = models.CharField(max_length=20, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Anonymous tracking (no user accounts needed)
    reactor_ip = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.reaction_type} on {self.plan.share_code}"


class LoveLetter(models.Model):
    """Store generated love letters"""
    
    plan = models.OneToOneField(ValentinePlan, on_delete=models.CASCADE, related_name='love_letter', null=True, blank=True)
    
    your_name = models.CharField(max_length=100)
    partner_name = models.CharField(max_length=100)
    letter_content = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Letter from {self.your_name} to {self.partner_name}"
