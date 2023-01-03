import os

API_KEY = (
    "5459857666:AAFdO_W-y4MFW2a7JSRkNG3ufVmCJnhGupM"
    if not os.getenv("TELEGRAM_API_KEY")
    else os.getenv("TELEGRAM_API_KEY")
)

BOTNAME = "@gcetsupportbot"
ENV = "DEV"
MADEBY = "Amit Akash"
