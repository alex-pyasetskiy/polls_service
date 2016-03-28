from django.test import TestCase
from flexmock import flexmock
from factory import Sequence
from factory.django import DjangoModelFactory
from datetime import datetime, timedelta
from rest_framework import status
from rest_api.serializers import QuestionSerializer
from rest_api.models import Question, Choice
from rest_assured.testcases import BaseRESTAPITestCase, ReadRESTAPITestCaseMixin, CreateAPITestCaseMixin
from rest_framework.test import APIClient


class QuestionFactory(DjangoModelFactory):
    class Meta:
        model = Question

    question = Sequence(lambda n: "Question %03d" % n)
    pub_date = Sequence(lambda n: datetime.utcnow() + timedelta(minutes=n))


class SmokeTest(TestCase):
    def test_bad_maths(self):
        self.assertEqual(1 + 1, 2)


class TestSerializers(TestCase):
    def setUp(self):
        self.serializer_class = QuestionSerializer
        self.question_model = flexmock(Question)
        self.choice_model = flexmock(Choice)
        super(TestSerializers, self).setUp()

    def test_minimal_question_serialization(self):
        q_s = self.serializer_class(data={"question": "fake"})
        q_s.is_valid(raise_exception=True)
        self.assertEqual(q_s.is_valid(), True)

    def test_full_question_serialization(self):
        q_s = self.serializer_class(
            data={"question": "fake", "choices": [{"choice": "one"}, {"choice": "zero", "votes": 10}]})
        q_s.is_valid(raise_exception=True)
        self.assertEqual(q_s.is_valid(), True)

    def test_question_creation_serializer(self):
        q_s = self.serializer_class(
            data={"question": "fake", "choices": [{"choice": "one"}, {"choice": "zero", "votes": 10}]})
        q_s.is_valid()
        res = q_s.create(q_s.validated_data)
        self.assertIsInstance(res, Question)


class QuestionAPITest(BaseRESTAPITestCase, ReadRESTAPITestCaseMixin):
    base_name = 'question'
    factory_class = QuestionFactory


class QuestionVoteAPITest(BaseRESTAPITestCase, CreateAPITestCaseMixin):
    base_name = 'question'
    factory_class = QuestionFactory
    create_data = {"question": "fake", "choices": [{"choice": "one"}, {"choice": "zero"}]}

    def setUp(self, *args, **kwargs):
        super(QuestionVoteAPITest, self).setUp()
        self.q = self.factory_class.create()
        self.client = APIClient()

    def test_voting(self):
        response = self.client.put('/api/questions/1/vote/?choice=1', {'title': 'new idea'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)