from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.utils import IntegrityError
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse, HttpResponseRedirect
from dotenv import load_dotenv
from json import loads
from supabase import create_client, Client
from re import match
from supabase.lib.client_options import ClientOptions
from os import getenv
from logging import getLogger, basicConfig, DEBUG
from .utils.db_get_data import email_exists



load_dotenv()
SUPABASE_KEY = getenv('SUPABASE_KEY')
SUPABASE_URL = getenv('SUPABASE_URL')


supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY,
    options=ClientOptions(
        auto_refresh_token=False,
        persist_session=False,
    ),
)

# Optional: Configure logging
logger = getLogger(__name__)
basicConfig(level=DEBUG)
link = f"{SUPABASE_URL}/auth/v1/authorize?provider="


@csrf_exempt
def signup_view(request):
    """sign up user using email method """
    if request.method == "POST":
        try:
            data = loads(request.body)
            print("Received data:", data)

            username = data.get('name')
            email = data.get('email')
            password = data.get('password')
            confirm_password = data.get('confirmPassword')
            language = data.get('language')
            country = data.get('country')
            mobile_phone = data.get('mobilePhone')
            address1 = data.get('address1')
            address2 = data.get('address2')
            terms_agreed = data.get('termsAgreed')

            # Validate inputs
            email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
            if not match(email_regex, email):
                return JsonResponse({"error": "Invalid email format"}, status=400)

            if not terms_agreed:
                return JsonResponse({"error": "Terms must be agreed upon to sign up"}, status=400)

            if password != confirm_password:
                return JsonResponse({"error": "Passwords do not match"}, status=400)

            user_metadata = {
                "first_name": username,
                "language": language,
                "country": country,
                "mobile_phone": mobile_phone,
                "address1": address1,
                "address2": address2
            }

            # Call Supabase sign_up method
            try:
                response = supabase.auth.sign_up(
                    {
                        "email": email,
                        "password": password,
                        "options": {"data": user_metadata},
                    }
                )

                # Access the session and access_token directly from the response object
                if hasattr(response, "session") and response.session:
                    access_token = getattr(
                        response.session, "access_token", None)
                    if access_token:
                        return JsonResponse({
                            "message": "User created successfully",
                            "access_token": access_token
                        }, status=201)
                    else:
                        return JsonResponse({"error": "Sign-up failed: no access token found in the session"}, status=500)
                else:
                    return JsonResponse({"error": "Sign-up failed: no session returned"}, status=500)

            except Exception as e:
                logger.error(f"Error during sign-up: {str(e)}")
                return JsonResponse({"error": str(e)}, status=500)

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

    return JsonResponse({"error": "Only POST requests are allowed"}, status=405)


@csrf_exempt
def signin_view(request):
    """sign in user using email method """
    if request.method == "POST":
        try:
            data = loads(request.body)
            email = data.get('email')
            password = data.get('password')

            response = supabase.auth.sign_in_with_password(
                {
                    "email": email,
                    "password": password,
                }
            )
            if hasattr(response, "session") and response.session:
                access_token = getattr(
                    response.session, "access_token", None)
                if access_token:
                    return JsonResponse({
                        "message": "Login successful",
                        "access_token": access_token
                    }, status=200)
            else:
                return JsonResponse({"error": "Invalid username or password"},
                                    status=401)

        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"},
                                status=500)
    return JsonResponse({"error": "Only POST requests are allowed"}, status=405)




@csrf_exempt
def check_email(request):
    """check if user already in db """
    if request.method == "POST":
        try:
            data = request.POST if request.POST else loads(request.body)
            email = data.get("email", "").strip()

            # Validate the email format using regex
            email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
            if not match(email_regex, email):
                return JsonResponse({"error": "Invalid email format"},
                                    status=400)

            exists = email_exists(email)
            return JsonResponse({"exists": exists})
        except Exception as e:
            print(f"Error processing request: {e}")
            return JsonResponse({"error": "Something went wrong"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def retrieve_session(request):
    """ retrive user session to keep user on session call whean session about to expire """
    if request.method == 'GET':
        try:
            return supabase.auth.get_session()
        except Exception as e:
            return JsonResponse({'error': 'something went wrong '}, status=500)
    return JsonResponse({"error": "Only POST requests are allowed"},
                        status=405)



@csrf_exempt
def google_oauth(request):
    """sign in  using oauth by calling supabase link"""
    if request.method == 'GET':
        redirect_url = link + 'google'
        return HttpResponseRedirect(redirect_url)
    else:
        return JsonResponse({"error": "Only GET requests are allowed"},
                            status=405)

@csrf_exempt
def bing_oauth(request):
    """sign in  using oauth by calling supabase link"""
    if request.method == 'GET':
        redirect_url = link + 'google'
        return HttpResponseRedirect(redirect_url)
    else:
        return JsonResponse({"error": "Only GET requests are allowed"},
                            status=405)

@csrf_exempt
def x_oauth(request):
    """sign in  using oauth by calling supabase link"""
    if request.method == 'GET':
        redirect_url = link + 'google'
        return HttpResponseRedirect(redirect_url)
    else:
        return JsonResponse({"error": "Only GET requests are allowed"},
                            status=405)
