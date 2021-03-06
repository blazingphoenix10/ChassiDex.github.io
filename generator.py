from jinja2 import Template
import mistune
import os

data_folder = 'data/'
data_files = sorted(os.listdir(data_folder))
data = []
listbytag = {}
renderer = mistune.Renderer(escape=True, hard_wrap=True)
markdown = mistune.Markdown(renderer=renderer)
output_folder = 'hosts/'

hosttemplate = ''
with open('templates/hostpage.html') as tf:
    hosttemplate = Template(tf.read())

indextemplate = ''
with open('templates/index.html') as tf:
    indextemplate = Template(tf.read())

# read data
for file in data_files:
    with open(data_folder + file) as f:
        t = f.read().split('---')
        header = t[1].strip().split('\n')
        markdown_content = t[2].strip()
        data_point = {}
        for line in header:
            key = line.split(':')[0].strip()
            value = line.split(':')[1].strip()
            data_point[key] = value
        data_point['tags'] = [tag.strip() for tag in data_point['tags'].split(',')]
        data_point['file'] = file[:-2]+'html'
        data_point['rendered_markdown'] = markdown(markdown_content)
        data.append(data_point)

# render host files
for host in data:
    html = hosttemplate.render(name=host['name'],color=host['color'],tags=host['tags'],markdown=host['rendered_markdown'])
    file = output_folder+host['file']
    with open(file,'w') as f:
        f.write(html)
        f.close()
        print('Wrote ' + file)

# list by tags
for i in range(len(data)):
    for tag in data[i]['tags']:
        if tag in listbytag.keys():
            listbytag[tag].append(i)
        else:
            listbytag[tag] = [i]

tagslist = list(listbytag.keys())
tagslist.sort()

# render home page
with open('index.html','w') as f:
    html = indextemplate.render(data=data,tagslist=tagslist,listbytag=listbytag)
    f.write(html)
    f.close()
    print('\nWrote index.html')
