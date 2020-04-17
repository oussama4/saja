from django.http import JsonResponse

from home.templatetags.menu_tags import catalog_menu

def menu(request):
    m = catalog_menu()
    return JsonResponse(m, safe=False)

