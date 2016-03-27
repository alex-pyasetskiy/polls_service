from .models import Question, Choice
from rest_framework import serializers


class ChoiceSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    choice = serializers.CharField()
    votes = serializers.IntegerField(read_only=True)
    question_id = serializers.PrimaryKeyRelatedField(read_only=True)


class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    question = serializers.CharField()
    pub_date = serializers.DateTimeField(read_only=True)
    choices = serializers.ListSerializer(child=ChoiceSerializer(), required=False)

    def create(self, validated_data):
        question = Question()
        question.question = validated_data['question']
        question.save()
        for item in validated_data.get('choices', []):
            c = Choice()
            c.choice = item['choice']
            c.votes = item.get('votes', 0)
            c.question = question
            c.save()
        return question

    def update(self, instance, validated_data):
        if validated_data['question']:
            instance.question = validated_data['question']

        if validated_data.get('choices', None) is not None:
            instance.choices.all().delete()

            for item in validated_data.get('choices', []):
                c = Choice()
                c.choice = item['choice']
                c.votes = item.get('votes', 0)
                c.question = instance
                c.save()

        return instance




