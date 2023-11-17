from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse

from .models import Choice
from .models import Question


def index(request):
    return render(request, "polls/index.html", get_context_last_n_published_questions())

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {"question": question}
    return render(request, "polls/question.html", context)


def results(request, question_id):
    results = Question.objects.get(pk=question_id).choice_set.order_by("-votes")
    last_vote_received = Question.objects.get(pk=question_id).choice_set.order_by("-last_vote")[0].last_vote
    context = {"results": results, "last_vote_received": last_vote_received}
    return render(request, "polls/results.html", context)


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/question.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.vote()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("myapp:results", args=(question.id,)))

def get_context_last_n_published_questions(n=5):
    """Return context for the last n published questions."""
    latest_question_list = Question.objects.order_by("-pub_date")[:n]
    return {"latest_question_list": latest_question_list,}