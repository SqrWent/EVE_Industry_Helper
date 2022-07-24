"""
This file includes all the raw data processing functions.
For example: fetching all the ids in EVE, fetching blueprints datas and fetching market datas.
"""
import json
import yaml
import grequests
import requests
from tqdm import tqdm
from encodings import utf_8

progressbar = None

__source_dir__ = "src"


def fetch_id_sheets():
    """
    Description:
        This Function fetches all the ids in EVE and forms a sheet under __source_dir__+"/id_sheet.json".

    Returns:
        None
    """
    pagenum = 1
    id_sheet = []
    url = "https://esi.evepc.163.com/latest/universe/types/"
    headers = {"accept": "application/json",
               "Cache-Control": "no-cache"}
    check_tag = True
    while check_tag is True:
        params = {"datasource": "serenity",
                  "page": pagenum}
        req = requests.get(url, params=params, headers=headers)
        if req.status_code != 200:
            check_tag = False
            print("Page", pagenum, "return error! Return code is ", req.status_code)
        else:
            id_sheet.append(req.json())
            print("Page", pagenum, "return succeed! Return code is ", req.status_code)
            pagenum = pagenum + 1

    json_file = open(__source_dir__ + "/id_sheet.json", "w")
    json.dump(id_sheet, json_file)
    json_file.close()


def fetch_object_infos():
    # TODO Finish exception handler!
    # TODO Switching to sql could be a better choice than json and yaml
    """
    Description:
        This function fetch all element information in EVE, saved under __source_dir__+"/objects_info.yaml".

    Returns:
        None

    """
    id_sheet = open(__source_dir__ + "/id_sheet.json", "r")
    id_sheets = json.load(id_sheet)
    id_sheet.close()
    raw_url = "https://esi.evepc.163.com/latest/universe/types/"
    id_sheet = []
    urls = []
    for sheet in id_sheets:
        id_sheet = id_sheet + sheet
    for ids in id_sheet:
        urls.append(raw_url + str(ids) + "/")

    params = {"datasource": "serenity",
              "language": "zh"}
    headers = {"accept": "application/json",
               "Accept-Language": "zh",
               "Cache-Control": "no-cache"}

    def request_update(response, *args, **kwargs):
        """
        Description:
            This function is designed to be a hook and to give a progressbar overview of grequests,
            it uses the global variable progressbar and its method update() to complete the work.

        Args:
            response: The response from GET.
            *args: Some arg used by hooks
            **kwargs: Some arg used by hooks

        Returns:
            None

        """
        progressbar.update()

    # Now fetching data and save to resp
    global progressbar
    async_list = []

    for u in urls:
        action_item = grequests.get(u, params=params, headers=headers, hooks={'response': request_update})
        async_list.append(action_item)

    progressbar = tqdm(total=len(async_list))
    resp = grequests.map(async_list)
    progressbar.close()
    progressbar = None

    saving_yaml = {}
    for single_resp in resp:
        saving_yaml[single_resp.json()["type_id"]] = single_resp.json()

    # Save data to file
    obinfo = open(__source_dir__ + "/object_info.yaml", "w+")
    yaml.dump(saving_yaml, obinfo, encoding=utf_8, allow_unicode=True)
    obinfo.close()
