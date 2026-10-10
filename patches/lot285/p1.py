import re
p='index.html';s=open(p,encoding='utf-8').read()
a=s.index("const PROFILES=[\n")+len("const PROFILES=[\n");b=s.index("\n];\n/* figés depuis",a)
body=s[a:b]
# découpe en entrées de premier niveau : chaque entrée commence par " {id:'"
parts=re.split(r"(?m)^(?= \{id:')",body);parts=[x for x in parts if x.strip()]
parts=[x.rstrip().rstrip(',') for x in parts]
ids=[re.match(r" \{id:'(\w+)'",x).group(1) for x in parts]
assert sorted(ids)==sorted(['syst','fonda','flux','rv','tail','act']),ids
order=['syst','tail','fonda','rv','flux','act']   # lot 285 : du plus facile au plus dur (survie mesurée au lot 284)
new=",\n".join(parts[ids.index(k)] for k in order)
s=s[:a]+new+s[b:]
open(p,'w',encoding='utf-8').write(s)
print(ids,'->',order)
