import uuid

from django.utils.timezone import now
from datetime import timedelta

from store.celery import app
from users.models import User, EmailVerification


@app.task
def send_verification_email(user_id):
    try:
        user = User.objects.get(id=user_id)
        expiration = now() + timedelta(hours=48)
        record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
        record.send_verification_email()
    except Exception as e:
        print(e)