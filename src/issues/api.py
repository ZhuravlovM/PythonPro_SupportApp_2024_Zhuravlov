import json
import random

from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from issues.models import Issues


def get_issues(request: HttpRequest) -> JsonResponse:
    issue_id = request.GET.get("id")
    if issue_id is None:
        return JsonResponse({"error": "No issue ID provided"}, status=400)

    try:
        issue = Issues.objects.get(id=issue_id)
        result = {
            "id": issue.id,
            "title": issue.title,
            "body": issue.body,
            "junior_id": issue.junior_id,
            "senior_id": issue.senior_id,
        }
        return JsonResponse(data=result)
    except Issues.DoesNotExist:
        return JsonResponse(
            {"error": f"Issue with ID {issue_id} does not exist"}, status=404
        )


@csrf_exempt
def post_issues(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        data = json.loads(request.body)
        title = data.get("title")
        body = data.get("body")

        if title is not None and body is not None:
            issue = Issues.objects.create(
                title=title,
                body=body,
                junior_id=random.randint(1, 5),
                senior_id=random.randint(1, 5),
            )

            result = {
                "id": issue.id,
                "title": issue.title,
                "body": issue.body,
                "junior_id": issue.junior_id,
                "senior_id": issue.senior_id,
            }

            return JsonResponse(data=result)
        else:
            return JsonResponse(
                {"error": "Missing 'title' or 'body' in JSON data"}, status=400
            )
    else:
        return JsonResponse(
            {"error": "Only POST requests are allowed"}, status=405
        )
