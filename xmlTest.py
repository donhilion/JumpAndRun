import xml.dom.minidom as dom

d = {} 
baum = dom.parse("testXml.xml")

for entry in baum.firstChild.childNodes: 
	if entry.nodeName == "entry": 
		key = value = None

		for node in entry.childNodes: 
			if node.nodeName == "key": 
				key = eval("%s('%s')" % (node.getAttribute("type"), 
                              node.firstChild.data.strip()))
			elif node.nodeName == "value": 
				value = eval("%s('%s')" % (node.getAttribute("type"), 
                              node.firstChild.data.strip()))

		d[key] = value

for key in d.keys():
	print(key)
	print(d[key]+1)