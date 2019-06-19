# Action Class - Static only. To hold names of actions that correspond to method calls.
#   This could be used for calling url_for(action)
#
#   Advantage: allows for changing action names in one place
#
#   Actions.[action]


class Action():
    # main sub system
    search = 'main.search'
    user = 'main.user'
    user_popup = 'main.user_popup'
    edit_profile = 'main.edit_profile'
    explore = 'main.explore'
    index = 'main.index'
    follow = 'main.follow'
    unfollow = 'main.unfollow'
    send_message = 'main.send_message'
    messages = 'main.messages'

    # auth sub system
    login = 'user_auth.login'
    logout = 'user_auth.logout'
    register = 'user_auth.register'
    request_password_reset = "user_auth.request_password_reset"


# URLRoute class - Static only. Holds route names.
# Advantage: better separation of concerns. easy to rename routes
# URLRoute.[route]


class URLRoute():
    edit_profile = "/edit_profile"
    explore = "/explore"
    follow = "/follow/<username>"
    home = {'root': "/", 'index': "/index"}
    login = "/login"
    logout = "/logout"
    messages = "/messages"
    register = "/register"
    user = "/user/<username>"
    popup = user + "/popup"
    unfollow = "/unfollow/<username>"
    request_password_reset = "/request_password_reset"
    reset_password = "/reset_password/<token>"
    send_message = "/send_message/<recipient>"

# end urls
