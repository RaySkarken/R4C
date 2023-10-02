import json

from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from django.core.exceptions import ValidationError, BadRequest
from django.views.decorators.csrf import csrf_exempt

from .models import Robot
from .services import string_validate_and_convert_to_datetime


@csrf_exempt  # To exempt from default requirement for CSRF tokens
def robots_view(request):
    if request.method == "POST":
        body = json.loads(request.body.decode("utf-8"))
        model = body.get('model')
        version = body.get('version')
        datetime_str = body.get('created')
        created_at = string_validate_and_convert_to_datetime(datetime_str)
        if any(map(lambda attr: attr is None, [model, version, created_at])):
            raise BadRequest()

        serial = f"{model}-{version}"

        robot = Robot.objects.filter(serial=serial).first()
        if robot is not None:
            raise ValidationError(message="Robot with the same serial already exists.")

        new_robot = Robot.objects.create(
            serial=serial,
            model=model,
            version=version,
            created=created_at
        )
        data = json.loads(serializers.serialize('json', [new_robot]))
        return JsonResponse(data, safe=False, status=201)
