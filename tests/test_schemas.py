
import pytest
from pydantic import ValidationError

from app.schemas import (
    UserSignup,
    UserLogin,
    FitnessClassCreate,
    BookingCreate,
)


def test_valid_signup():
    # Check that valid user details are accepted.
    user = UserSignup(
        name="Ragini",
        email="ragini@example.com",
        password="securepass123",
    )

    assert user.name == "Ragini"
    assert user.email == "ragini@example.com"


def test_signup_rejects_short_password():
    # Passwords shorter than 8 characters must be rejected.
    with pytest.raises(ValidationError):
        UserSignup(
            name="Ragini",
            email="ragini@example.com",
            password="123",
        )


def test_login_rejects_invalid_email():
    # Login must reject an invalid email address.
    with pytest.raises(ValidationError):
        UserLogin(
            email="not-an-email",
            password="securepass123",
        )


def test_class_requires_timezone():
    # Class date and time must include a timezone.
    with pytest.raises(ValidationError):
        FitnessClassCreate(
            name="Yoga Flow",
            dateTime="2026-11-13T10:00:00",
            instructor="John Doe",
            availableSlots=20,
        )


def test_class_rejects_negative_slots():
    # Available slots cannot be negative.
    with pytest.raises(ValidationError):
        FitnessClassCreate(
            name="Yoga Flow",
            dateTime="2026-11-13T10:00:00+05:30",
            instructor="John Doe",
            availableSlots=-1,
        )


def test_booking_requires_valid_class_id():
    # Class IDs must be positive integers.
    with pytest.raises(ValidationError):
        BookingCreate(
            class_id=0,
            client_name="Alice",
            client_email="alice@example.com",
        )


def test_valid_booking():
    # Check that valid booking details are accepted.
    booking = BookingCreate(
        class_id=1,
        client_name="Alice",
        client_email="alice@example.com",
    )

    assert booking.class_id == 1
    assert booking.client_name == "Alice"
    assert booking.client_email == "alice@example.com"