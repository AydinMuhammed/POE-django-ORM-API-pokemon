from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout
from pokemon.forms import LoginForm



# @user_passes_test(lambda user: user.has_perm("pokemon.view_pokemon"))
def view_home(request):
    """Home page."""

    # Get the current user
    user = request.user
    # Get whether the user has permission to view the pokemon.pokemon model
    can_view_pokemon = user.has_perm("pokemon.view_pokemon")
    # Show the informations cleanly in the console
    print(f"User: {user}")
    print(f"Can view pokemon: {can_view_pokemon}")
    return render(request, "pokemon/page-home.html", context={})


@user_passes_test(lambda user: user.is_anonymous)
def view_login(request):
    form = LoginForm(data=request.POST or None)
    if form.is_valid():
        # If the form is valid, it will have a user attribute to login as
        login(request, form.user)
        return redirect("home")
    return render(request, "pokemon/page-login.html", context={"form": form})


@user_passes_test(lambda user: user.is_authenticated)
def view_logout(request):
    logout(request)
    return redirect("login")