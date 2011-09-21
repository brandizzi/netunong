from BeautifulSoup import BeautifulSoup

COMPANY_LINK = 'https://www.seatecnologia.com.br/netuno/index.php?m=companies&a=view&company_id='

def get_organizations(content):
    soup = BeautifulSoup(content)

    company_table = soup.contents[2].contents[2].contents[3]
    company_links = (a for a in company_table.findAll('a') 
                       if a['href'].startswith(COMPANY_LINK))
    organizations = [{
            'name' : a.string.strip(),
            'original_id' : int(a['href'].split('=')[-1]),
            'description' : a['title']
            }
        for a in company_links
    ]

    return organizations
