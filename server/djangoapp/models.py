# Uncomment the following imports before adding the Model code

from django.db import models
# from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Other fields as needed

    def __str__(self):
        return self.name  # Return the name as the string representation

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many
# Car Models, using ForeignKey field)
# - Name
# - Type (CharField with a choices argument to provide limited choices
# such as Sedan, SUV, WAGON, etc.)
# - Year (IntegerField) with min value 2015 and max value 2023
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object


class CarModel(models.Model):
    # Many-to-One relationship
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    CAR_TYPES = [
        ('COUPE', 'Coupe'),
        ('CONVERTIBLE', 'Convertible'),
        ('HATCHBACK', 'Hatchback'),
        ('SUV', 'SUV'),
        ('SEDAN', 'Sedan'),
        ('MINIVAN', 'Minivan'),
        ('CROSSOVER', 'Crossover'),
        ('SPORTS_CAR', 'Sports car'),
        ('TRUCK', 'Truck'),
        ('WAGON', 'Wagon'),
        ('MPV', 'MPV'),
        ('HYBRID', 'Hybrid'),
        ('JEEP', 'Jeep'),
        ('COMPACT', 'Compact'),
        ('LIMOUSINE', 'Limousine'),
        ('MUSCLE_CARS', 'Muscle cars'),
        ('ESTATE', 'Estate'),
        ('SALOON', 'Saloon'),
        # Add more choices as required
    ]
    type = models.CharField(max_length=20, choices=CAR_TYPES, default='SUV')
    year = models.IntegerField(
        default=2024,
        validators=[
            MaxValueValidator(2024),
            MinValueValidator(2015)
        ]
    )
    # Other fields as needed
    engine_type = models.CharField(max_length=50, blank=True)
    TRANS_TYPES = [
        ('AUTOMATIC', 'Automatic'),
        ('MANUAL', 'Manual'),
        # Add more choices as required
    ]
    transmisson_type = models.CharField(
        max_length=20,
        choices=TRANS_TYPES,
        default='AUTOMATIC',
        blank=True
    )
    transmission_speed = models.CharField(max_length=50, blank= True)

    def __str__(self):
        return self.name  # Return the name as the string representation