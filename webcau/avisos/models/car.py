from .base import *
from .member import Member

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

