
import json,requests,csv
from requests.auth import HTTPBasicAuth
from orange.common.log import Log
log = Log()


headers = {
    "Accept": 'application/json',
    "Content-Type": "application/json",
}
all_data=[]


def get_data_from_csv(excel_file):
    list_csv=[]
    with open(excel_file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            list_csv.append(row)
    return list_csv


def get_test_points_id(all_data,plan_id,suite_id,personal_access_token):
    test_points_url = 'https://aspentech-alm.visualstudio.com/AspenTech/_apis/testplan/Plans/' + plan_id + '/Suites/' + suite_id + '/TestPoint?includePointDetails=true&returnIdentityRef=true&api-version=7.1-preview.2'
    try:
        response_test_points = requests.get(test_points_url, headers=headers,
                                            auth=HTTPBasicAuth('', personal_access_token))
        all_cases = json.loads(response_test_points.text)['value']
        log.info("get test points id according to case id,response id: " + str(response_test_points.status_code))
    except Exception as e:
        log.error(e)
        return False

    list_test_points_id=[]

    for index,item in enumerate(all_data[0]):
        if item.lower() == 'id' or item.lower() == 'tc_id':
            id_index=index
        elif item == 'Result':
            result_index=index
          
    for line in all_data[1:]:
        if len(line)>2:
            for item in all_cases:
                if str(item['testCaseReference']['id']) == line[id_index]:
                    list_test_points_id.append({item['id']:line[result_index]})

    return list_test_points_id


def get_test_points_id_new(all_data,plan_id,suite_id,personal_access_token):
    test_points_url = 'https://aspentech-alm.visualstudio.com/AspenTech%20Sandbox/_apis/testplan/Plans/' + plan_id + '/Suites/' + suite_id + '/TestPoint?includePointDetails=true&returnIdentityRef=true&api-version=7.1-preview.2'
    try:
        response_test_points = requests.get(test_points_url, headers=headers,
                                            auth=HTTPBasicAuth('', personal_access_token))
        all_cases = json.loads(response_test_points.text)['value']
        log.info("get test points id according to case id,response id: " + str(response_test_points.status_code))
    except Exception as e:
        log.error(e)
        return False

    list_test_points_id=[]

    id_index, result_index, defect_index, comments_index = '', '', '', ''
    for index,item in enumerate(all_data[0]):
        item=item.lower()
        if item.lower() == 'id' or item.lower() == 'tc_id':
            id_index=index
        elif item == 'result':
            result_index=index
        elif item == 'defect':
            defect_index=index
        elif item == 'comments':
            comments_index=index
          
    for line in all_data[1:]:
        if len(line)>2:
            for item in all_cases:
                if str(item['testCaseReference']['id']) == line[id_index]:
                    list_test_points_id.append({item['id']:[line[result_index],line[defect_index],line[comments_index]]})

    return list_test_points_id



def create_run(test_points_id,plan_id,personal_access_token):
    for item in test_points_id:
            
        for key,value in item.items():
            point=key
            result=value[0].strip().lower()
            defect=str(value[1])
            comment=str(value[2])
            if result == 'passed':
                state=2
            elif result == 'failed':
                state=3
            elif result == 'active':
                state=1
            else:
                raise ValueError("Invalid input")
            data={
                    "name": "test",
                    "pointIds": [point],
                    "plan": {
                        "id": int(plan_id)
                    }
            }

        # create a run and get runid
        run_url = 'https://aspentech-alm.visualstudio.com/AspenTech%20Sandbox/_apis/test/runs?api-version=7.1-preview.3'

        try:
            response = requests.post(run_url,json=data,headers=headers,auth=HTTPBasicAuth('', personal_access_token))
            content=json.loads(response.text)
            runid=str(content["id"])

            print(runid)
        except Exception as e:
            if "Invalid URL" in str(e):
                return False
            else:
                log.error(e)

        # update result
        url = "https://aspentech-alm.visualstudio.com/AspenTech%20Sandbox/_apis/test/runs/" + runid + "/results?api-version=7.1-preview.6"
        data=[{
            "id": 100000,
            "outcome": state,
            "state": "Completed",
            "comment": comment,
            "associatedBugs": [ {
                    "id": defect
                } ]
            }]

        try:
            response = requests.patch(url,json=data,headers=headers,auth=HTTPBasicAuth('', personal_access_token))
        except Exception as e:
            if "Invalid URL" in str(e):
                return False
            else:
                log.error(e)
    
    return True