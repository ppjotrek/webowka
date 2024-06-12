from django.db import models

# Create your models here.
class ActiveSubstance(models.Model):
    act_sub_name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.act_sub_name
    
class AddedSubstance(models.Model):
    sub_name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.sub_name
    
class Drug(models.Model):
    drug_name = models.CharField(max_length=100)
    description = models.TextField()
    main_active_substance = models.ForeignKey(ActiveSubstance, on_delete=models.CASCADE)
    other_substances = models.ManyToManyField(AddedSubstance, blank=True)

    def __str__(self):
        return self.drug_name + ' (' + self.main_active_substance.act_sub_name + ')'
    
class Patient(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    birth_date = models.DateField()
    pesel = models.CharField(max_length=11)
    treatment_plan = models.TextField()
    drugs = models.ManyToManyField(Drug, blank=True)
    
    def __str__(self):
        return self.name + ' ' + self.surname + ' (' + self.pesel + ')'
