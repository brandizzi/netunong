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
