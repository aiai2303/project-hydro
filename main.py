from environ import session
from hydrogram import Client
import os, sys

app = Client("Google AI", session_string=session, plugins=dict(root='plugins'))

app.run()