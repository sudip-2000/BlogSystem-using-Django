from django.contrib.auth.models import User


def authors_list(request):
    authors = User.objects.filter(profile__isnull=False)
    return {'authors': authors}