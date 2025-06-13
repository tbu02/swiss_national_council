import csv
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, FOAF, XSD

# Initialiser le graphe RDF
g = Graph()

# Définir les namespaces utiles
WD = Namespace("http://www.wikidata.org/entity/")
WDT = Namespace("http://www.wikidata.org/prop/direct/")
SCHEMA = Namespace("http://schema.org/")

# Ajouter les namespaces au graphe
g.bind("wd", WD)
g.bind("wdt", WDT)
g.bind("schema", SCHEMA)

data_file = 'conseillers.csv'  # <-- à adapter avec ton vrai chemin CSV

# Lire le CSV et ajouter les triplets RDF
with open(data_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Identifier la personne
        person_uri = URIRef(row['person'])
        g.add((person_uri, RDF.type, WD['Q5']))  # Q5 = Human

        # Ajouter le nom de la personne
        if row['personLabel']:
            g.add((person_uri, FOAF.name, Literal(row['personLabel'])))

        # Ajouter la date de naissance
        if row['birthDate']:
            g.add((person_uri, SCHEMA.birthDate, Literal(row['birthDate'], datatype=XSD.date)))

        # Ajouter le parti politique (si existant)
        if row['party']:
            party_uri = URIRef(row['party'])
            g.add((person_uri, WDT['P102'], party_uri))
            if row['partyLabel']:
                g.add((party_uri, RDFS.label, Literal(row['partyLabel'])))

        # Ajouter le canton (si existant)
        if row['canton']:
            canton_uri = URIRef(row['canton'])
            g.add((person_uri, WDT['P768'], canton_uri))
            if row['cantonLabel']:
                g.add((canton_uri, RDFS.label, Literal(row['cantonLabel'])))

# Sauvegarder le graphe RDF au format Turtle
output_file = 'conseillers.ttl'
g.serialize(destination=output_file, format='turtle')

print(f"Conversion terminée. Fichier RDF généré : {output_file}")
