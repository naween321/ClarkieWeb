from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import detect_intent_cx
from core.models import QuestionAnswer
import json


@csrf_exempt
def get_answer(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON from request
            user_question = data.get("question", "")

            if not user_question:
                return JsonResponse({"error": "No question provided"}, status=400)

            # Call the function
            answer = detect_intent_cx(user_question)
            QuestionAnswer.objects.create(question=user_question, answer=answer)
            return JsonResponse({"question": user_question, "answer": answer})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Only POST requests allowed"}, status=405)
