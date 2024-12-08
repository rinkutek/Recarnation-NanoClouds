from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Car
from datetime import datetime


# Test for Car Model
class CarModelTest(TestCase):


   def setUp(self):
       # Create a user for the car
       self.user = User.objects.create_user(username='testuser', password='12345')
      
       # Create a car instance
       self.car = Car.objects.create(
           car_title="Test Car",
           state="CA",
           city="San Francisco",
           color="Red",
           model="Tesla Model 3",
           year=2022,
           condition="New",
           price=35000,
           description="A brand new Tesla Model 3.",
           features=["Cruise Control", "Bluetooth Handset"],
           body_style="Sedan",
           engine="Electric",
           transmission="Automatic",
           interior="Leather",
           miles=0,
           doors="4",
           passengers=5,
           vin_no="1234567890ABCDEF",
           milage=0,
           fuel_type="Electric",
           no_of_owners="1",
           is_featured=True,
           status="Approved",
           seller=self.user
       )


   def test_car_creation(self):
       """Test if the car is created successfully"""
       self.assertEqual(self.car.car_title, "Test Car")
       self.assertEqual(self.car.city, "San Francisco")
       self.assertEqual(self.car.status, "Approved")


   def test_car_str_method(self):
       """Test the string representation of the car"""
       self.assertEqual(str(self.car), "Test Car")




# Test for Approve Cars View (Requires staff user)
class ApproveCarsViewTest(TestCase):


   def setUp(self):
       # Create a staff user
       self.staff_user = User.objects.create_user(username='staffuser', password='12345')
       self.staff_user.is_staff = True
       self.staff_user.save()


       # Create a car in "Pending" status
       self.car = Car.objects.create(
           car_title="Pending Car",
           state="CA",
           city="Los Angeles",
           color="Blue",
           model="Ford Mustang",
           year=2023,
           condition="Used",
           price=25000,
           description="A used Ford Mustang.",
           features=["Cruise Control"],
           body_style="Coupe",
           engine="V8",
           transmission="Manual",
           interior="Leather",
           miles=1000,
           doors="2",
           passengers=2,
           vin_no="0987654321XYZ",
           milage=1000,
           fuel_type="Gasoline",
           no_of_owners="2",
           is_featured=False,
           status="Pending",
           seller=self.staff_user
       )
  
   def test_approve_car_view(self):
       """Test the approve car view"""
       self.client.login(username='staffuser', password='12345')  # Login as staff
       url = '/approve_cars/'  # Use the actual path here
       response = self.client.get(url)
       self.assertEqual(response.status_code, 404)
       self.assertContains(response, 'Pending Car')


   def test_approve_car_view(self):
       """Test the approve car view"""
       self.client.login(username='staffuser', password='12345')  # Login as staff
       url = reverse('approve_cars')  # Ensure the name matches your URL pattern
       response = self.client.get(url)
       self.assertEqual(response.status_code, 200)
       self.assertContains(response, 'Pending Car')


   def test_approve_car_action(self):
       """Test approving a car"""
       self.client.login(username='staffuser', password='12345')  # Login as staff
       url = reverse('approve_cars')  # Ensure the name matches your URL pattern
       response = self.client.post(url, {'car_id': self.car.id, 'action': 'approve'})
       self.car.refresh_from_db()
       self.assertEqual(self.car.status, 'Approved')


   def test_reject_car_action(self):
       """Test rejecting a car"""
       self.client.login(username='staffuser', password='12345')  # Login as staff
       url = reverse('approve_cars')  # Ensure the name matches your URL pattern
       response = self.client.post(url, {'car_id': self.car.id, 'action': 'reject'})
       self.car.refresh_from_db()
       self.assertEqual(self.car.status, 'Rejected')


