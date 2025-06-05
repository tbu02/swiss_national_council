## Exploration de Wikidata

Dans ce notebook, nous explorons et documentons différente reqête.


### Exploration des "occupations" et des "fields of work"


```sparql
### List 'n' more frequent occupations

PREFIX wd: <http://www.wikidata.org/entity/>


SELECT ?occupation ?occupationLabel ?n
WHERE {

    {
    SELECT ?occupation (COUNT(*) as ?n)
    WHERE {
        ?item wdt:P106 ?occupation.
        }
    GROUP BY ?occupation 
    ORDER BY DESC(?n)

    #OFFSET 20
    LIMIT 20
    }

    SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
    
    }
    ORDER BY DESC(?n)
```

```sparql
### List more frequent occupations

PREFIX wd: <http://www.wikidata.org/entity/>

SELECT ?field ?fieldLabel ?n
WHERE {

    {
    SELECT ?field (COUNT(*) as ?n)
    WHERE {
        ?item wdt:P101 ?field.
        }
    GROUP BY ?field 
    ORDER BY DESC(?n)

    #OFFSET 20
    LIMIT 20
    }

    SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
    
    }
    ORDER BY DESC(?n)
```
## Exploration des politiciens et relatifs

```sparql
   ## Count and inspect occupations and fields of work
   SELECT (COUNT(*) as ?eff)
    WHERE {
        {
        ?item wdt:P106 wd:Q82955  # politician 82955
        }
        UNION
        {
        ?item wdt:P101 wd:Q7163     # politics
        }

    ?item wdt:P31 wd:Q5  # Any instance of a human.
SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } 

    }  
ORDER BY DESC(?n)

```
## Les politiciens suisses

```sparql
### Swiss politician
SELECT (count(*) as ?number)
WHERE {
    {?item wdt:P106 wd:Q82955}  # politician
    
    {?item wdt:P31 wd:Q5} # Any instance of a human.
    {?item wdt:P27 wd:Q39} # Any Country of citizenship Switzerland.

}
ORDER BY DESC(?n)
```

```sparql
## Swiss politics
SELECT (count(*) as ?number)
WHERE {
    {?item wdt:P101 wd:Q7163}  # politics
    
    {?item wdt:P31 wd:Q5} # Any instance of a human.
    {?item wdt:P27 wd:Q39} # Any Country of citizenship Switzerland.

}
ORDER BY DESC(?n)
```
Cette requête indique qu'il n'y a pas beosin d'utiliser un champs (field)

```sparql
### Swiss politician
SELECT ?item ?itemLabel # (count(*) as ?number)
WHERE {
    {?item wdt:P106 wd:Q82955}  # politician
    
    {?item wdt:P31 wd:Q5} # Any instance of a human.
    {?item wdt:P27 wd:Q39} # Any Country of citizenship Switzerland.

SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } 

}
ORDER BY DESC(?n)
LIMIT 20            
```
## Les politiciens suisses du Conseil national

```sparql
### Swiss politician from the national council
SELECT (count(*) as ?number)
WHERE {
    {?item wdt:P106 wd:Q82955}  # politician
    {?item wdt:P31 wd:Q5} # Any instance of a human.
    {?item wdt:P27 wd:Q39} # Any Country of citizenship Switzerland.
    {?item wdt:P39 wd:Q18510612} # Any Position held Member of the Swiss National Council

SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } 

}
ORDER BY DESC(?n)         
```

```sparql
### Swiss politician from the national council
SELECT ?item ?itemLabel # (count(*) as ?number)
WHERE {
    {?item wdt:P106 wd:Q82955}  # politician
    {?item wdt:P31 wd:Q5} # Any instance of a human.
    {?item wdt:P27 wd:Q39} # Any Country of citizenship Switzerland.
    {?item wdt:P39 wd:Q18510612} # Any Position held Member of the Swiss National Council

SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } 

}
ORDER BY DESC(?n)
LIMIT 20
```
## Les politiciens suisses du Conseil national depuis 2003

```sparql
### Swiss politician from the national council since 2003
SELECT (COUNT(*) AS ?number)
WHERE {
    ?item wdt:P106 wd:Q82955 .          # Profession: Politician
    ?item wdt:P31 wd:Q5 .               # Instance of: Human
    ?item wdt:P27 wd:Q39 .              # Citizenship: Switzerland
    ?item p:P39 ?mandatStatement .      # Statement about a position held
    ?mandatStatement ps:P39 wd:Q18510612 .   # Position held: Member of Swiss National Council
    OPTIONAL { ?mandatStatement pq:P580 ?start . }  # Start time of the mandate

    FILTER(BOUND(?start) && YEAR(?start) > 2003)

    SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}

ORDER BY DESC(?n)
```

```sparql
SELECT ?item ?itemLabel
WHERE {
    ?item wdt:P106 wd:Q82955 .          # Profession: Politician
    ?item wdt:P31 wd:Q5 .               # Instance of: Human
    ?item wdt:P27 wd:Q39 .              # Citizenship: Switzerland
    ?item p:P39 ?mandatStatement .      # Statement about a position held
    ?mandatStatement ps:P39 wd:Q18510612 .   # Position held: Member of Swiss National Council
    OPTIONAL { ?mandatStatement pq:P580 ?start . }  # Start time of the mandate

    FILTER(BOUND(?start) && YEAR(?start) > 2003)

    SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
ORDER BY DESC(?n)
Limit 20
```
## Inclure les réélus pour 2003

```sparql
### Swiss politician from the national council since 2003, including re-elected politicians
SELECT (COUNT(*) AS ?number)
WHERE {
    ?item wdt:P106 wd:Q82955 .          # Profession: Politician
    ?item wdt:P31 wd:Q5 .               # Instance of: Human
    ?item wdt:P27 wd:Q39 .              # Citizenship: Switzerland
    ?item p:P39 ?mandatStatement .      # Statement about a position held
    ?mandatStatement ps:P39 wd:Q18510612 .   # Position held: Member of Swiss National Council
    
    # Get the start time of the mandate
    OPTIONAL { ?mandatStatement pq:P580 ?start . }
    
    # Filter for mandates that started after 2003
    FILTER(BOUND(?start) && YEAR(?start) > 2003)

    # If no start time, allow previous mandates (before 2003) that are still active after 2003
    OPTIONAL {
        ?item p:P39 ?reElectionStatement .
        ?reElectionStatement ps:P39 wd:Q18510612 .
        ?reElectionStatement pq:P580 ?reElectionStart .
        FILTER(YEAR(?reElectionStart) > 2003)
    }
    
    SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
```
Nouveau test 1 (pas concluant) :

```sparql
SELECT (count(*) as ?number)
    WHERE {
      {?item wdt:P106 wd:Q82955}  # Politician
      ?item wdt:P31 wd:Q5 .        # Any instance of a human
      ?item wdt:P27 wd:Q39 .       # Any country of citizenship: Switzerland
      ?item p:P39 ?mandatStatement .  # Position held: Member of the Swiss National Council
      ?mandatStatement ps:P39 wd:Q18510612 .  # Member of Swiss National Council
      
      # Get start time of the mandate
      OPTIONAL { ?mandatStatement pq:P580 ?start . }
      
      # Extract the year from the start date and filter for those after 2003
      BIND(REPLACE(str(?start), "(.*)([0-9]{4})(.*)", "$2") AS ?year)
      FILTER(xsd:integer(?year) > 2003)

      
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en", "fr", "de-ch". }
    }
```
Nouveau test 2 (concluant, mais pas satisfaisant):

```sparql
SELECT (COUNT(*) AS ?number)
WHERE {
    {?item wdt:P106 wd:Q82955}          # Profession: Politician
    ?item wdt:P31 wd:Q5 .               # Instance of: Human
    ?item wdt:P27 wd:Q39 .              # Citizenship: Switzerland
    ?item p:P39 ?mandatStatement .      # Statement about a position held
    ?mandatStatement ps:P39 wd:Q18510612 .   # Position held: Member of Swiss National Council
    
    # Get the start time of the mandate
    OPTIONAL { ?mandatStatement pq:P580 ?start . }
    
    # Filter for mandates that started after 2003
    FILTER(BOUND(?start) && xsd:dateTime(?start) >= "2003-01-01T00:00:00Z"^^xsd:dateTime)

    # If no start time, allow previous mandates (before 2003) that are still active after 2003
    OPTIONAL {
        ?item p:P39 ?reElectionStatement .
        ?reElectionStatement ps:P39 wd:Q18510612 .
        ?reElectionStatement pq:P580 ?reElectionStart .
        FILTER(xsd:dateTime(?reElectionStart) >= "2003-01-01T00:00:00Z"^^xsd:dateTime)
    }

    SERVICE wikibase:label { bd:serviceParam wikibase:language "en" . }
}
```
Cette manière de filtrer ne fonctionne pas correctement... Donc je filtre avec l'âge des parlementaires. lors de la législature 47 (2003 à 2007), l'élu le plus âgé est né en 1934. Filtrons donc en 1934.

```sparql
### Swiss politician from the national council born after 1934
SELECT (count(*) as ?number)
WHERE {
    {?item wdt:P106 wd:Q82955}  # politician
    {?item wdt:P31 wd:Q5} # Any instance of a human.
    {?item wdt:P27 wd:Q39} # Any Country of citizenship Switzerland.
    {?item wdt:P39 wd:Q18510612} # Any Position held Member of the Swiss National Council
    {?item wdt:P569 ?birthDate}
    

    BIND(REPLACE(str(?birthDate), "(.*)([0-9]{4})(.*)", "$2") AS ?year)
    FILTER(xsd:integer(?year) >= 1934 )

SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } 

}
ORDER BY DESC(?n)
# LIMIT 20
```
Avec un résultat de 822, le résultat est déjà plus satisfaisant. Je vais donc utiliser ce filtre.
## Nombre de propriété dans la population

```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX bd: <http://www.bigdata.com/rdf#>

SELECT ?p ?propLabel ?eff
WHERE {
{
SELECT ?p  (count(*) as ?eff)
WHERE {
    {?item wdt:P106 wd:Q82955}  # politician
    {?item wdt:P31 wd:Q5} # Any instance of a human.
    {?item wdt:P27 wd:Q39} # Any Country of citizenship Switzerland.
    {?item wdt:P39 wd:Q18510612} # Any Position held Member of the Swiss National Council
    {?item wdt:P569 ?birthDate}
    
?item  ?p ?o.

    BIND(REPLACE(str(?birthDate), "(.*)([0-9]{4})(.*)", "$2") AS ?year)
    FILTER(xsd:integer(?year) >= 1934 )

}
GROUP BY ?p 

    }

# get the original property (in the the statement construct)     
?prop wikibase:directClaim ?p .

SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } 


}  
ORDER BY DESC(?eff)
#LIMIT 20


```
## Même opération, mais en limitant moins la recherche
Afin d'avoir plus que 823 résulatas, je vais supprimer la requête de membre du Conseil national. Ce qui permettra également d'avoir une répartition binaire entre deux sous-population.

```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX bd: <http://www.bigdata.com/rdf#>

SELECT ?p ?propLabel ?eff
WHERE {
{
SELECT ?p  (count(*) as ?eff)
WHERE {
    {?item wdt:P106 wd:Q82955}  # politician
    {?item wdt:P31 wd:Q5} # Any instance of a human.
    {?item wdt:P27 wd:Q39} # Any Country of citizenship Switzerland.
    {?item wdt:P569 ?birthDate}
    
?item  ?p ?o.

    BIND(REPLACE(str(?birthDate), "(.*)([0-9]{4})(.*)", "$2") AS ?year)
    FILTER(xsd:integer(?year) >= 1934 )

}
GROUP BY ?p 

    }

# get the original property (in the the statement construct)     
?prop wikibase:directClaim ?p .

SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } 


}  
ORDER BY DESC(?eff)
#LIMIT 20
```
## Exploration finale
Finalement, en se rendant compte des limites de cette population et en discutant avec le professeur, il a été décidé de rattiser large en englobant tous les élus du conseil national.

```sparql
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX bd: <http://www.bigdata.com/rdf#>

SELECT ?p ?propLabel ?eff
WHERE {
{
SELECT ?p  (count(*) as ?eff)
WHERE {
    {?item wdt:P106 wd:Q82955}  # politician
    {?item wdt:P31 wd:Q5} # Any instance of a human.
    {?item wdt:P27 wd:Q39} # Any Country of citizenship Switzerland.
    {?item wdt:P569 ?birthDate}
    
?item  ?p ?o.

    BIND(REPLACE(str(?birthDate), "(.*)([0-9]{4})(.*)", "$2") AS ?year)
    FILTER(xsd:integer(?year) >= 1934 )

}
GROUP BY ?p 

    }

# get the original property (in the the statement construct)     
?prop wikibase:directClaim ?p .

SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } 


}  
ORDER BY DESC(?eff)
```
C'est donc ce code qui fera foi. Retrouvez une liste des informations disponibles dans Wikidata [ici](https://github.com/tbu02/swiss_national_council/blob/main/Wikidata/wdt_person_prorpieties_20250605.csv).
