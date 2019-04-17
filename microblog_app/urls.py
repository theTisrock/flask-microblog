# Action Class - Static only. To hold names of actions that correspond to method calls.
#   This could be used for calling url_for(action)
#
#   Advantage: allows for changing action names in one place
#
#   Actions.[action]


class Action():
    edit_profile = 'edit_profile'
    explore = 'explore'
    index = 'index'
    login = 'login'
    logout = 'logout'
    register = 'register'
    user = 'user'

# URLRoute class - Static only. Holds route names.
# Advantage: better seperation of concerns. easy to rename routes
# URLRoute.[route]


class URLRoute():
    edit_profile = "/edit_profile"
    explore = "/explore"
    follow = "/follow/<username>"
    home = {'root': "/", 'index': "/index"}
    login = "/login"
    logout = "/logout"
    register = "/register"
    user = "/user/<username>"
    unfollow = "/unfollow/<username>"
    request_password_reset = "/request_password_reset"
    reset_password = "/reset_password/<token>"

# end urls
