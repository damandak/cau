from django.db.models.signals import pre_save
from django.dispatch import receiver
from .base import *

class EmergencyContact(BaseModel):
    member = models.ForeignKey('avisos.Member', on_delete=models.CASCADE)
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

