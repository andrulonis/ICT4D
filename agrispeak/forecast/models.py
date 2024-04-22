from django.db import models

class PastRainfall(models.Model):
    '''
        Once rainfall data is available, it will be stored in the PastRainfall model.
        Can be queried by the user to get past rainfall data.

        Fields:
        - date: Date of the rainfall
        - rainfall: Amount of rainfall in mm
    '''
    date = models.DateField()
    rainfall = models.FloatField()

class RainfallPrediction(models.Model):
    '''
        Rainfall prediction data will be stored in the RainfallPrediction model.
        Can be queried by the user to get predictions of rainfall.

        Fields:
        - date: Date of the prediction
        - rainfall: Amount of rainfall expected in mm
        - duration: How long the rainfall is expected to last
    '''
    date = models.DateField()
    rainfall = models.FloatField()
    duration = models.DurationField()

