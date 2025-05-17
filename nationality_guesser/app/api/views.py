from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from django.db import models
from ..utils.api_client import fetch_nationality, fetch_country_details
from .models import Country, NameNationality
from .serializers import NameNationalitySerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class NameNationalityView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "name",
                openapi.IN_QUERY,
                description="Name to analyze",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        responses={
            200: NameNationalitySerializer(many=True),
            400: "Bad Request - Name parameter is required",
            404: "Not Found - No nationality data available",
        },
    )
    def get(self, request):
        name = request.query_params.get("name", "").strip()

        if not name:
            return Response(
                {"error": "Name parameter is required and cannot be empty"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Проверяем кэш (данные не старше 1 дня)
            one_day_ago = timezone.now() - timedelta(days=1)
            cached_results = NameNationality.objects.filter(
                name__iexact=name, last_accessed__gte=one_day_ago
            ).select_related("country")

            if cached_results.exists():
                serializer = NameNationalitySerializer(cached_results, many=True)
                return Response(serializer.data)

            # Запрашиваем из внешнего API
            api_response = fetch_nationality(name)

            if not api_response or not api_response.get("country"):
                return Response(
                    {"error": "Cannot determine nationality for this name"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            results = []
            for country_data in api_response["country"]:
                country_code = country_data["country_id"].upper()
                probability = country_data["probability"]

                # Получаем или создаем страну
                country, _ = Country.objects.get_or_create(
                    country_code=country_code,
                    defaults={
                        "name": f"Country {country_code}",
                        "full_name": f"Country {country_code}",
                        "region": "Unknown",
                    },
                )

                # Обновляем или создаем запись (исправленная версия)
                name_nat, created = NameNationality.objects.get_or_create(
                    name=name.lower(),
                    country=country,
                    defaults={
                        "probability": probability,
                        "count": 1,  # Начальное значение для новой записи
                    },
                )

                if not created:
                    # Только для существующих записей используем F()
                    name_nat.count = models.F("count") + 1
                    name_nat.save()

                results.append(name_nat)

            serializer = NameNationalitySerializer(results, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response(
                {"error": f"Server error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PopularNamesView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "country",
                openapi.IN_QUERY,
                description="Country code (e.g. US, UK)",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="List of popular names",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "name": openapi.Schema(type=openapi.TYPE_STRING),
                            "total_count": openapi.Schema(type=openapi.TYPE_INTEGER),
                        },
                    ),
                ),
            ),
            400: "Bad Request - Country parameter is required",
            404: "Not Found - No data for this country",
        },
    )
    def get(self, request):
        country_code = request.query_params.get("country")

        if not country_code:
            return Response(
                {"error": "Paramets 'country' is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Проверяем, существует ли такая страна
        if not Country.objects.filter(country_code=country_code.upper()).exists():
            return Response(
                {"error": "No country with this code"},
                status=status.HTTP_404_NOT_FOUND,
            )

        popular_names = (
            NameNationality.objects.filter(country__country_code=country_code.upper())
            .values("name")
            .annotate(total_count=models.Sum("count"))
            .order_by("-total_count")[:5]
        )

        if not popular_names:
            return Response(
                {"error": "No data for this country"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(popular_names)


def all_names_view(request):
    # Получаем все записи из базы с связанной страной
    names = NameNationality.objects.select_related("country").all()

    # Формируем данные для таблицы
    table_data = []
    for name in names:
        table_data.append(
            {
                "name": name.name,
                "count": name.count,
                "last_accessed": name.last_accessed,
                "country": name.country.name,
                "country_code": name.country.country_code,
                "probability": name.probability,
                "capital": name.country.capital,
                "flag": name.country.flag_png,
            }
        )

    return render(request, "api/all_names.html", {"names": table_data})


@login_required
def home_view(request):
    return render(request, "home/home.html", {"user": request.user})
