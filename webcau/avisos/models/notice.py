from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta
from django.utils import timezone as tz
from django.core.mail import send_mail
from .base import *
from .member import Member, EmailRecipient, ClubBoard, ClubBoardMember
from .car import Car

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
    arrival_confirmation_date = models.DateTimeField(null=True, blank=True)
    arrival_confirmation_by = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="arrival_confirmation_by", blank=True, null=True)

    def allowed_to_edit(self):
        return list(self.participants.all()) + [self.cau_contact]

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
