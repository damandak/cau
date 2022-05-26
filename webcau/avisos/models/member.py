from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .base import *
from .emergencycontact import EmergencyContact

#   Member model. Pending: member status, image, signature, etc.
class Member(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    middlename = models.CharField(max_length=100, blank=True)
    first_surname = models.CharField(max_length=100)
    second_surname = models.CharField(max_length=100, blank=True)
    rut = models.CharField(max_length=20)
    birth_date = models.DateField(null=True, blank=True)
    enrollment_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    use_middlename = models.BooleanField(default=False)
    use_second_surname = models.BooleanField(default=False)

    profile_image = models.ImageField(upload_to='profile_images', blank=True, validators =[file_size], default = 'default.png')

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('member-detail', kwargs={'pk': self.pk})
    
    def __str__(self):
        if self.name and self.first_surname:
            middle = (self.middlename + " ") if self.use_middlename else ""
            last = self.second_surname if self.use_second_surname else ""
            names = self.name + " " + middle
            surnames = self.first_surname + " " + last
            return names + surnames
        return self.user.username

    @property
    def main_emergencycontact(self):
        return EmergencyContact.objects.filter(member=self, main_contact=True).first()

@receiver(post_save, sender=User)
def create_user_member(sender, instance, created, **kwargs):
    if created:
        Member.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_member(sender, instance, **kwargs):
    instance.member.save()

class ClubBoard(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(Member, blank=True, through='ClubBoardMember')

    def __str__(self):
        return self.name

class ClubBoardMember(BaseModel):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    clubboard = models.ForeignKey(ClubBoard, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    receivenotices = models.BooleanField(default=True)

    def __str__(self):
        return self.position + " en " + self.clubboard.name

class Committee(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(Member, blank=True, through='CommitteeMember')

    def __str__(self):
        return self.name

class CommitteeMember(BaseModel):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)

    def __str__(self):
        return self.position + " en " + self.committee.name

class EmailRecipient(BaseModel):
    email = models.EmailField(max_length=254)
    def __str__(self):
        return str(self.email)
