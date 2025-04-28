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
