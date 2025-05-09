from rest_framework import serializers
from home.models import User , Person , Note
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ "id" , "name" , "email" , "mobile" , "password"]
    
class PersonSeriliazer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = "__all__"
        
    def validate(self , data):
        if(data['age'] < 18):
            raise serializers.ValidationError('age should be greater than 18')
        
        return data
    
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'