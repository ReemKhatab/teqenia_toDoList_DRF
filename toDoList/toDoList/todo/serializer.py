from rest_framework import serializers
from .models import Task,Priority
from django.contrib.auth.models import User

class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all()
    )
    priority = serializers.PrimaryKeyRelatedField(queryset=Priority.objects.all())

    class Meta:
        model = Task
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['priority'] = PrioritySerializer(instance.priority).data
        representation['users'] = [
            {'id': user.id, 'username': user.username} for user in instance.users.all()
        ]
        return representation
    # priority = serializers.PrimaryKeyRelatedField(queryset=Priority.objects.all())
    # user = serializers.ReadOnlyField(source='user.username')
    # class Meta:
    #     model = Task
    #     fields = '__all__'

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['priority'] = PrioritySerializer(instance.priority).data
    #     return representation


    