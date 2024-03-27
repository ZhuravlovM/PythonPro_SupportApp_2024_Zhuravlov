import json

import httpx
from django.contrib import admin
from django.http import HttpRequest, JsonResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
async def currency(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            currency_from = data.get("from_currency")
            currency_to = data.get("to_currency")

            url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={currency_from}&to_currency={currency_to}&apikey=V2V43QAQ8RILGBOW"

            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                exchange_data = response.json()

                exchange_rate = exchange_data.get(
                    "Realtime Currency Exchange Rate", {}
                ).get("5. Exchange Rate")
                if exchange_rate:
                    return JsonResponse({"rate": float(exchange_rate)})
                else:
                    return JsonResponse(
                        {"error": "Exchange rate not found in response"},
                        status=500,
                    )

        except json.JSONDecodeError:

            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except httpx.RequestError:
            return JsonResponse(
                {"error": "Failed to fetch exchange rate"}, status=500
            )

    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("currency", view=currency),
]
