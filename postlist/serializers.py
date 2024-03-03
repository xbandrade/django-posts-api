from rest_framework import serializers

from postlist.models import Post


class PostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    title = serializers.CharField(required=True)
    content = serializers.CharField(required=True)

    class Meta:
        model = Post
        fields = ['id', 'username', 'title', 'content', 'created_datetime']
        read_only_fields = ['updated_datetime']

    def update(self, instance, validated_data):
        validated_data.pop('username', None)
        return super().update(instance, validated_data)


class PostAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
