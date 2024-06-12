import pandas as pd
import os
import re
import base64
from pymongo import IndexModel, ASCENDING, DESCENDING
from datetime import datetime, timedelta
from pymongo import MongoClient
from openpyxl.utils import get_column_letter
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font
from functools import wraps
import time
import pickle
import io
from typing import Union

# ---- INTERNAL VARIABLES ----#
def connect_db(host:str = ''):

    mongo_username = "bases"
    mongo_password = "dedatos"
    if host.lower() == 'datos':
        ssh_address = "basesdedatos"
        client = MongoClient("mongodb://" + mongo_username + ":" + mongo_password + "@" + ssh_address)
    elif 'test' in host.lower():
        ssh_address = "addres"
        client = MongoClient("mongodb://" + mongo_username + ":" + mongo_password + "@" + ssh_address)
    else:
        client = MongoClient("mongodb://localhost:27017/")
    return client