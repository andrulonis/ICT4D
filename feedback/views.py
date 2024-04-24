from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import get_language


from feedback.models import Feedback
import forecast

@csrf_exempt
def index(request):
    if request.method != 'POST':
        return redirect(f'/{get_language()}/forecast')

    feedback = Feedback(
        recording_file  = request.FILES['msg'],
        language = get_language()
    )

    feedback.save()

    return forecast.views.index(request)
