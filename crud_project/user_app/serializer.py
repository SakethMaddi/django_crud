from rest_framework import serializers
from .models import usertable


class userserializer(serializers.ModelSerializer):
    class Meta:
        model=usertable
        fields='__all__'