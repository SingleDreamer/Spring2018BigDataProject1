f = open("entrez_ids_uniprot.txt", "r")
#print f.readline()
for l in f.readlines():
    l = l.split("\t")
    for i in l:
        print i
f.close()
