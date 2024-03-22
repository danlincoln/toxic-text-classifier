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
        p_not_toxic, p_toxic = probability
        p_not_toxic = f"{p_not_toxic:6.2%}"  # Prettify into percentages.
        p_toxic = f"{p_toxic:6.2%}"
        context["p_not_toxic"], context["p_toxic"] = p_not_toxic, p_toxic

    return render(request, "classifier_form.html", context)
