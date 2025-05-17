from rest_framework import serializers
from .models import Country, NameNationality


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class NameNationalitySerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = NameNationality
        fields = "__all__"
