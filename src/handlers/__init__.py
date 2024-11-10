from src.handlers import commands, states, unreg, callbacks, chats


routers = [commands.router, states.router, unreg.router, callbacks.router, chats.router]
