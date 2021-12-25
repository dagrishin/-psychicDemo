from django.conf import settings
from django.shortcuts import render
from .forms import RenewForm
import random


def guess_psychic():
    return random.randint(10, 99)


def change_confidence_level(level, guess, coefficient=10):
    return level + coefficient if guess else level - coefficient


def create_response(psychics_stat, number_of_psychics):
    response = {}
    for number_psychic in range(1, number_of_psychics):
        response[str(number_psychic)] = {
            'state': ", ".join(list(map(str, psychics_stat[f"psychic_{number_psychic}_state"]))),
            'confidence_level': psychics_stat[f"psychic_{number_psychic}_confidence_level"],
        }
    return response


def index(request):
    number_of_psychics = settings.NUMBER_OF_PSYCHICS
    psychics_stat = {}
    for number_psychic in range(1, number_of_psychics):
        psychics_stat[f"psychic_{number_psychic}_state"] = request.session.get(f"psychic_{number_psychic}_state", [])
        psychics_stat[f"psychic_{number_psychic}_confidence_level"] = request.session.get(
            f"psychic_{number_psychic}_confidence_level", 0)
    numbers = request.session.get('numbers', [])
    form = RenewForm(request.POST if request.POST else None)
    if request.method == 'POST':
        if form.is_valid():
            number = form.cleaned_data['number']
            numbers.append(number)
            request.session['numbers'] = numbers
            for number_psychic in range(1, number_of_psychics):
                guesstimate = guess_psychic()
                guess = False
                if guesstimate == number:
                    guess = True
                if psychics_stat[f"psychic_{number_psychic}_state"] is None:
                    psychics_stat[f"psychic_{number_psychic}_state"] = []
                psychics_stat[
                    f"psychic_{number_psychic}_state"].append(guesstimate)
                request.session[f"psychic_{number_psychic}_state"] = psychics_stat[f"psychic_{number_psychic}_state"]
                psychics_stat[f"psychic_{number_psychic}_confidence_level"] = change_confidence_level(
                    level=psychics_stat[f"psychic_{number_psychic}_confidence_level"],
                    guess=guess,
                )
                request.session[f"psychic_{number_psychic}_confidence_level"] = psychics_stat[
                    f"psychic_{number_psychic}_confidence_level"
                ]
    response = create_response(psychics_stat, number_of_psychics)
    return render(
        request,
        'psychic/index.html',
        context={
            'numbers': ", ".join(list(map(str,numbers))),
            'form': form,
            'response': response,
        },
    )
