import json

from django.http import Http404, HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from issues.models import Issue


class IssuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ["id", "title", "status", "junior", "senior"]


@api_view(["GET"])
def get_issues(request: HttpRequest) -> Response:
    issues = Issue.objects.all()
    serializer = IssuesSerializer(issues, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def retrieve_issues(request: HttpRequest, issue_id: int) -> Response:
    try:
        issue = Issue.objects.get(id=issue_id)
    except Issue.DoesNotExist:
        raise Http404
    serializer = IssuesSerializer(issue)
    return Response(serializer.data)


@api_view(["POST"])
@csrf_exempt
def post_issues(request: HttpRequest) -> JsonResponse:
    try:
        payload = json.loads(request.body)
    except json.decoder.JSONDecodeError:
        return JsonResponse({"error": "Request Body is invalid"}, status=400)

    serializer = IssuesSerializer(data=payload)
    if serializer.is_valid():
        issue = serializer.save()
        return JsonResponse(data=IssuesSerializer(issue).data, status=201)
    else:
        return JsonResponse(serializer.errors, status=400)
