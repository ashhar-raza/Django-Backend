from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from home.models import User , Person , Note
from home.serializers import UserSerializer , PersonSeriliazer , NoteSerializer
from home.utils import hash_password, verify_password, generate_token  # Assuming you have those functions in utils.py

# Sample index view
@api_view(['GET', 'POST'])
def index(request):
    courses = {
        'course_name': 'Django',
        'learn': ['flask', 'Django', 'Tornado', 'FastApi'],
        'course_provide': 'Scaler'
    }
    if request.method == "GET":
        print("GET Triggered")
        return Response(courses)
    elif request.method == "POST":
        print("POST Triggered")
        data = request.data
        return Response({"input": data, "output": courses})
    else:
        return Response("No data triggered")


@api_view(['GET' , 'POST' , 'PUT' , 'PATCH' , 'DELETE'])
def person(request):
    if(request.method == 'GET'):
        objs = Person.objects.all()
        serializer = PersonSeriliazer(objs , many=True)
        return Response(serializer.data)
    elif(request.method == 'POST'):
        data = request.data
        serializer = PersonSeriliazer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif(request.method == 'PUT'):
       data = request.data
       obj = Person.objects.get(id = data['id'])
       ser = PersonSeriliazer( obj , data = data , partial = True)
       if(ser.is_valid()):
            ser.save()
            return Response(ser.data)
       return Response(ser.errors)
    elif(request.method == 'PATCH'):
        data = request.data
        obj = Person.objects.get(id = data['id'])
        ser = PersonSeriliazer(obj, data = data , partial = True)
        if(ser.is_valid()):
            ser.save()
            return Response(ser.data)
        return Response(res.errors)
    else :
        data = request.data
        obj = Person.objects.get(id = data['id'])
        obj.delete()
        return Response({'message' : 'Person deleted'})

# USER CRUD
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def user_api(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = request.data.copy()
        if 'password' in data:
            data['password'] = hash_password(data['password'])

        serializer = UserSerializer(data=data)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        user_id = request.data.get('id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        if 'password' in data:
            data['password'] = hash_password(data['password'])

        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user_id = request.data.get('id')
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


# Login API for generating JWT Token
@api_view(['POST'])
def login_api(request):
    email = request.data.get('email')
    password = request.data.get('password')

    # Check if email and password are provided
    if not email or not password:
        return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Fetch user by email
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)

    # Verify if the entered password matches the hashed password in the database
    if verify_password(password, user.password):
        # Generate the JWT token
        token = generate_token(user.id)
        return Response({"token": token}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def notes_api(request):
    user = getattr(request, 'user', None)
    if user is None:
        return Response({'error': 'Authentication required'}, status=401)

    # GET all notes for the user
    if request.method == 'GET':
        notes = Note.objects.filter(user=user)
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    # POST - Create new note
    elif request.method == 'POST':
        data = request.data.copy()
        data['user'] = user.id  # Set the user
        serializer = NoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    # PUT - Update an existing note
    elif request.method == 'PUT':
        note_id = request.data.get('id')
        try:
            note = Note.objects.get(id=note_id, user=user)
        except Note.DoesNotExist:
            return Response({'error': 'Note not found'}, status=404)

        data = request.data.copy()
        serializer = NoteSerializer(note, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    # DELETE - Delete a note
    elif request.method == 'DELETE':
        note_id = request.data.get('id')
        try:
            note = Note.objects.get(id=note_id, user=user)
            note.delete()
            return Response({'message': 'Note deleted successfully'})
        except Note.DoesNotExist:
            return Response({'error': 'Note not found'}, status=404)

    user = getattr(request, 'user', None)
    if user is None:
        return Response({'error': 'Authentication required'}, status=401)

    if request.method == 'GET':
        notes = Note.objects.filter(user=user)
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data.copy()
        data['user'] = user.id 
        serializer = NoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
        
    