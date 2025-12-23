from decimal import Decimal

import stripe
from django.conf import settings


def _to_unit_amount(amount: Decimal) -> int:
    """
    Stripe принимает сумму в минимальных единицах валюты.
    Для RUB: рубли -> копейки (умножаем на 100).
    """
    return int((Decimal(amount) * 100).quantize(Decimal("1")))


def create_stripe_product(name: str, description: str = "") -> stripe.Product:
    stripe.api_key = settings.STRIPE_SECRET_KEY
    return stripe.Product.create(name=name, description=description)


def create_stripe_price(product_id: str, amount: Decimal, currency: str = "rub") -> stripe.Price:
    stripe.api_key = settings.STRIPE_SECRET_KEY
    return stripe.Price.create(
        product=product_id,
        unit_amount=_to_unit_amount(amount),
        currency=currency,
    )


def create_stripe_checkout_session(price_id: str) -> stripe.checkout.Session:
    stripe.api_key = settings.STRIPE_SECRET_KEY
    return stripe.checkout.Session.create(
        mode="payment",
        success_url=settings.STRIPE_SUCCESS_URL,
        cancel_url=settings.STRIPE_CANCEL_URL,
        line_items=[
            {"price": price_id, "quantity": 1},
        ],
    )
