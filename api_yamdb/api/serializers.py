from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Comment, Review, Title


class ReviewSerialaizer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    
    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, validated_data):
        if self.context['request'].method != 'POST':
            return validated_data
        pk = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=pk)
        current_review = Review.objects.filter(
            title=title,
            author=self.context['request'].user,
        )
        if current_review.exists():
            raise serializers.ValidationError(
                'Вы можете добавить только один отзыв к произведению!'
            )
        return validated_data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
