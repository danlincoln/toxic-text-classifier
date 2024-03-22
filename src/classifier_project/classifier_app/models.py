from .classifier import Classifier, preprocess
from django.db import models


class Text(models.Model):
    unprocessed = models.TextField()
    processed = models.TextField()
    classifier = Classifier()

    def classify(self) -> tuple[bool, tuple[float, float]]:
        self.processed = preprocess(self.unprocessed)
        rating, probability = self.classifier.classify(self.processed)
        return rating, probability


class HumanRating(models.Model):
    rating = models.BooleanField()
    raw_rating = models.FloatField()
    text = models.OneToOneField(Text, on_delete=models.CASCADE)


class HumanRatingClass(models.Model):
    severe_toxicity = models.FloatField()
    obscene = models.FloatField()
    threat = models.FloatField()
    insult = models.FloatField()
    identity_attack = models.FloatField()
    sexual_explicit = models.FloatField()
    human_rating = models.OneToOneField(HumanRating, on_delete=models.CASCADE)


class MachineRating(models.Model):
    rating = models.BooleanField()
    text = models.OneToOneField(Text, on_delete=models.CASCADE)
