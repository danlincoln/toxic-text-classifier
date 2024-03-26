from .models import MachineRating, Text
from django.shortcuts import render
import logging

logger = logging.getLogger("Views")


def main(request):
    return render(request, "classifier_form.html", {})


def classify(request):
    context = {"request": request}
    try:
        unprocessed_text = request.POST["unprocessed_text"]
        if not unprocessed_text:
            raise ValueError("Text cannot be empty.")
    except (KeyError, ValueError) as e:
        message = f"{type(e).__name__}: {e}"
        logger.error(message)
        context["error_message"] = message
    else:
        # Build text object and run classification.
        text = Text(unprocessed=unprocessed_text)
        rating, probability = text.classify()

        # Build machine rating object with the results.
        machinerating = MachineRating(rating=rating, text=text)

        # Save to the db.
        text.save()
        machinerating.save()

        # Return results to the template (view).
        context["text"] = text
        context["probability"] = f"{probability:6.2%}"

    return render(request, "classifier_form.html", context)
