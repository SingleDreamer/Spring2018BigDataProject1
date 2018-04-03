#import xml.etree.ElementTree as ET
#tree = ET.parse('uniprot-human.xml')
#tree = ET.parse('uniprot.xsd.xml')
#root = tree.getroot()
#for child in root:
#    print child.tag, child.attrib


import xml.etree.ElementTree as etree
for event, elem in etree.iterparse("../raw_data/uniprot-human.xml", events=('end',)):
  #print "new\n"
  #print event, elem
  #if event == 'end':
      #print elem.tag
      #print elem.attrib
      #if elem.tag == 'name':
  if elem.tag == '{http://uniprot.org/uniprot}name':
    #print "hi"
    print elem.text
  elem.clear()
