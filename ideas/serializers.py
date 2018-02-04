from rest_framework import serializers
from .models import Ideas

class IdeasSerializer(serializers.ModelSerializer):
    '''
    Serializer for Ideas based on the Model
    '''

    # The test expects the DateTime field to be UNIX Format
    created_at = serializers.DateTimeField(format="%s", read_only=True)

    class Meta:
        model = Ideas
        fields = (
            'id', 'content', 'impact', 'ease', 'confidence', 'average_score', 'created_at'
        )
