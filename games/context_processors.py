from games.models import Category


def categories(request):
    """
    Add list of categories to all requests. This is done because nav bar needs category information.
    """
    return {"categories": Category.objects.all()}