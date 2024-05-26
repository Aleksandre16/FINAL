from rest_framework import serializers
from users.models import Reservation


class BookReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '_all'
