from src.handlers import commands, states, unreg, callbacks


routers = [commands.router, states.router, unreg.router, callbacks.router]
