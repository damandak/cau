from .base import *
from .member import Member

class Car(SoftDeletionModel):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True)
    alias = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    color = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=100)

    def delete(self):
      self.member = None
      self.save()

    def __str__(self):
        if self.member:
            if self.alias:
                return str(self.member.name) +  " - " + str(self.alias) + " - " + str(self.license_plate)
            else:
                return " - " + str(self.member.name) + " - " + str(self.license_plate)
        else:
            return " - "

