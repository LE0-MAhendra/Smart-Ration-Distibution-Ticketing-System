from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Supplier, DistributionSession, UserBooking
from datetime import date


class SupplierTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.supplier = Supplier.objects.create(
            user=self.user,
            agent_name="Test Agent",
            phone="9999999999",
            center_code="C123",
            address="Test Address",
            availability_days=5,
        )

    def test_supplier_creation(self):
        self.assertEqual(self.supplier.agent_name, "Test Agent")
        self.assertEqual(str(self.supplier), "Test Agent")


class DistributionSessionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="sessionuser", password="password123"
        )
        self.supplier = Supplier.objects.create(
            user=self.user,
            agent_name="Session Agent",
            phone="8888888888",
            center_code="C456",
            address="Session Address",
            availability_days=6,
        )
        self.session = DistributionSession.objects.create(
            supplier=self.supplier, date=date.today(), max_tokens=30
        )

    def test_session_creation(self):
        self.assertEqual(self.session.max_tokens, 30)
        self.assertEqual(
            str(self.session), f"{self.supplier.agent_name} - {self.session.date}"
        )


class UserBookingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="bookinguser", password="password123"
        )
        self.supplier = Supplier.objects.create(
            user=self.user,
            agent_name="Booking Agent",
            phone="7777777777",
            center_code="C789",
            address="Booking Address",
            availability_days=7,
        )
        self.session = DistributionSession.objects.create(
            supplier=self.supplier, date=date.today(), max_tokens=40
        )
        self.booking = UserBooking.objects.create(
            ration_card_number="RC123456",
            phone="6666666666",
            date=date.today(),
            token_number=1,
            session=self.session,
        )

    def test_booking_created(self):
        self.assertEqual(self.booking.token_number, 1)
        self.assertEqual(str(self.booking), "RC123456 - Token 1")


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = "viewuser"
        self.password = "password123"
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )
        self.supplier = Supplier.objects.create(
            user=self.user,
            agent_name="View Agent",
            phone="9998887777",
            center_code="C321",
            address="View Address",
            availability_days=3,
        )

    def test_supplier_login_view_get(self):
        response = self.client.get(reverse("supplier_login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/supplier_login.html")

    def test_supplier_login_view_post_success(self):
        response = self.client.post(
            reverse("supplier_login"),
            {
                "username": self.username,
                "password": self.password,
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirect to dashboard

    def test_supplier_dashboard_view_auth_required(self):
        response = self.client.get(reverse("supplier_dashboard"))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_supplier_register_view(self):
        response = self.client.post(
            reverse("supplier_register"),
            {
                "username": "newuser",
                "password": "newpass",
                "agent_name": "New Agent",
                "phone": "1234567890",
                "center_code": "NEW123",
                "address": "New Address",
                "availability_days": 4,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Supplier.objects.filter(agent_name="New Agent").exists())
