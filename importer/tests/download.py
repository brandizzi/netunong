import os.path
import sys

from importer.crawler import NetunoCrawler
from importer.parser import get_companies, get_list_of_partial_tasks, get_task

crawler = NetunoCrawler('https://www.seatecnologia.com.br/netuno')
crawler.login(username=sys.argv[2], password=sys.argv[3])
base_url = sys.argv[1]
company_url = base_url + '?m=companies&a=view&company_id=%s'
users_url = base_url + '?m=companies&a=view&company_id=%s&tab=3'
task_url = base_url + '?m=tasks&a=view&task_id=%s' 
'''crawler.go_to_all_companies()

companies = get_companies(crawler.content)
for count, company in enumerate(companies):
    id = company['original_id']
    filename = 'netunomock/html/company%s.html' % id
    print "Importing company #%d of #%d (%s) to file %s" % (count, len(companies), company['name'], filename)
    response = crawler.browser.open(company_url%id)
    doc = file(filename, 'w')
    doc.write(response.read())
    doc.close()

    filename = 'netunomock/html/company%s-users.html' % id
    print "Importing company #%d - users" % count
    response = crawler.browser.open(users_url%id)
    doc = file(filename, 'w')
    doc.write(response.read())
    doc.close()'''

print 'Going to all tasks'
#crawler.go_to_all_tasks()
print 'Now parsing partial tasks'
tasks = get_list_of_partial_tasks(file('netunomock/html/tasks_all.html').read())

for count, task in enumerate(tasks):
    id = task['original_id']
    filename = 'netunomock/html/task%s.html' % id
    if not os.path.exists(filename):
        print "Importing task #%d of #%d to file %s" % (count+1, len(tasks), filename)
        response = crawler.browser.open(task_url%id)
        content = response.read()
        doc = file('tmp', 'w')
        doc.write(content)
        doc.close()
        #task = get_task(content)
        if 'Tarefas Filho' in content: # SGHOUD GO TO TAB!
            response = crawler.browser.follow_link(text='Tarefas Filho')
            content = response.read()
            task = get_task(content)
            for count, subid in enumerate(task['subtasks_ids']):
                subfilename = 'netunomock/html/task%s.html' % subid
                print "Importing subtask #%d of #%d to file %s" % (count+1, len(task['subtasks_ids']), subfilename)
                response = crawler.browser.open(task_url%subid)
                doc = file(subfilename, 'w')
                doc.write(response.read())
                doc.close()
        doc = file(filename, 'w')
        doc.write(content)
        doc.close()
    else:
        print 'Already imported task #%s (%s)' % (count+1, id)
