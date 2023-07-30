from rest_framework import serializers

from reviews.models import Comment, Review


class ReviewSerialaizer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    
    class Meta:
        fields = ('__all__')
        model = Review
        read_only_fields = ('title', 'author', 'title_id')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('__all__')
        model = Comment
        read_only_fields = ('review', 'author', 'review_id')
