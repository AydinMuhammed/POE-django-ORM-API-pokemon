from django.shortcuts import redirect, render
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import login, logout
from pokemon.forms import LoginForm
# Create your views here.

# @user_passes_test(lambda u: u.has_perm("pokemon.view_pokemon"))
# @login_required
def view_home(request):
    """Render the home page."""
    user = request.user
    can_view_pokemon = user.has_perm("pokemon.view_pokemon")
    
    print(f"User: {user}, Can view pokemon: {can_view_pokemon}")
    return render(request, 'pokemon/page-home.html', context={})



def view_login(request):
    form = LoginForm(data=request.POST or None)
    if form.is_valid():
        # If the form is valid, it will have a user attribute to login as
        login(request, form.user)
        return redirect("home")
    return render(request, "pokemon/page-login.html", context={"form": form})


def view_logout(request):
    logout(request)
    return redirect("home")
