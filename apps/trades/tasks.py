import logging
import smtplib

from celery import shared_task
from .models import Transactions
from django.contrib.auth import get_user_model
from .models import Stocks
UserModel = get_user_model()

@shared_task(bind=True, name="create_transaction", max_retries=3, autoretry_for=(Exception,), retry_backoff=True,
             queue="HIGH_PRIORITY_Q")
def create_transaction(self, transaction_data):
    try:
        transaction_data['owner'] = UserModel.objects.get(id = transaction_data['owner'])
        transaction_data['stock'] = Stocks.objects.get(id = transaction_data['stock'])
        Transactions.objects.create(**transaction_data)
        logging.info(f"Created transaction {transaction_data}")
    except smtplib.SMTPException:
        logging.error("Failed to send email")
    except Exception as exc:
        logging.error(str(exc))
        self.retry(exc=exc)
