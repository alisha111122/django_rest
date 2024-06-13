from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from recipe.models import Recipe
from recipe.serializers import RecipeSerializer



@api_view(['GET','POST'])
def index(request):
    '''This is index route'''

    if request.method == "POST":
        print(request.data.get('name'))
        return Response(data={
            'message':"thanks for posting"
        })
   
    data = [
        {"id": 1, "name": "John", "age": 30},
        {"id": 2, "name": "Jane", "age": 25},
        {"id": 3, "name": "Bob", "age": 40},
    ]
    my_dict = {
        "message": "Hello, World!",
    }
    # return JsonResponse(data=data,safe=False)
    return Response(data=data)



@api_view(['GET','POST'])
def recipe(request):
    '''This is recipe list view'''
    recipes = Recipe.objects.all()
    serializer = RecipeSerializer(recipes,many=True)
    if request.method == "POST":
        serializer = RecipeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=201,data=serializer.data)
        # return Response(status=400,data=serializer.errors)
    return Response(data=serializer.data)


@api_view(['GET','PUT','DELETE'])
def recipe_detail(request,id):
    '''
    ### Recipe Detail
    This is recipe detail view  passing `id` will give the instance\n
        - OK THIS LOOKS GOOD
    ['/recipe/'](/recipe/)
    
    '''
    try:
        recipe = Recipe.objects.get(id=id)
    except Recipe.DoesNotExist:
        return Response(status=404,data={'message':"Recipe not found"})

    if request.method == "PUT":
        serializer = RecipeSerializer(instance=recipe,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    if request.method == "DELETE":
        recipe.delete()
        return Response(status=204,data=None)

    serializer = RecipeSerializer(recipe)
    return Response(data=serializer.data)



class RecipeView(APIView):
    def get(self,request):
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes,many=True)
        return Response(data=serializer.data)
    
    def post(self,request):
        serialzer = RecipeSerializer(data=request.data)
        serialzer.is_valid(raise_exception=True)
        serialzer.save()
        return Response(status=201,data=serialzer.data)
    

class RecipeDetailView(APIView):
    def get(self,request,id):
        try:
            recipe = Recipe.objects.get(id=id)
        except Recipe.DoesNotExist:
            return Response(status=404,data={'message':"Recipe not found"})
        serializer = RecipeSerializer(recipe)
        return Response(data=serializer.data)
    
    def put(self,request,id):
        try:
            recipe = Recipe.objects.get(id=id)
        except Recipe.DoesNotExist:
            return Response(status=404,data={'message':"Recipe not found"})
        serialzer = RecipeSerializer(instance = recipe, data=request.data)
        serialzer.is_valid(raise_exception=True)
        serialzer.save()
        return Response(status=200,data=serialzer.data)
    
    def delete(self,request,id):
        try:
            recipe = Recipe.objects.get(id=id)
        except Recipe.DoesNotExist:
            return Response(status=404,data={'message':"Recipe not found"})
        recipe.delete()
        return Response(status=204,data=None)
        