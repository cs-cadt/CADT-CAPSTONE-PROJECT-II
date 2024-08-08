
import os
import json, requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib import messages
import logging
from secretkey.models import SecretKey
from .forms import SecretKeyForm, SecretKeyUpdateForm, TrainModelForm
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, Http404
from django.utils.encoding import smart_str

logger = logging.getLogger(__name__)

def admin_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            logger.debug(f'Attempting to authenticate user: {username}')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                logger.info(f'User {username} authenticated successfully.')
                login(request, user)
                logger.info(f'User {username} logged in and redirected to dashboard.')
                return redirect('dashboard')
            else:
                logger.warning(f'Failed login attempt for user: {username}')
                messages.error(request, 'Invalid email or password.')
        else:
            logger.warning(f'Form validation failed for user: {request.POST.get("username")}')
            messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()

    return render(request, 'admin/login.html', {'form': form})

def forgot_password_view(request):
    return render(request, 'admin/forgot-password.html')

def verify_code_view(request):
    return render(request, 'admin/verify-code.html')

def reset_password_view(request):
    return render(request, 'admin/reset-password.html')

# @login_required
def admin_dashboard(request):
    try:
        # Make a request to the UnAnsweredAPI
        response = requests.get('http://127.0.0.1:8000/api/monitoring/unanswered/')
        response.raise_for_status()
        data = response.json()
        unanswered_questions = data.get('unanswered', [])
    except requests.exceptions.RequestException as e:
        # Handle exceptions (e.g., API down, network issues)
        unanswered_questions = []
        print(f"Error fetching unanswered questions: {e}")

    return render(request, 'admin/dashboard.html', {'questions': unanswered_questions})

#secret key management view
def manage_secret_keys_view(request):
    secret_keys = SecretKey.objects.all()
    return render(request, 'pages/secret-key.html', {'secret_keys': secret_keys})

def generate_key(request):
    if request.method == 'POST':
        form = SecretKeyForm(request.POST)
        if form.is_valid():
            #extract the key name
            name = form.cleaned_data.get('name')
            #check if the key exists with the same name
            if SecretKey.objects(name=name).exists():
                messages.error(request, 'Key with this name already exists.')
                return render(request, 'pages/generate.html', {'form': form})
            
            #save the secret key
            form.save()
            messages.success(request, 'Secret key generated successfully.')
            return redirect('manage_secret_key')
    else:
        form = SecretKeyForm()
    return render(request, 'pages/generate.html', {'form': form})

@csrf_exempt
def edit_secret_key(request, key_id):
    secret_key = get_object_or_404(SecretKey, id=key_id)
    
    if request.method == 'POST':
        form = SecretKeyUpdateForm(request.POST, instance=secret_key)
        if form.is_valid():
            new_name = form.cleaned_data.get('name')
            
            if SecretKey.objects.exclude(id=key_id).filter(name=new_name).exists():
                return JsonResponse({'meta': {'status': 400, 'message': 'A key with this name already exists.'}}, status=400)
            
            form.save()
            return JsonResponse({'meta': {'status': 200, 'message': 'Secret key updated successfully.'}}, status=200)
        else:
            errors = form.errors.as_json()
            print(f"Form errors: {errors}")  # Log form errors
            return JsonResponse({'meta': {'status': 400, 'message': 'Form is not valid.', 'errors': errors}}, status=400)
    else:
        form = SecretKeyUpdateForm(instance=secret_key)
    
    return render(request, 'pages/edit_key.html', {'form': form, 'secret_key': secret_key})

@csrf_exempt  # Temporarily disable CSRF protection for DELETE requests (be cautious with this)
@require_http_methods(["DELETE"])
def delete_secret_key(request, id):
    try:
        key = SecretKey.objects.get(id=id)
        key.delete()
        return JsonResponse({
            'meta': {
                'status': 200,
                'message': "Secret key has been deleted successfully"
            }
        })
    except SecretKey.DoesNotExist:
        return JsonResponse({
            'meta': {
                'status': 400,
                'message': "Secret key does not exist"
            }
        })
    except Exception as e:
        return HttpResponseBadRequest(f"Error: {str(e)}")

#model management view
def models_view(request):
    models = []
    models_dir = os.path.join('ds/models')  # Ensure this is the absolute path
    
    if os.path.exists(models_dir):
        for file_name in os.listdir(models_dir):
            file_path = os.path.join(models_dir, file_name)
            if os.path.isfile(file_path):
                models.append({
                    'name': file_name
                })

    return render(request, 'pages/models.html', {'models': models})

@csrf_exempt
def model_upload(request):
    if request.method == 'POST':
        model_file = request.FILES.get('file')
        setting_file = request.FILES.get('setting_file')
        
        if not model_file or not setting_file:
            return JsonResponse({'status': 400, 'message': 'Both model file and setting file are required'}, status=400)
        
        model_file_path = os.path.join(settings.BASE_DIR, 'ds', 'models', model_file.name)
        setting_file_path = os.path.join(settings.BASE_DIR, 'ds', 'setting', setting_file.name)
        
        # Ensure the directories exist
        os.makedirs(os.path.dirname(model_file_path), exist_ok=True)
        os.makedirs(os.path.dirname(setting_file_path), exist_ok=True)
        
        # Save the files
        try:
            with open(model_file_path, 'wb') as f:
                for chunk in model_file.chunks():
                    f.write(chunk)
            
            with open(setting_file_path, 'wb') as f:
                for chunk in setting_file.chunks():
                    f.write(chunk)
            
            return JsonResponse({'status': 200, 'message': 'Files uploaded successfully'})
        except Exception as e:
            return JsonResponse({'status': 500, 'message': f'File upload failed: {str(e)}'}, status=500)
    
    return render(request, 'pages/model_upload.html')

@csrf_exempt
def edit_model_view(request, file_name):
    model_file_path = os.path.join(settings.BASE_DIR, 'ds', 'models', file_name)
    settings_file_path = os.path.join(settings.BASE_DIR, 'ds', 'setting', file_name)

    if not os.path.exists(model_file_path):
        return HttpResponseNotFound("Model file does not exist")

    if request.method == 'POST':
        new_name = request.POST.get('name')
        if new_name:
            new_model_file_path = os.path.join(settings.BASE_DIR, 'ds', 'models', f"{new_name}.pkl")
            new_settings_file_path = os.path.join(settings.BASE_DIR, 'ds', 'setting', f"{new_name}.pkl")
            
            # Rename the model file
            os.rename(model_file_path, new_model_file_path)
            
            # Rename the settings file if it exists
            if os.path.exists(settings_file_path):
                os.rename(settings_file_path, new_settings_file_path)
            
            return redirect('manage_models')  # Redirect to model list after success

    return render(request, 'pages/edit_model.html', {'file_name': file_name})

@csrf_exempt
def delete_model_view(request, file_name):
    file_path = f"ds/models/{file_name}"
    setting_path = f"ds/setting/{file_name}"

    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            if os.path.exists(setting_path):
                os.remove(setting_path)
            return JsonResponse({'message': 'Model and setting have been deleted.'}, status=200)
        else:
            return JsonResponse({'error': 'Model file not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_available_datasets():
    datasets_dir = os.path.join(settings.BASE_DIR, 'data_storage')
    choices = []
    if os.path.exists(datasets_dir):
        for file_name in os.listdir(datasets_dir):
            file_path = os.path.join(datasets_dir, file_name)
            if os.path.isfile(file_path):
                choices.append((file_name, file_name))  # Value and display should match
    return choices

@csrf_exempt
def train_model_view(request):
    if request.method == 'POST':
        print("POST Data:", request.POST)  # Debugging line

        dataset_choices = get_available_datasets()
        form = TrainModelForm(request.POST, dataset_choices=dataset_choices)
        
        if form.is_valid():
            file_name = form.cleaned_data['file_name']
            model_name = form.cleaned_data['model_name']
            data = {'modelname': model_name, 'filename': file_name}
            
            try:
                response = requests.post(
                    'http://127.0.0.1:8000/api/model/training',
                    data=json.dumps(data),
                    headers={'Content-Type': 'application/json'}
                )
                response.raise_for_status()
                
                response_data = response.json()
                print("API Response Data:", response_data)  # Debug line
                
                if response.status_code == 200:
                    return JsonResponse({'message': 'Model has been trained successfully.'}, status=200)
                else:
                    error_message = response_data.get('message', 'Failed to train model')
                    return JsonResponse({'error': error_message}, status=response.status_code)
            except requests.exceptions.HTTPError as http_err:
                return JsonResponse({'error': f'HTTP error occurred: {http_err}'}, status=500)
            except Exception as err:
                return JsonResponse({'error': f'An error occurred: {err}'}, status=500)
        else:
            print("Form Errors:", form.errors)  # Debugging line
            return JsonResponse({'error': 'Form validation failed.', 'form_errors': form.errors}, status=400)
    else:
        dataset_choices = get_available_datasets()
        form = TrainModelForm(dataset_choices=dataset_choices)
        return render(request, 'pages/train_model.html', {'form': form})
    
from django.views.generic import TemplateView
class ChangeModelView(TemplateView):
    template_name = 'pages/change_model.html'


#dataset management view
@csrf_exempt
def upload_file_view(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        file_name = request.POST.get('name')
        
        if not uploaded_file or not file_name:
            return JsonResponse({'error': 'File or name is missing'}, status=400)
        
        # Ensure the file name is unique
        unique_file_name = f"{file_name}.csv"
        file_path = os.path.join(settings.BASE_DIR, 'data_storage', unique_file_name)

        # Check if the file already exists
        if os.path.exists(file_path):
            return JsonResponse({'error': 'File with this name already exists'}, status=400)

        # Create the directory if it does not exist
        if not os.path.exists('data_storage'):
            os.makedirs('data_storage')

        # Save the file
        try:
            with open(file_path, 'wb') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)
            return redirect('manage_dataset')  # Redirect to the file list page
        except Exception as e:
            return JsonResponse({'error': f'File upload failed: {str(e)}'}, status=500)
    return render(request, 'pages/upload_data.html')

def dataset_view(request):
    files = []
    datasets_dir = os.path.join(settings.BASE_DIR, 'data_storage')  # Ensure this is the absolute path
    
    if os.path.exists(datasets_dir):
        for file_name in os.listdir(datasets_dir):
            file_path = os.path.join(datasets_dir, file_name)
            if os.path.isfile(file_path):
                files.append({
                    'name': file_name,
                    'path': os.path.join('data_storage', file_name),  # Relative path for use in the template
                    'uploaded_at': os.path.getmtime(file_path)  # Unix timestamp; can format as needed
                })

    return render(request, 'pages/dataset.html', {'files': files})

@csrf_exempt
def delete_file_view(request, file_name):
    if request.method == 'DELETE':
        try:
            # Construct the absolute file path
            file_path = os.path.join(settings.BASE_DIR, 'data_storage', file_name)
            
            logger.info(f'Received delete request for filename: {file_name}')
            logger.info(f'File path: {file_path}')
            
            if os.path.exists(file_path):
                os.remove(file_path)
                return JsonResponse({'message': 'File deleted successfully'})
            else:
                return JsonResponse({'error': 'File not found'}, status=404)
        except Exception as e:
            logger.error(f"Error processing delete request: {e}")
            return JsonResponse({'error': 'Internal server error'}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def edit_file_view(request, file_name):
    if request.method == 'POST':
        new_name = request.POST.get('new_name')
        
        if not new_name:
            return JsonResponse({'status': 400, 'message': 'New name is missing'}, status=400)
        
        # Construct the file paths
        old_file_path = os.path.join(settings.BASE_DIR, 'data_storage', file_name)
        new_file_path = os.path.join(settings.BASE_DIR, 'data_storage', f"{new_name}.csv")
        
        # Check if the old file exists
        if not os.path.exists(old_file_path):
            return JsonResponse({'status': 404, 'message': 'File not found'}, status=404)
        
        # Check if the new file name already exists
        if os.path.exists(new_file_path):
            return JsonResponse({'status': 400, 'message': 'File with the new name already exists'}, status=400)
        
        # Rename file
        try:
            os.rename(old_file_path, new_file_path)
            return JsonResponse({'status': 200, 'message': 'File renamed successfully'})
        except Exception as e:
            return JsonResponse({'status': 500, 'message': f'File rename failed: {str(e)}'}, status=500)
    
    # If the request method is not POST, show the edit form
    return render(request, 'pages/edit_dataset.html', {'file_name': file_name})

