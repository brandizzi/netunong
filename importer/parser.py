import itertools
from urlparse import urlparse, parse_qs

from BeautifulSoup import BeautifulSoup

import settings

COMPANY_LINK = 'https://www.seatecnologia.com.br/netuno/index.php?m=companies&a=view&company_id='
PARENT_TAG = 'Tarefas Filho'

def get_company_id_from_url(url):
    parsed_url = urlparse(url)
    parsed_qs = parse_qs(parsed_url.query)
    return int(parsed_qs['company_id'].pop())

def get_project_id_from_url(url):
    parsed_url = urlparse(url)
    parsed_qs = parse_qs(parsed_url.query)
    return int(parsed_qs['project_id'].pop())

def get_task_id_from_url(url):
    parsed_url = urlparse(url)
    parsed_qs = parse_qs(parsed_url.query)
    return int(parsed_qs['task_id'].pop())

def get_user_id_from_url(url):
    parsed_url = urlparse(url)
    parsed_qs = parse_qs(parsed_url.query)
    return int(parsed_qs['user_id'].pop())

class ElementNofFoundException(Exception):
    pass

def get_parent_by_tagname(element, tagname):
    try:
        name = element.name
    except AttributeError:
        name = None

    if name == tagname:
        return element
    elif name != 'html':
        return get_parent_by_tagname(element.parent, tagname)
    else:
        raise ElementNofFoundException(
            'No parent element of time <%s> found for %s' % (tagname, element))

def get_companies(content):
    soup = BeautifulSoup(content)

    some_cell = soup.find(text='Nome da Empresa')
    company_table = get_parent_by_tagname(some_cell, 'table')
    company_links = (a for a in company_table.findAll('a') 
                       if 'm=companies' in a['href'] and
                            'a=view' in a['href'] )
    companies = [{
            'name' : a.string.strip(),
            'original_id' : get_company_id_from_url(a['href']),
            'description' : a['title']
            }
        for a in company_links
    ]

    return companies

def is_parent_task(content):
    return PARENT_TAG in content

def get_projects(content):
    soup = BeautifulSoup(content)

    project_table = soup.find('table', {'class':'tbl'})
    project_rows = project_table.findAll('tr')[2:-1]

    projects = []
    for row in project_rows:
        (
            completude_cell, 
            company_cell, 
            project_cell, 
            start_cell,
            expected_end_cell,
            real_end_cell,
            problem_cell,
            responsible_cel,
            tasks_count_cell,
            selection_cell,
            situation_cell
        ) = row.findAll('td')
        projects.append({
            'name' : project_cell.a.text.split(">").pop(),
            'original_id' : get_project_id_from_url(project_cell.a['href']),
            'company_id' : get_company_id_from_url(company_cell.a['href']),
            'description' : ''
        })
    return projects

def get_task(content):
    soup = BeautifulSoup(content)
    # Is a leaf tasks (tasks that does not have subtasks) or a parent task
    # (a task with subtasks)?
    is_parent = is_parent_task(content)
    if not is_parent:
        task_type =  'leaf'
    else:
        task_type =  'parent'

    # Getting name
    task_supertable = soup.find('table', {'class':'std'})
    task_table = task_supertable.findAll('table')[0]
    name_row = task_table.findAll('tr')[2]
    name_cell = name_row.findAll('td')[1]
    name = name_cell.strong.text
    # Getting original id
    ids_table = soup.findAll('table')[6]
    task_url = ids_table.findAll('a')[2]['href']
    original_id = get_task_id_from_url(task_url)
    # Getting project id
    project_url = ids_table.findAll('a')[1]['href']
    project_id = get_project_id_from_url(project_url)
    # Getting subtasks ids
    if is_parent:
        try:
            subtasks_ids = [get_task_id_from_url(tr.a['href'])
                    for tr in soup.find('table', {'class':'tbl'}).findAll('tr')[1:]
                    if tr.a and 'task_id' in tr.a['href']]
        except AttributeError:
             subtasks_ids = []
    else:
        subtasks_ids = []
    return {
            'type' : task_type, 
            'name' : name, 
            'original_id' : original_id,
            'project_id' : project_id,
            'description' : '',
            'subtasks_ids' : subtasks_ids
    }

def get_list_of_partial_tasks(content):
    soup = BeautifulSoup(content)
    tasks_table = soup.find('table', {'class':'tbl'})
    tasks_ids = [get_task_id_from_url(img.parent['href'])
                for img in tasks_table.findAll('img', {'alt':'Editar Tarefa'})]
    return [{'type' : 'partial', 'original_id' : int(task_id)}
            for task_id in tasks_ids]

def get_users(content):
    soup = BeautifulSoup(content)
    company_url = soup.find('td', {'id':'toptab_0'}).find('a')['href']
    company_id = get_company_id_from_url(company_url)
    users_trs = [a.parent.parent 
                for a in soup.findAll('a') 
                if '?m=admin&a=viewuser&' in  a['href']][1:]
    users = []
    for tr in users_trs:
        user_id = get_user_id_from_url(tr.a['href'])
        name = tr.findAll('td')[1].text
        splitted_name = name.split(",")
        splitted_name = [name 
                for name in " ".join(reversed(splitted_name)).split() 
                if name]
        first_name = splitted_name[0]
        last_name = splitted_name[-1]
        middle_name = " ".join(splitted_name[1:-1])
        username = tr.a.text
        email = "@".join([username, settings.NETUNONG_EMAIL_DOMAIN])
        users.append({
            'original_id' : user_id,
            'first_name' : first_name,
            'middle_name' : middle_name,
            'last_name' : last_name,
            'username' : username,
            'company_id' : company_id,
            'email' : email,
            'password' : username
        })
    return users
