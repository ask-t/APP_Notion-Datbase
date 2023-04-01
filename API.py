import requests, json,config, os
import pandas as pd

url = "https://api.notion.com/v1/pages"
path = os.getcwd()
token = config.NOTION_TOKEN


headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13"
}

def fetchData(databaseId, headers = headers):
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"

    res = requests.request("POST", readUrl, headers=headers)
    data = res.json()
    print(res.status_code)
    # print(res.text)
    column_list = []
    column = data["results"][0]["properties"].keys()
    for i in column:
        a = []
        datatype = data["results"][0]["properties"][i]["type"]
        a.append(i)
        a.append(datatype)
        column_list.append(a)
    return column_list



def readDatabase(databaseId, headers):
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"
    res = requests.request("POST", readUrl, headers=headers)
    data = res.json()
    print(res.status_code)
    # print(res.text)
    res = requests.request("POST", readUrl, headers=headers)
    data = res.json()
    print(res.status_code)
    # print(res.text)
    column_list = []
    column = data["results"][0]["properties"].keys()
    for i in column:
        a = []
        datatype = data["results"][0]["properties"][i]["type"]
        a.append(i)
        a.append(datatype)
        column_list.append(a)
    with open('./db.json', 'w', encoding='utf8') as f:
        "{}".format(json.dump(data, f, ensure_ascii=False,indent=2))
    with open('./db.json','r',encoding='utf8') as f:
        data = json.load(f)

    result_len = len(data["results"])
    column_len = len(column_list)
    selected_rows = []
    for i in range(result_len):
        a = []
        for j in range(column_len):
            try:
                value = data["results"][i]["properties"][column_list[j][0]][column_list[j][1]][0]["plain_text"]
                a.append(value)
            except IndexError:
                pass
        selected_rows.append(a)

    column_data = []
    for i in column_list:
        column_data.append(i[0])

    df = pd.DataFrame(selected_rows,columns=column_data)
    df = df.replace([''], [None]).dropna(how='all')
    return df

#readDatabase(databaseId, headers)


def createPage(row,databaseId, headers = headers):
    createUrl = 'https://api.notion.com/v1/pages'
    newPageData = {"parent": { "database_id": databaseId },
	"properties": {
        }
    }

    for i in row:
        object ={
            i[0]:{
                i[1]: [
                    {"type":"text", "text": {
                    "content": i[2] }
                        }
                    ]
                }
            }
        newPageData["properties"].update(object)
    data = json.dumps(newPageData)
    print(newPageData)
    res = requests.request("POST", createUrl, headers=headers, data=data)
    print(res.status_code)
    print(res.text)
    return readDatabase(databaseId, headers)

# createPage(databaseId, headers)

def updatePage(pageId, headers):
    updateUrl = f"https://api.notion.com/v1/pages/{pageId}"

    updateData = {
        "properties": {
            "Value": {
                "rich_text": [
                    {
                        "text": {
                            "content": "Pretty Good"
                        }
                    }
                ]
            }
        }
    }

    data = json.dumps(updateData)

    response = requests.request("PATCH", updateUrl, headers=headers, data=data)

    print(response.status_code)
    print(response.text)

def create_csv(databaseId, headers = headers):
    df = readDatabase(databaseId, headers)
    df = df.replace([''], [None]).dropna(how='all')
    df.to_csv(f'{path}/to_csv_out.csv', header=False, index=False)