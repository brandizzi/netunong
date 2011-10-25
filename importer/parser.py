from urlparse import urlparse, parse_qs

from BeautifulSoup import BeautifulSoup

COMPANY_LINK = 'https://www.seatecnologia.com.br/netuno/index.php?m=companies&a=view&company_id='

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

def get_companies(content):
    soup = BeautifulSoup(content)

    company_table = soup.contents[2].contents[2].contents[3]
    company_links = (a for a in company_table.findAll('a') 
                       if a['href'].startswith(COMPANY_LINK))
    companies = [{
            'name' : a.string.strip(),
            'original_id' : get_company_id_from_url(a['href']),
            'description' : a['title']
            }
        for a in company_links
    ]

    return companies

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
    is_parent = soup.findAll('table')[14].findAll('td')[2].a.text == 'Tarefas Filho'
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
        subtasks_ids = [get_task_id_from_url(tr.a['href'])
                for tr in soup.findAll('table')[16].findAll('tr')[1:]]
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

