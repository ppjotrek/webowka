from django.db import models
from django.utils import timezone

# Create your models here.
class ActiveSubstance(models.Model):
    act_sub_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.act_sub_name
    
class AddedSubstance(models.Model):
    sub_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.sub_name
    
class Drug(models.Model):
    drug_name = models.CharField(max_length=100)
    description = models.TextField()
    main_active_substance = models.ForeignKey(ActiveSubstance, on_delete=models.CASCADE)
    other_substances = models.ManyToManyField(AddedSubstance, blank=True)

    @property
    def added_substances_list(self):
        if self.other_substances.count() == 0:
            return 'Brak dodatkowych substancji'
        else:
            return ', '.join([str(substance) for substance in self.other_substances.all()])

    def __str__(self):
        return self.drug_name + ' (' + self.main_active_substance.act_sub_name + ')'
    
class Patient(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    birth_date = models.DateField()
    pesel = models.CharField(max_length=11)
    contact = models.CharField(max_length=100, blank=True)
    treatment_plan = models.TextField(blank=True)
    current_drugs = models.ForeignKey(Drug, blank=True, null=True, on_delete=models.CASCADE)
    drug_end_date = models.DateField(blank=True, null=True)
    allergies_for_active = models.ManyToManyField(ActiveSubstance, blank=True)
    allergies_for_added = models.ManyToManyField(AddedSubstance, blank=True)

    @property
    def age(self):
        today = timezone.now().date()
        age = int(
            today.year
            - (self.birth_date.year)
            - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        )
        return age
    
    @property
    def get_current_drugs(self):
        if self.current_drugs is None:
            return 'Brak leków'
        else:
            if self.drug_end_date is not None:
                if self.drug_end_date < timezone.now().date():
                    return 'Brak leków'
                else:
                    return str(self.current_drugs) + ' (do ' + str(self.drug_end_date) + ')'
            else:
                return str(self.current_drugs)
        
    @property
    def get_allergies(self):
        if self.allergies_for_active.count() == 0 and self.allergies_for_added.count() == 0:
            return 'Brak alergii'
        elif self.allergies_for_active.count() == 0:
            return ', '.join([str(substance) for substance in self.allergies_for_added.all()])
        elif self.allergies_for_added.count() == 0:
            return ', '.join([str(substance) for substance in self.allergies_for_active.all()])
        else:
            return ', '.join([str(substance) for substance in self.allergies_for_active.all()]) + ', ' + ', '.join([str(substance) for substance in self.allergies_for_added.all()])
    
    def __str__(self):
        return self.name + ' ' + self.surname + ' (' + self.pesel + ')'


class PatientManager(models.Manager):
    def create_patient(self, name, surname, birth_date, pesel, treatment_plan=None, drugs=None, allergies_for_active=None, allergies_for_added=None):
        patient = self.create(name=name, surname=surname, birth_date=birth_date, pesel=pesel, treatment_plan=treatment_plan)
        patient.drug.set(drugs)
        return patient
    
class DrugManager(models.Manager):
    def create_drug(self, drug_name, description, main_active_substance, other_substances=None):
        other_substances_list = []
        if other_substances is None:
            other_substances = []
        if ActiveSubstance.objects.filter(act_sub_name=main_active_substance).exists():
            main_active_substance = ActiveSubstance.objects.get(act_sub_name=main_active_substance)
        else:
            main_active_substance = ActiveSubstance.objects.create(act_sub_name=main_active_substance, description='Brak opisu')
        for substance in other_substances:
            if AddedSubstance.objects.filter(sub_name=substance).exists():
                other_substances_list.append(AddedSubstance.objects.get(sub_name=substance))
            else:
                other_substances_list.append(AddedSubstance.objects.create(sub_name=substance, description='Brak opisu'))
        other_substances_str = str(other_substances_list)
        drug = self.create(drug_name=drug_name, description=description, main_active_substance=main_active_substance, other_substances=other_substances_str)
        return drug