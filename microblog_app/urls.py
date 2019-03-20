# Action Class - Static only. To hold names of actions that correspond to method calls.
#   This could be used for calling url_for(action)
#
#   Advantage: allows for changing action names in one place
#
#   Actions.[action]


class Action():
    index = 'index'
    login = 'login'
    logout = 'logout'
    register = 'register'

# URLRoute class - Static only. Holds route names.
# Advantage: better seperation of concerns. easy to rename routes
# URLRoute.[route]


class URLRoute():
    home = {
                'root': "/",
                'index': "/index"
        }

    login = "/login"
    logout = "/logout"
    register = "/register"

# end urls
