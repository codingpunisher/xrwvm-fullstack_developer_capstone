from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .populate import initiate
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review
import json
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.


@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        return JsonResponse(
            {
                "userName": username,
                "status": "Authenticated"
            }
        )
    return JsonResponse(
        {
            "userName": username,
            "status": "Authentication Failed"
        }
    )


def logout_request(request):
    logout(request)
    return JsonResponse({"userName": ""})


@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']

    if User.objects.filter(username=username).exists():
        return JsonResponse(
            {
                "userName": username,
                "error": "Already Registered"
            }
        )

    user = User.objects.create_user(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        password=password
    )

    login(request, user)
    return JsonResponse({"userName": username, "status": "Authenticated"})


def get_cars(request):
    if not CarMake.objects.exists():
        initiate()

    cars = [
        {"CarModel": car_model.name, "CarMake": car_model.car_make.name}
        for car_model in CarModel.objects.select_related('car_make')
    ]
    return JsonResponse({"CarModels": cars})


def get_dealerships(request, state="All"):
    endpoint = "/fetchDealers" if state == "All" else "/fetchDealers/" + state
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint)
        for review in reviews:
            review['sentiment'] = analyze_review_sentiments(
                review['review']
            )['sentiment']
        return JsonResponse({"status": 200, "reviews": reviews})
    return JsonResponse({"status": 400, "message": "Bad Request"})


def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchDealer/" + str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    return JsonResponse({"status": 400, "message": "Bad Request"})


def add_review(request):
    if not request.user.is_anonymous:
        data = json.loads(request.body)
        try:
            post_review(data)
            return JsonResponse({"status": 200})
        except Exception as e:
            logger.error("Error posting review: %s", str(e))
            return JsonResponse(
                {
                    "status": 401,
                    "message": "Error in posting review"
                }
            )
    return JsonResponse({"status": 403, "message": "Unauthorized"})
