from types import SimpleNamespace
from azure.devops.v6_0.work_item_tracking.models import Wiql, WorkItemQueryResult
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v5_1.py_pi_api import JsonPatchOperation
import Token
import requests
import base64
import json
import os
import subprocess
import time
from selenium import webdriver
import pyperclip
import datetime
import re


WEBDRIVER_CHROME = f"/usr/bin/chromedriver"

def get_context(auth_token, url):
    try:
        context = SimpleNamespace()
        context.runner_cache = SimpleNamespace()

        context.connection = Connection(
            base_url=url,
            creds=BasicAuthentication('PAT', auth_token))

        return context
    except:
        pass


if os.path.exists("/ElcSoftware/misc/Python36TK/bin/python3"):
    url = 'http://dvdtfsp:8080/tfs/ComputingSystems_Collection'
else:
    url = 'https://azuredevops.rafael.co.il/ComputingSystems_Collection'

s = requests.session()

def init_globals():
    global token
    token = Token.createToken()
    if token != None:
        global context
        context = get_context(token, url)
        global access_token
        access_token = ":" + token
        s.headers = {"Authorization": f"Basic {base64.b64encode(access_token.encode()).decode()}", "Content-Type": "application/json"}
        global wit_client
        wit_client = context.connection.clients.get_work_item_tracking_client()
    else:
        print(f'# error creating Token')
    return token


def get_members(project):
    team_url = f"{url}/_apis/teams?api-version=5.1-preview.3"
    members = []

    authorization = str(base64.b64encode(bytes(':' + token, 'ascii')), 'ascii')
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic ' + authorization
    }

    response = requests.get(url=team_url, headers=headers)
    response_json = json.loads(response.text)

    for value in response_json["value"]:
        if value['projectName'] == project:
            team_id = value["id"]
            project_id = value["projectId"]
            team_url = f'{url}/_apis/projects/{project_id}/teams/{team_id}/members?api-version=5.1'
            response = requests.get(url=team_url, headers=headers)
            users = json.loads(response.text)
            for user in users["value"]:
                members.append(user["identity"]["displayName"])
    return members


def get_projects():
    try:
        project_url = f"{url}/_apis/projects?api-version=6.0"
        projects = json.loads(s.get(project_url).content.decode())['value']
        projects = [(x['name']) for x in projects]
        return projects
        
    except:
        return []


def get_project_id(project):
    api_url = f"{url}/_apis/projects?api-version=5.1"
    r = json.loads(s.get(api_url).content.decode())
    for value in r['value']:
        if value['name'] == project:
            return value['id']
    return ''


def get_iterations(area):
    area = area.split('\\')
    api_url = f"{url}/{area[0]}/_apis/work/teamsettings/iterations?api-version=6.0"

    r = json.loads(s.get(api_url).content.decode())
    if not r['count']:
        api_url = f"{url}/{area[0]}/{area[1]}/_apis/work/teamsettings/iterations?api-version=6.0"
        r = json.loads(s.get(api_url).content.decode())

    iterations = []

    for attribute in r['value']:
        if attribute['attributes']['startDate'] and attribute['attributes']['finishDate']:
             given_date=datetime.datetime.strptime(attribute['attributes']['finishDate'],"%Y-%m-%dT%H:%M:%SZ")
             curent_date=datetime.datetime.utcnow()
             if(given_date>curent_date):
                iterations.append(attribute['path'])

    return iterations


def get_workitem_id(project, area, iteration):
    query = Wiql(
        query=f"""SELECT [System.Id] FROM workitems
           WHERE [System.WorkItemType] IN ('User Story')
           AND [System.State] <> 'Closed'
           AND ([System.Title] = 'Bugs' OR [System.Title] = 'Features')
           AND [System.AreaPath] = '{area}'
           ORDER BY [System.Title]"""
    )
    query_results = wit_client.query_by_wiql(query).work_items
    ids = []
    if query_results:
        for work_item in query_results:
            ids.append(work_item.id)
        return ids
    else:
        return add_epic(project, area, iteration, 'Bugs And Features')


def add_epic(project, area, iteration, name, proj_id=None):
    epic_patch_document = [
        JsonPatchOperation(
            op="add",
            path="/fields/System.WorkItemType",
            value="Epic",
        ),
        JsonPatchOperation(
            op="add",
            path="/fields/System.Title",
            value=name,
        ),
        JsonPatchOperation(
            op="add",
            path="/fields/System.IterationPath",
            value=iteration,
        ),
        JsonPatchOperation(
            op="add",
            path="/fields/System.AreaPath",
            value=area,
        ),
        JsonPatchOperation(
            op="add",
            path="/fields/System.State",
            value="New",
        ),
        JsonPatchOperation(
            op="add",
            path="/fields/Custom.SecurityClassification",
            value="a. Unclassified",
        )

    ]
    if proj_id is not None:
            url_input = 'dvdtfsp:8080/tfs/ElectronicsFieldCollection/{}/_workitems/{}'.format(project, proj_id)
            epic_patch_document.append(JsonPatchOperation(from_=None, op='add', path="/relations/-", value={
                'rel': "System.LinkTypes.Hierarchy-Reverse",
                'url': url_input
            }))
    epic_work_item = wit_client.create_work_item(
        document=epic_patch_document,
        project=project,
        type='Epic'
    )
    epic_id = epic_work_item.id
    if name == 'Bugs And Features':
        return add_feature(project, area, iteration, epic_id, ['Bugs', 'Features'])
    else:
        return epic_id


def add_feature(project, area, iteration, epic_id, feature_names):
    ids = []
    for feature_name in feature_names:
        feature_patch_document = [
            JsonPatchOperation(
                op="add",
                path="/fields/System.WorkItemType",
                value="Feature",
            ),
            JsonPatchOperation(
                op="add",
                path="/fields/System.Title",
                value=feature_name,
            ),
            JsonPatchOperation(
                op="add",
                path="/fields/System.IterationPath",
                value=iteration,
            ),
            JsonPatchOperation(
                op="add",
                path="/fields/System.AreaPath",
                value=area,
            ),
            JsonPatchOperation(
                op="add",
                path="/fields/System.State",
                value="New",
            ),
            JsonPatchOperation(
                op="add",
                path="/fields/Custom.SecurityClassification",
                value="a. Unclassified",
            )
        ]
        if epic_id is not None:
            url_input = 'dvdtfsp:8080/tfs/ElectronicsFieldCollection/{}/_workitems/{}'.format(project, epic_id)
            feature_patch_document.append(JsonPatchOperation(from_=None, op='add', path="/relations/-", value={
                'rel': "System.LinkTypes.Hierarchy-Reverse",
                'url': url_input
            }))
        feature_result = wit_client.create_work_item(document=feature_patch_document, project=project,
                                                     type='Feature')
        if len(feature_name) == 2:
            ids.append(add_userstory(feature_name, project, area, iteration, feature_result.id))
        else:
            return feature_result.id
    return ids


def add_userstory(title, project, area, iteration, feature_id):
    userstory_patch_document = [
        JsonPatchOperation(
            op="add",
            path="/fields/System.WorkItemType",
            value="User Story",
        ),
        JsonPatchOperation(
            op="add",
            path="/fields/System.Title",
            value=title,
        ),
        JsonPatchOperation(
            op="add",
            path="/fields/System.IterationPath",
            value=iteration,
        ),
        JsonPatchOperation(
            op="add",
            path="/fields/System.AreaPath",
            value=area,
        ),
        JsonPatchOperation(
            op="add",
            path="/fields/System.State",
            value="New",
        ),
        JsonPatchOperation(
            op="add",
            path="/fields/Custom.SecurityClassification",
            value="a. Unclassified",
        )
    ]
    if feature_id is not None:
        url_input = 'dvdtfsp:8080/tfs/ElectronicsFieldCollection/{}/_workitems/{}'.format(project, feature_id)
        userstory_patch_document.append(JsonPatchOperation(from_=None, op='add', path="/relations/-", value={
            'rel': "System.LinkTypes.Hierarchy-Reverse",
            'url': url_input
        }))
    userstory_result = wit_client.create_work_item(document=userstory_patch_document, project=project, type='Feature')

    return userstory_result.id


def get_repos(project):
    api_url = f"{url}/{project}/_apis/git/repositories?api-version=5.1"
    r = json.loads(s.get(api_url).content.decode())
    repos = []
    for value in r['value']:
        repos.append(value['name'])
    sorted_repos=sorted(repos)
    return sorted_repos


def get_repos_id(project, repo):
    api_url = f"{url}/{project}/_apis/git/repositories?api-version=5.1"
    r = json.loads(s.get(api_url).content.decode())
    for value in r['value']:
        if value['name'] == repo:
            return value['id']
    return ''


def get_commit_id(project, repo_id):
    api_url = f"{url}/{project}/_apis/git/repositories/{repo_id}/commits?api-version=5.1"
    r = json.loads(s.get(api_url).content.decode())
    try:
        return r['value'][0]['commitId']
    except:
        return ''


def add_task(title, description, type, member, project , area, iteration, repo_name,test_name,seed):
    if os.path.exists("/ElcSoftware/misc/Python36TK/bin/python3"):
        proj_id = get_project_id_on_soc()
        to_workitem_id = get_repo_id_on_soc(proj_id)
        areas=get_root_areas_list("SOC_Dev_Department")
        for area_path in areas:
            if area in area_path:
                area=area_path
                break
                
  

    else:
        ids = get_workitem_id(project, area, iteration)
        if type == 'Bug':
            to_workitem_id = ids[0]
        else:
            to_workitem_id = ids[1]
            type = "Task"

    operation = 'add'

    patch_document = []
    if title is not None:
        patch_document.append(JsonPatchOperation(from_=None, op=operation, path="/fields/System.Title", value=title))

    if member is not None:
        patch_document.append(JsonPatchOperation(from_=None, op=operation, path="/fields/System.AssignedTo", value=member))

    if area is not None:
        patch_document.append(JsonPatchOperation(from_=None, op=operation, path="/fields/System.AreaPath", value=area))

    if iteration is not None:
        patch_document.append(JsonPatchOperation(from_=None, op=operation, path="/fields/System.IterationPath", value=iteration))

    if to_workitem_id is not None:
        url_input = 'dvdtfsp:8080/tfs/ElectronicsFieldCollection/{}/_workitems/{}'.format(project, to_workitem_id)
        patch_document.append(JsonPatchOperation(from_=None, op=operation, path="/relations/-", value={
            'rel': "System.LinkTypes.Hierarchy-Reverse",
            'url': url_input
        }))

    
    time.sleep(1)
    project_id = get_project_id(project)
    repo_id = get_repos_id(project, repo_name)
    commit_id = get_commit_id(project, repo_id)
    info = f"<div>********************DO NOT REMOVE********************</div>"
    info += f"<div>commit: {commit_id}</div>"
    info += f"<div>test name: {test_name}</div>"
    info += f"<div>seed: {seed}</div>"
    info += f"<div>***********************************************************</div>"
    description = info+description
    if commit_id != '':
        url_input = 'vstfs:///Git/Commit/{}%2F{}%2F{}'.format(project_id, repo_id, commit_id)
        patch_document.append(JsonPatchOperation(from_=None, op='add', path="/relations/-", value={
            'rel': "ArtifactLink",
            'url': url_input,
            'attributes': {
                'name': 'Fixed in Commit'}
        }))
    if type == 'Bug':
        patch_document.append(JsonPatchOperation(from_=None, op=operation, path="/fields/Custom.EPRTypepic", value="Defect"))
    else:
        patch_document.append(JsonPatchOperation(from_=None, op=operation, path="/fields/Custom.EPRTypepic", value="Change Request"))

    patch_document.append(JsonPatchOperation(from_=None, op=operation, path="/fields/Custom.ERPIdentificationActivity", value="2. Verification"))
    patch_document.append(JsonPatchOperation(from_=None, op=operation, path="/fields/Custom.Disciplines", value="FW"))
    patch_document.append(
    JsonPatchOperation(
        op="add",
        path="/fields/Custom.SecurityClassification",
        value="a. Unclassified",
    ))
    if description is not None:
        patch_document.append(
            JsonPatchOperation(from_=None, op=operation, path="/fields/System.Description", value=description))
    
    try:
        work_item = wit_client.create_work_item(document=patch_document, project=project, type="Bug")
        print("# Bug Uploaded")

        subprocess.call(['pkill', "klipper"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        subprocess.call(['klipper'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

        
        token_url = f"{url}/SOC_Dev_Department/_workitems/edit/{get_bug_id(title)}" #TODO: add klipper suport
        pyperclip.copy(token_url)
        #subprocess.run(['xsel', "-i"],input=token_url.encode("utf-8"))
        #clipboard.copy(token_url)


    except Exception as e:
        print(f"# Error: {e}")


def get_repo_name():
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)

    result = subprocess.run(['git', 'config', '--get', 'remote.origin.url'], check=True, universal_newlines=False, stdout=subprocess.PIPE)
   

    if result.returncode == 0:
        git_output = result.stdout.strip()
        repo_name = os.path.basename(git_output)
        return repo_name.decode()
    return ""

def get_area(project,member):
    areas=[]
    team_url = f"{url}/_apis/teams?api-version=5.1-preview.3"


    authorization = str(base64.b64encode(bytes(':' + token, 'ascii')), 'ascii')
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic ' + authorization
    }

    response = requests.get(url=team_url, headers=headers)
    response_json = json.loads(response.text)

    for value in response_json["value"]:
        if value['projectName'] == project:

            team_id = value["id"]
            project_id = value["projectId"]
            

            team_url = f'{url}/_apis/projects/{project_id}/teams/{team_id}/members?api-version=5.1'
            response = requests.get(url=team_url, headers=headers)
            users = json.loads(response.text)
            areas.append(value["name"])
            for user in users["value"]:
                if(member in user["identity"]["displayName"]):
                    area=value["name"]
                    
    areas.remove(area)
    areas.insert(0,area)
    return areas


def get_root_areas_list(project_name):
    path_list = []
    root_nodes = wit_client.get_root_nodes(project_name, depth=3)
    areas = root_nodes[0].children
    path_string = project_name
    if areas is not None:
        for child in areas:
            path_string = path_string + "\\" + child.name
            path_list.append(path_string)
            if child.has_children:
                for child2 in child.children:
                    path_string2 = path_string + "\\" + child2.name
                    if child2.has_children:
                        for child3 in child2.children:
                            path_string3 = path_string2 + "\\" + child3.name
                            path_list.append(path_string3)

            path_string = project_name
        return path_list
    return []


def get_bug_workitems():
    project_name = "SOC_Dev_Department"
    base_url = f"{url}/{project_name}/_apis/wit/wiql?api-version=6.0"
    repo = get_repo_name()
    repo=repo.replace("_verif","")
    repo=repo.replace("_V1","")
    repo=repo.replace("FPGA_","")
    repo=repo.replace("IP_REPO_","")
    proj_id = get_project_id_on_soc()
    repo_id=get_repo_id_on_soc(proj_id)
    wiql_query= {
       
    }
    wiql_query = {
             "query": f"SELECT [System.Id], [System.Title] FROM WorkItemLinks WHERE ([Source].[System.Id] = '{repo_id}' AND [System.Links.LinkType] = 'System.LinkTypes.Hierarchy-Forward')  ORDER BY [System.CreatedDate] DESC mode(Recursive) "
 
    }

    try:
        response = requests.post(
           base_url,
           json=wiql_query,
           auth=("", token)
        )
        response.raise_for_status()
        wiql_result = response.json()
        
        workitem_ids = [result['target']['id'] for result in wiql_result['workItemRelations']]

        workitems = []
        stateitem = []
        for workitem_id in workitem_ids:
            workitem_url = f"{url}/{project_name}/_apis/wit/workitems/{workitem_id}?api-version=6.0"
            response = requests.get(workitem_url, auth=("", token))
            response.raise_for_status()
            workitem = response.json()
            if(workitem['fields']['System.WorkItemType'] == 'Bug'):
                if(workitem['fields']['Custom.EPRTypepic'] == 'Defect'):
                    if(workitem['fields']['System.Description'].startswith("<div>****************")):
                        workitems.append(f"{workitem['fields']['System.Title']}  <vrc>")
                    else:
                        workitems.append(workitem['fields']['System.Title'])
                    stateitem.append(workitem['fields']['System.State'])

        return workitems,stateitem

    except requests.exceptions.RequestException as e:
        print(f"# Error: {e}")
        return []


def pull_commit_by_bug(bug):
    try:
        subprocess.run(['git', 'reset', '--hard'])
        subprocess.run(['git', 'pull', 'origin', bug], check=True, universal_newlines=False, stdout=subprocess.DEVNULL)
        subprocess.run(['git', 'submodule', 'update','--init', '--recursive'], check=True, universal_newlines=False, stdout=subprocess.DEVNULL)

        print("# Files Pulled")
        return True
    except subprocess.CalledProcessError as e:
        print(f"# Error: {e}")
        return False


def get_current_project_name():
    try:
        result = subprocess.run(['git', 'config', '--get', 'remote.origin.url'], check=True, universal_newlines=False, stdout=subprocess.PIPE)
        if result.returncode == 0:
            repository_path = result.stdout.strip()
            project_name = repository_path.split(b'/')[5]
            return project_name.decode()

            
        return ''

    except FileNotFoundError:
        ("# Error: 'git' command not found.")


def get_bug_id(bug):
    query = Wiql(
        query=f"""SELECT [System.Id] FROM workitems
           WHERE [System.State] <> 'Closed'
           AND [System.Title] = '{bug}'"""
    )
    query_results = wit_client.query_by_wiql(query).work_items
    for work_item in query_results:
        return work_item.id


def get_bug_description(bug_name):
    bug_id = get_bug_id(bug_name)
    org_url = f"{url}/SOC_Dev_Department/_apis/wit/workitems/{bug_id}?api-version=6.0"

    try:
        response = requests.get(org_url, headers=s.headers)
        response.raise_for_status()
        result = response.json()
        bug_description = result['fields']['System.Description']
        match_commit = re.search("commit: (\w+)", bug_description)
        match_test = re.search("test name: (\w+)", bug_description)
        match_seed = re.search("seed: (\w+)", bug_description)              
        if match_commit :
            match_commit = match_commit.group(1)
        else:
            print("seed not found in tfs bug")
        if match_test :
            match_test = match_test.group(1)
        else:
            print("test not found in tfs bug")
        if match_seed :
            match_seed = match_seed.group(1)
        else:
            print("seed not found in tfs bug")
        return match_commit, match_test, match_seed
    except requests.exceptions.HTTPError as err:
        (f"# Error: {err}")


def get_project_id_on_soc():
    base_url = f"{url}/SOC_Dev_Department/_apis/wit/wiql?api-version=6.0"

    wiql_query = {
       "query": "SELECT [System.Id], [System.Title] FROM WorkItems WHERE [System.WorkItemType] = 'Project' ORDER BY [System.CreatedDate] DESC"
    }
    try:
        response = requests.post(
            base_url,
            json=wiql_query,
            auth=("", token)
        )
        response.raise_for_status()
        wiql_result = response.json()
        workitem_ids = [result['id'] for result in wiql_result['workItems']]
        for workitem_id in workitem_ids:
            workitem_url = f"{url}/SOC_Dev_Department/_apis/wit/workitems/{workitem_id}?api-version=6.0"
            response = requests.get(workitem_url, auth=("", token))
            response.raise_for_status()
            workitem = response.json()
            if(get_current_project_name() == workitem['fields']['System.Title']):
                return workitem_id

    except requests.exceptions.RequestException as e:
        (f"# Error: {e}")
        return None
    print((f'ERROR: there is no "{get_current_project_name()}" diamond in SOC_Dev_Department'))
    raise FileNotFoundError(f'ERROR: there is no "{get_current_project_name()}" diamond in SOC_Dev_Department')
    

def get_defects_id(name, proj_id):
    base_url = f"{url}/SOC_Dev_Department/_apis/wit/wiql?api-version=6.0"
  

    wiql_query = {
             "query": f"SELECT [System.Id], [System.Title] FROM WorkItemLinks WHERE ([Source].[System.Id] = '{proj_id}'  AND [System.Links.LinkType] = 'System.LinkTypes.Hierarchy-Forward')  ORDER BY [System.CreatedDate] DESC mode(Recursive) "
 
    }
 
    try:
        response = requests.post(
            base_url,
            json=wiql_query,
            auth=("", token)
        )
        response.raise_for_status()
        wiql_result = response.json()

    except requests.exceptions.RequestException as e:
        print(f"# Error: {e}")
    

    workitem_ids = [result['target']['id'] for result in wiql_result['workItemRelations']]

    workitems = []
    for workitem_id in workitem_ids:
        workitem_url = f"{url}/SOC_Dev_Department/_apis/wit/workitems/{workitem_id}?api-version=6.0"
        response = requests.get(workitem_url, auth=("", token))
        response.raise_for_status()
        workitem = response.json()
        if(workitem['fields']['System.WorkItemType'] == 'Epic' and workitem['fields']['System.Title']== 'Defects_ChangeRequests' ):
           return  workitem["id"]

    if not len(workitems):
        print("create new Defects_ChangeRequests")
        return add_epic(get_current_project_name(), 'SOC_Dev_Department\SOC_leadership', 'SOC_Dev_Department', 'Defects_ChangeRequests', proj_id)
    


def get_repo_id_on_soc(proj_id):
    base_url = f"{url}/SOC_Dev_Department/_apis/wit/wiql?api-version=6.0"
    repo = get_repo_name()
    repo=repo.replace("_verif","")
    repo=repo.replace("_V1","")
    repo=repo.replace("FPGA_","")
    repo=repo.replace("IP_REPO_","")
    wiql_query = {
       "query": f"SELECT [System.Id], [System.Title] FROM WorkItems WHERE [System.WorkItemType] = 'Feature' AND [System.Title] = '{repo}' ORDER BY [System.CreatedDate] DESC"
    }
    try:
        response = requests.post(
            base_url,
            json=wiql_query,
            auth=("", token)
        )
        response.raise_for_status()
        wiql_result = response.json()

        workitem_ids = [result['id'] for result in wiql_result['workItems']]

    except requests.exceptions.RequestException as e:
        print(f"# Error: {e}")
    
    if not len(workitem_ids):
        epic_id = get_defects_id(get_current_project_name(), proj_id)
        names = []
        names.append(repo)
        return add_feature(get_current_project_name(), 'SOC_Dev_Department\SOC_leadership', 'SOC_Dev_Department', epic_id , names)
    return workitem_ids[0]
