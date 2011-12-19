import os.path
import sys

from importer.crawler import NetunoCrawler
from importer.parser import get_companies

crawler = NetunoCrawler('https://www.seatecnologia.com.br/netuno')
crawler.login(username=sys.argv[1], password=sys.argv[2])
crawler.go_to_all_companies()

companies = get_companies(crawler.content)
base_url = 'https://www.seatecnologia.com.br/netuno/index.php?m=companies&a=view&company_id=%s'
users_url = 'https://www.seatecnologia.com.br/netuno/index.php?m=companies&a=view&company_id=%s&tab=3'
for count, company in enumerate(companies):
    id = company['original_id']
    filename = 'netunomock/html/company%s.html' % id
    print "Importing company #%d of #%d (%s) to file %s" % (count, len(companies), company['name'], filename)
    response = crawler.browser.open(base_url%id)
    doc = file(filename, 'w')
    doc.write(response.read())
    doc.close()

    filename = 'netunomock/html/company%s-users.html' % id
    print "Importing company #%d - users" % count
    response = crawler.browser.open(users_url%id)
    doc = file(filename, 'w')
    doc.write(response.read())
    doc.close()
