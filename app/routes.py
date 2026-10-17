
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)
from app.database import get_db
from app.models import User, FitnessClass, Booking
from app.schemas import (
    UserSignup,
    UserLogin,
    TokenResponse,
    FitnessClassCreate,
    FitnessClassResponse,
    BookingCreate,
    BookingResponse,
    MyBookingResponse,
)


router = APIRouter()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(data: UserSignup, db: Session = Depends(get_db)):
    """Register a new user."""

    email = str(data.email).lower()

    existing_user = db.scalar(
        select(User).where(User.email == email)
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )

    user = User(
        name=data.name,
        email=email,
        hashed_password=hash_password(data.password),
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception:
        db.rollback()
        raise

    return {
        "message": "Registration successful.",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        },
    }


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    """Authenticate a user and return a JWT."""

    email = str(data.email).lower()

    user = db.scalar(
        select(User).where(User.email == email)
    )

    if not user or not verify_password(
        data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

IST = ZoneInfo("Asia/Kolkata")


@router.post(
    "/classes",
    response_model=FitnessClassResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_class(
    data: FitnessClassCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a fitness class. Login is required."""

    class_time_ist = data.date_time.astimezone(IST)

    if class_time_ist <= datetime.now(IST):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Class dateTime must be in the future.",
        )

    fitness_class = FitnessClass(
        name=data.name,
        date_time=class_time_ist,
        instructor=data.instructor,
        available_slots=data.available_slots,
    )

    db.add(fitness_class)
    db.commit()
    db.refresh(fitness_class)

    return fitness_class


@router.get("/classes", response_model=list[FitnessClassResponse])
def get_upcoming_classes(db: Session = Depends(get_db)):
    """Return all upcoming fitness classes, displayed in IST."""

    now = datetime.now(timezone.utc)

    classes = (
        db.query(FitnessClass)
        .filter(FitnessClass.date_time > now)
        .order_by(FitnessClass.date_time.asc())
        .all()
    )

    return classes

@router.post(
    "/book",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
)
def book_class(
    data: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Check if the class exists
    fitness_class = db.get(FitnessClass, data.class_id)

    if fitness_class is None:
        raise HTTPException(
            status_code=404,
            detail="Fitness class not found.",
        )

    # Check whether the class is in the future
    if fitness_class.date_time <= datetime.now(timezone.utc):
        raise HTTPException(
            status_code=400,
            detail="This class has already passed.",
        )

    # Prevent duplicate bookings
    existing_booking = db.scalar(
        select(Booking).where(
            Booking.user_id == current_user.id,
            Booking.class_id == data.class_id,
        )
    )

    if existing_booking:
        raise HTTPException(
            status_code=409,
            detail="You have already booked this class.",
        )

    try:
        # Reduce a slot only if at least one is available
        result = db.execute(
            update(FitnessClass)
            .where(
                FitnessClass.id == data.class_id,
                FitnessClass.available_slots > 0,
            )
            .values(
                available_slots=FitnessClass.available_slots - 1
            )
            .returning(FitnessClass.id)
        )

        if result.scalar_one_or_none() is None:
            db.rollback()
            raise HTTPException(
                status_code=409,
                detail="No available slots remain.",
            )

        booking = Booking(
            user_id=current_user.id,
            class_id=data.class_id,
            client_name=data.client_name,
            client_email=str(data.client_email).lower(),
        )

        db.add(booking)
        db.commit()
        db.refresh(booking)

        return booking

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="You have already booked this class.",
        )
    except Exception:
        db.rollback()
        raise


@router.get(
    "/bookings",
    response_model=list[MyBookingResponse],
)
def get_my_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    bookings = (
        db.query(Booking)
        .filter(Booking.user_id == current_user.id)
        .order_by(Booking.created_at.desc())
        .all()
    )

    return bookings
