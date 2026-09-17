import re
s=open('index.html').read()
s=re.sub(r'^<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/>\n<meta name="viewport"[^>]*/>\n','',s)
s=s.replace('</style></head><body>\n','</style>\n\n',1)
s=re.sub(r'</script></body></html>\s*$','</script>\n',s)
assert s.startswith('<title>') and 'DOCTYPE' not in s and '</html>' not in s
open('artifact.html','w',encoding='utf-8').write(s); print(len(s),s[:60].replace('\n',' '))
