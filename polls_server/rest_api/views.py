from rest_framework import viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .serializers import QuestionSerializer
from .models import Question

import rest_api.tasks as bgtasks


class QuestionViewSet(viewsets.ViewSet):
    """
    API endpoint that allows questions to be viewed or edited.
    """

    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

    def list(self, request):
        """
        GET api/questions/

        [
  {
    "id": 1,
    "question": "FIRST TEST",
    "pub_date": "2016-03-27T03:45:04.799939Z",
    "choices": [
      {
        "id": 1,
        "choice": "Chose 1",
        "votes": 0,
        "question_id": 1
      },
      {
        "id": 2,
        "choice": "Chose 2",
        "votes": 0,
        "question_id": 1
      }
    ]
  },
  {
    "id": 7,
    "question": "SUPERNEW 2",
    "pub_date": "2016-03-27T05:57:33.885677Z",
    "choices": [
      {
        "id": 5,
        "choice": "one",
        "votes": 0,
        "question_id": 7
      },
      {
        "id": 6,
        "choice": "2 two",
        "votes": 0,
        "question_id": 7
      }
    ]
  }
]

        """
        serializer = self.serializer_class(data=self.queryset, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        GET api/questions/3

        """
        question = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(question)
        result = serializer.data
        return Response(result, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        POST api/questions/

        {
  "question": "SUPERNEW 2",
  "choices": [
    {
      "choice": "one"
    },
    {
      "choice": "2 two"
    }
  ]
}

        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            result = Response(serializer.data, status=status.HTTP_201_CREATED)
            return result

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, **kwargs):
        """
        PUT api/question/3/

        {"question":"SUPERNEW 3", "choices":[{"choice":"one"}]}

        {
            "id": 3,
            "question": "SUPERNEW 3",
            "pub_date": "2016-03-27T05:05:49.585966Z",
            "choices": [
                {
                "id": 7,
                "choice": "one",
                "votes": 0,
                "question_id": 3
                }
            ]
        }
        """
        question = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(question, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(question, serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        """
        DELETE api/question/3/
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @detail_route(methods=['put'])
    def vote(self, request, pk=None):
        """
        PUT api/questions/1/vote/?choice=3
        """
        question = get_object_or_404(self.queryset, pk=pk)
        choice_id = self.request.query_params.get('choice', None)
        bgtasks.vote_task.delay(question.id, choice_id)
        return Response()


