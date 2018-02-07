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

    def validate_impact(self, impact):
        # validate the impact and raise an exception
        if impact>10 or impact<1:
            raise serializers.ValidationError("Impact must be between than 1 and 10")
        return impact

    def validate_ease(self, ease):
        # validate the ease and raise an exception
        if ease>10 or ease<1:
            raise serializers.ValidationError("Ease must be between than 1 and 10")
        return ease

    def validate_confidence(self, confidence):
        # validate the confidence and raise an exception
        if confidence>10 or confidence<1:
            raise serializers.ValidationError("Confidence must be between than 1 and 10")
        return confidence