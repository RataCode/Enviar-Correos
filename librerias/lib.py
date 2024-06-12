from datetime import date, datetime,timedelta
import numpy as np
import pandas as pd
import pymongo
from librerias.Utilities import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .formatText import dataText
from dateutil.relativedelta import relativedelta

client = connect_db('bases')
client_local = connect_db('')

client = client_local

user_collection = client.gdc.users
calendar_collection = client.gdc.Calendar

users_names= list(pd.DataFrame(list(user_collection.aggregate([{ "$match": {"notification": { "$exists": True}}},{ "$project": {"user_name": 1, "_id": 0}}]))).user_name)


# ------------------------------------------------------------EMAIL---------------------------------------------------------------
sender = 'correo@gmail.com'
password = 'pass'
server = 'smtp.correo.com'
port = 465