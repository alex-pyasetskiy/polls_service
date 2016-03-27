from polls_server import celery_app
from rest_api.serializers import QuestionSerializer
from rest_api.models import Question, Choice


@celery_app.task
def test_task(data):
    return data


@celery_app.task
def vote_task(question_id, choice_id):
    instance = Question.objects.get(pk=int(question_id))
    choice = Choice.objects.get(pk=int(choice_id))
    choice.votes += 1
    choice.save()
    res = QuestionSerializer().to_representation(instance)
    return res
