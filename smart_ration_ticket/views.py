from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .models import Supplier, DistributionSession, UserBooking
from datetime import datetime, date
from django.contrib import messages  # Optional for flash messaging
import qrcode
from io import BytesIO
import base64
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.models import User
from django.contrib.auth import logout


def supplier_register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        agent_name = request.POST["agent_name"]
        phone = request.POST["phone"]
        center_code = request.POST["center_code"]
        address = request.POST["address"]
        availability_days = request.POST["availability_days"]

        # Create user
        user = User.objects.create_user(username=username, password=password)

        # Create supplier profile
        Supplier.objects.create(
            user=user,
            agent_name=agent_name,
            phone=phone,
            center_code=center_code,
            address=address,
            availability_days=availability_days,
        )

        return redirect("supplier_login")

    return render(request, "core/supplier_register.html")


def supplier_login_view(request):
    error = None
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("supplier_dashboard")
        else:
            error = "Invalid username or password"
    return render(request, "core/supplier_login.html", {"error": error})


@login_required
def supplier_dashboard_view(request):
    supplier = Supplier.objects.get(user=request.user)
    today = date.today()

    # Get or create today's session
    session, created = DistributionSession.objects.get_or_create(
        supplier=supplier, date=today
    )

    # Generate booking link
    link = request.build_absolute_uri(
        f"/user/book/{session.supplier.center_code}/{session.id}/"
    )

    # Generate QR Code as base64
    qr = qrcode.make(link)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    # Count today's registrations
    registrations_today = UserBooking.objects.filter(session=session).count()

    # Get the current booking for this token (if exists)
    current_booking = UserBooking.objects.filter(
        session=session, token_number=session.current_token
    ).first()

    # Update session details if POST (session setup form)
    if request.method == "POST":
        session.start_time = request.POST.get("start_time")
        session.end_time = request.POST.get("end_time")
        session.status = request.POST.get("status")
        session.max_tokens = request.POST.get("max_tokens")
        session.save()

    return render(
        request,
        "core/supplier_dashboard.html",
        {
            "supplier": supplier,
            "session": session,
            "qr_code": qr_base64,
            "link": link,
            "registrations_today": registrations_today,
            "current_booking": current_booking,
        },
    )


@login_required
def update_ticket_status(request, booking_id):
    booking = get_object_or_404(UserBooking, id=booking_id)
    session = booking.session

    if request.method == "POST":
        new_status = request.POST.get("status")
        booking.status = new_status
        booking.save()

        # Automatically move to next token if current one is closed or cancelled
        if (
            new_status in ["closed", "cancelled"]
            and session.current_token == booking.token_number
        ):
            next_token = session.current_token + 1
            if next_token <= session.max_tokens:
                session.current_token = next_token
                session.save()

    return redirect("supplier_dashboard")


def user_booking_form(request, ration_card, session_id):
    session = DistributionSession.objects.get(id=session_id)
    today = date.today()

    if session.status != "open" or session.date != today:
        return render(request, "core/user_booking_closed.html", {"session": session})

    total_booked = UserBooking.objects.filter(session=session).count()
    remaining_tokens = session.max_tokens - total_booked

    if request.method == "POST":
        ration_card = request.POST.get("ration_card")
        phone = request.POST.get("phone")

        if UserBooking.objects.filter(
            ration_card_number=ration_card, date=today
        ).exists():
            return HttpResponseRedirect(
                reverse("user_booking_with_card", args=[session.id, ration_card])
            )

        if remaining_tokens <= 0:
            return render(
                request,
                "core/user_booking_form.html",
                {
                    "session": session,
                    "prefill_card": ration_card,
                    "error": "No more tokens available for today.",
                    "remaining_tokens": remaining_tokens,
                },
            )

        token_number = total_booked + 1
        UserBooking.objects.create(
            ration_card_number=ration_card,
            phone=phone,
            date=today,
            token_number=token_number,
            session=session,
        )

        return HttpResponseRedirect(reverse("user_status", args=[ration_card]))

    return render(
        request,
        "core/user_booking_form.html",
        {
            "session": session,
            "prefill_card": ration_card,
            "remaining_tokens": remaining_tokens,
        },
    )


def user_ticket_status(request, ration_card_number):
    today = date.today()
    booking = UserBooking.objects.filter(
        ration_card_number=ration_card_number, date=today
    ).first()

    if not booking:
        return render(request, "core/user_no_booking.html")

    # Estimated wait time: assume 3 minutes per token
    estimated_wait = max(0, (booking.token_number - booking.session.current_token) * 3)

    return render(
        request,
        "core/user_ticket_status.html",
        {"booking": booking, "wait_time": estimated_wait, "session": booking.session},
    )


@csrf_exempt
def supplier_profile_update(request):
    if request.method == "POST":
        supplier = Supplier.objects.get(user=request.user)
        supplier.agent_name = request.POST.get("agent_name")
        supplier.phone = request.POST.get("phone")
        supplier.center_code = request.POST.get("center_code")
        supplier.address = request.POST.get("address")
        supplier.availability_days = request.POST.get("availability_days")
        supplier.save()
    return redirect("supplier_dashboard")


def logout_view(request):
    logout(request)
    return redirect("supplier_login")
