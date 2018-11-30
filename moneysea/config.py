# coding=utf-8

class Config:
    #-------------------------- File path --------------------------
    #input
    INPUT_DIR = "input"

    STOCK_ID_NAME_MAP_SHA = "input/common/stock_id_name_map/sha"
    STOCK_ID_NAME_MAP_SZ = "input/common/stock_id_name_map/sz"
    STOCK_ID_NAME_MAP_OPEN = "input/common/stock_id_name_map/open"

    CURRENT_HOLDED_PATH = "input/holded"

    STOCKS_PATH = "input/stocks"

    CLASSFY_PATH = "input/classfy"
    CLASSFY_XML = "input/classfy/classfy.xml"

    PRICES_PATH = "input/prices"

    #output
    OUTPUT = "output/"

    def __init__(self):
        pass
