from rest_framework import serializers


class UnreadCountSerializer(serializers.Serializer):
    counts = serializers.DictField(child=serializers.IntegerField(), read_only=True)
    total = serializers.IntegerField(read_only=True)
