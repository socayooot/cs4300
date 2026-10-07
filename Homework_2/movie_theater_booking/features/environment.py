"""Behave hooks: give every scenario a fresh web client and API client."""
from django.test import Client
from rest_framework.test import APIClient


def before_scenario(context, scenario):
    context.client = Client()
    context.api = APIClient()
