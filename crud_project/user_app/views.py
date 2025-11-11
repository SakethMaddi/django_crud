from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import usertable
from .serializer import userserializer
import json
import cloudinary
import cloudinary.uploader

# Create your views here.
@csrf_exempt
def reg_user(req):
    if req.method=="POST":
        try:
            id=req.POST.get("user_id")
            name=req.POST.get("user_name")
            email=req.POST.get("user_email")
            password=req.POST.get("user_password")
            image=req.FILES.get("user_image")
            
            img_url=cloudinary.uploader.upload(image)
            new_user=usertable.objects.create(user_id=id,user_name=name,user_email=email,user_password=password,user_image=img_url["secure_url"])
            return JsonResponse({"Msg":"user created successfully"})
        except Exception as e:
            return JsonResponse({"Error":str(e)})
    else:
        return JsonResponse({'error': 'Invalid Type'}, status=400)
    
    
def get_user(req,id):
    if req.method == "GET":
        try:
            single_user=usertable.objects.get(user_id=id)
            serializer=userserializer(single_user)
            return JsonResponse({"User":serializer.data})
        except usertable.DoesNotExist:
            return JsonResponse("user not found")
    else:
        return JsonResponse("invalid method")

def get_user(req):
    if req.method == "GET":
        user_data=usertable.objects.all()
        serializer=userserializer(user_data,many=True)
        return JsonResponse({"Users":serializer.data})
    else:
        return JsonResponse("invalid method")
    
@csrf_exempt
def update_user(req, id):

    if req.method in ["PUT", "PATCH"]:
        try:
            single_user = usertable.objects.get(user_id=id)
        except usertable.DoesNotExist:
            return HttpResponse("User not found")

        try:
            user_data = json.loads(req.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"})

        partial_update = True if req.method == "PATCH" else False

        serializer = userserializer(single_user, data=user_data, partial=partial_update)

        if serializer.is_valid():
            serializer.save()
            return HttpResponse("User updated successfully")
        return JsonResponse(serializer.errors)

    return HttpResponse("Only PUT and PATCH methods are allowed")


@csrf_exempt   
def delete_user(req,id):
    if req.method=="DELETE":
        
        try:
            user=usertable.objects.get(user_id=id)
        except usertable.DoesNotExist:
            return HttpResponse("user not found")
        user.delete()
        return HttpResponse("user deleted successfully")
    else:
        return HttpResponse("only delete method is allowed")