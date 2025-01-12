from rest_framework import serializers
from .models import Event, Review


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'email', 'rating', 'comment', 'event']
        
    def create(self, validated_data):
        return Review.objects.create(**validated_data)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'email', 'rating', 'comment',
        'created_at']

class EventSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'location',
        'reviews']
        
