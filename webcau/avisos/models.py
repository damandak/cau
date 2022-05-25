import email
from email.policy import default
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from annoying.fields import AutoOneToOneField
from datetime import datetime, timezone, timedelta
from django.utils import timezone as tz
from django.core.exceptions import ValidationError
from django.core.mail import send_mail


def file_size(value): 
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('Archivo excede los 2MB')

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

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

class Car(BaseModel):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    alias = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    color = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=100)
    def __str__(self):
        if self.alias:
            return str(self.member.name) +  " - " + str(self.alias) + " - " + str(self.license_plate)
        else:
            return " - " + str(self.member.name) + " - " + str(self.license_plate)

class MedicalRecord(BaseModel):
    member = AutoOneToOneField(Member, primary_key=True, on_delete=models.CASCADE)
    no_medical_record = models.BooleanField(default=False)
    sicknesses = models.TextField(null=True, blank=True)
    medications = models.TextField(null=True, blank=True)
    risks = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return str(self.member) + " - " + str(self.sicknesses)
    
    def pending(self):
        if self.no_medical_record:
            return False
        if self.sicknesses or self.medications or self.risks:
            return False
        return True

@receiver(post_save, sender=Member)
def create_member_medical(sender, instance, created, **kwargs):
    if created:
        MedicalRecord.objects.create(member=instance)

@receiver(post_save, sender=Member)
def save_member_medical(sender, instance, **kwargs):
    instance.medicalrecord.save()

class NoticeCategory(BaseModel):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class BaseNotice(BaseModel):
    # ¿Cómo lo hacemos con gente que no es del CAU?
    description = models.TextField(blank=True, null=True)
    DRAFT = 0
    PUBLISHED = 1
    ACTIVE = 2
    LATE = 3
    ARRIVED = 4
    CANCELLED = 5
    STATUS_CHOICES = (
        (DRAFT, 'Borrador'),
        (PUBLISHED, 'Publicado'),
        (ACTIVE, 'Activo'),
        (LATE, 'Retrasado'),
        (ARRIVED, 'Llegado'),
        (CANCELLED, 'Cancelado'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT)
    category = models.ForeignKey(NoticeCategory, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=datetime.now, blank=True)
    max_end_date = models.DateTimeField(default=datetime.now, blank=True)
    participants = models.ManyToManyField(Member, blank=True)
    cars = models.ManyToManyField(Car, blank=True)
    cau_contact = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="cau_contact", blank=True, null=True)

    email_recipients = models.ManyToManyField(EmailRecipient, blank=True, related_name="email_recipients")
    sent_date = models.DateTimeField(null=True, blank=True)
    sent_by = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="sent_by", blank=True, null=True)

    def include_email(self, email):
        if EmailRecipient.objects.filter(email=email).exists():
            self.email_recipients.add(EmailRecipient.objects.get(email=email))
        else:
            self.email_recipients.add(EmailRecipient.objects.create(email=email))

    def include_caucontacts(self):
        if self.cau_contact:
            self.include_email(self.cau_contact.user.email)

    def include_participants(self):
        for member in self.participants.all():
            self.include_email(member.user.email)

    def include_board(self):
        if ClubBoard.objects.count() > 0:
            for member in ClubBoard.objects.first().members.all():
                self.include_email(member.user.email)
    
    def include_emergencycontacts(self):
        for member in self.participants.all():
            if member.main_emergencycontact:
                self.include_email(member.main_emergencycontact.email)

    def include_caumembers(self):
        # Horrible Hardcodeo
        self.include_email("montanismo-uc@googlegroups.com")

    def publish_notice(self, mail_content=None):
        self.mail(publication=True, mail_content=mail_content)
        if datetime.now(self.max_end_date.tzinfo) >= self.max_end_date:
            self.late_notice()
        elif datetime.now(self.start_date.tzinfo) >= self.start_date:   
            self.activate_notice()
        else:
            print("start chron 2")
            print("publicado")
            self.status = self.PUBLISHED
            self.save()
    
    def activate_notice(self):
        if datetime.now(self.max_end_date.tzinfo) >= self.max_end_date:
            self.late_notice()
        else:
            print("start chron 3")
            print("activado")
            self.status = self.ACTIVE
            self.save()

    def late_notice(self):
        print("atrasado")
        self.status = self.LATE
        self.save()
        self.mail(late=True)

    def notify_arrival(self):
        print("llegado")
        self.status = self.ARRIVED
        self.save()
        self.mail(arrival=True)

    def cancel_notice(self):
        print("cancelado")
        self.status = self.CANCELLED
        self.save()
        self.mail(cancellation=True)
    

    def mail(self, publication=False, arrival=False, late=False, cancel=False, mail_content=None):
        if publication:
            print("Enviando correo de aviso de salida")
            mail_title = 'Aviso de Salida Corta: ' + self.location
            if mail_content:
                mail_content = mail_content
            else:
                mail_content = 'Sin contenido.'
            mail_sender = self.sent_by.user.email
            mail_recipients = self.email_recipients.all()
        elif late:
            mail_title = 'Aviso de Atraso: ' + self.location
            mail_content = 'TEXTO DE EXPLICACIÓN CON LINK DIRECTO?.'
            mail_sender = self.sent_by.user.email # O un correo institucional?
            mail_recipients = self.email_recipients.all() # CAMBIAR ESTO, debiera sacarse a los contactos de emergencia y al correo CAU
        elif arrival:
            mail_title = 'Aviso de Llegada: ' + self.location
            mail_content = 'Sin contenido.' # Debiera incluirse un texto de llegada? como funcionaría esto?
            mail_sender = self.sent_by.user.email # O un correo institucional? O quien notifica?
            mail_recipients = self.email_recipients.all() # ESTÁ BIEN PORQUE DEBE SER LA MISMA GENTE QUE RECIBIÓ EL AVISO INICIALMENTE
        elif cancel:
            mail_title = 'Aviso Cancelado: ' + self.location
            mail_content = 'TEXTO DE EXPLICACIÓN CANCELACIÓN' # Debiera incluirse un texto de llegada? como funcionaría esto?
            mail_sender = self.sent_by.user.email # O un correo institucional? O quien notifica?
            mail_recipients = self.email_recipients.all() # ESTÁ BIEN PORQUE DEBE SER LA MISMA GENTE QUE RECIBIÓ EL AVISO INICIALMENTE
        else:
            return
        send_mail(mail_title, mail_content, mail_sender, mail_recipients)
    
    @property
    def time_left_for_arrival(self):
        now = tz.now()
        print(now)
        print(self.max_end_date)
        result = self.max_end_date - now
        print(result)
        return result.total_seconds()

@receiver(post_save, sender=BaseNotice)
def notice_handler(sender, instance, created, **kwargs):
    if created:
        if instance.status == instance.DRAFT:
            if instance.max_end_date <= datetime.now():
                # Alert that the notice was never activated and can't be published
                instance.cancel_notice()
            elif instance.start_date <= datetime.now():
                # Start chron 3 until end date IF chron 3 not started yet
                # Alert that the notice is not yet published
                print("Notice is not published yet!!")
            elif instance.start_date - timedelta(hours=8) <= datetime.now():
                # Start chron 2 until start_date IF chron 2 not started yet
                # Alert that the notice is not yet published
                print("Starting chron 2")
            else:
                # Start chron 1 until 8 hours before start_date IF chron 1 not started yet
                print("Starting chron 1")
        elif instance.status == instance.PUBLISHED:
            instance.publish_notice()
        elif instance.status == instance.ACTIVE:
            if instance.max_end_date <= datetime.now():
                instance.late_notice()
            else:
                print("Starting chron 3")

class ShortNotice(BaseNotice):
    location = models.CharField(max_length=100)
    route = models.CharField(max_length=100)
    # definir como asociar members con emergency contacts

    def __str__(self):
        return self.category.name + ": " + self.location + " - " + self.route

class EmergencyContact(BaseModel):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    main_contact = models.BooleanField(default=False)
    relationship = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['main_contact', 'member'], condition=models.Q(main_contact=True), name='unique_main_contact'),
        ]

    def __str__(self):
        return str(self.name)

@receiver(pre_save, sender=EmergencyContact)
def set_main_contact(sender, instance, **kwargs):
    if instance.main_contact:
        EmergencyContact.objects.filter(main_contact=True, member=instance.member).update(main_contact=False)

