import re
"""--------------------
TAGS:       RE:
all tag:    <[^>]+>
open tag:   <[^/>][^>]*>
close tag:  </[^>]+>
self close: <[^/>]+/>
"""#--------------------

re_tags =[
     "<[tag]>(.+?)</[tag]>",
     "<[tag][^>]*>(.+?)</[tag]",
     "(?<=<pre>)(.*?)(?=</pre>)",
     "(?<=>)([\w\s]+)(?=<\/)"
        ]

# READ IN FILE
fname="web_table.html"
with open(fname, 'r') as infile:
    html=infile.read()
# RETURNS ONE STRING

# Is tag in html?
#total_tags = len(all_tags)            # get total number of tags

def has_tag(tag,html):
    ntags=numTags(tag,html)
    if ntags >0:
        return True
    else:
        return False

def numTags(tag,html):
    all_tags = re.findall('<[^>]+>',html) # get all tags
    num_tags=0
    for t in all_tags:
        if tag in t:
            num_tags+=1
    return num_tags

def exact_tags(tag, html):
    all_tags = re.findall('<[^>]+>',html) # get all tags
    tags=[]
    for t in all_tags:
        if tag in t:
            tags.append(t)
    return tags

    
# REMOVE HTML TAGS
TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('', text)

# Debug Info:
#print(has_tag('</table>',html))
#print(numTags('</table>',html))
#print('exact tags: ', exact_tags('<table',html))


def find_tags(tag,html):
    etags = exact_tags(tag,html)
    ntags=numTags(tag,html) # or len(etags)

    # Check etags for special cases involving back slashes
    for i in range(0,len(etags)):
        if '\\' in etags[i]:
            print('BACKSLASH in etags!!!')
            etags[i]=tag

    ctag=etags[0].split()[0]
    ctag=ctag[0]+'/'+ctag[1:]+'>'
    if ">>" in ctag:
        ctag = ctag[:-1]
    
    #print('ctag = ', ctag) # debug info

    ctags=[]
    for n in range(0, ntags):
        ctags.append(ctag)

    def search_loop(etags,ntags,html):
        T=[]
        for t in range(0,ntags):

            # OPEN TAGS
            filler='x'*len(etags[t])
            #print('filler=',filler, ' len(filler) = ',len(filler)) # debug info
            
            tagm = re.search(etags[t], html)

            # Add Matches to List
            if tagm != None:
                T.append(tagm)

            #print(tagm)
            
            # Replace Find With Filler
            html=html.replace(etags[t],filler,1)

        return T

    OT=search_loop(etags,ntags,html)
    CT = search_loop(ctags,ntags,html)

    # Debug Info
    print("OT = ", OT)
    print("CT = ", CT)

    """!!! NOTE HAVE NOT PERFORMED STACK OPERATION TO CATCH NESTED TAGS"""

    matches=[]
    # PRINT ALL MATCHES
    for n in range(0,len(OT)):
        matches.append(html[OT[n].start():CT[n].end()])

    #print(html[OT[0].start():CT[0].end()])
    return matches # python list
    

"""*******************************"""
# CASE SPECIFIC CODE FROM HERE ON
"""*******************************"""
# Find Tables
tag = '<table'
table = find_tags(tag,html)

# Find Rows
tag = "<tr"
rows = find_tags(tag,table[0]) # Note I am only interested in the first table

# Get Number of Columns
ncols=re.findall('<td',rows[1]) # Note: table w/ headers start with index 1
cols=[]

# Debug info
#print("len(table) =",len(table))
#print(table[0])

# Extract Data From Rows
for r in rows:
    # Debug Info
    #print(remove_tags(r))#.split('</td'))
    #print(r)

    ##########################
    # Get Columns out of Rows
    for c in range(0,len(ncols)):
        start = r.find('<td')
        end = r.find('</td>') + len('</td>')

        col=r[start:end]
        col=remove_tags(col)
        print(col,"\t", end='') # Display table columns
        cols.append(col)
        r = r[end:] # position for next col    
    print() # newline for next row


