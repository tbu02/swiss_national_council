## Importer dans Allegrograph
Dans ce dossier, je vais décrire les étapes de l'importation de données dans mon référentiel Allegrograph.

Tout d'abord, je vérifie les propriétés de base de la population : nom, sexe, année de naissance.

```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX bd: <http://www.bigdata.com/rdf#>

SELECT DISTINCT ?item ?itemLabel ?gender ?year 
WHERE {
   SERVICE <https://query.wikidata.org/sparql> {
  ?item wdt:P106 wd:Q82955;           # profession: politician
        wdt:P31 wd:Q5;                # instance of: human
        wdt:P27 wd:Q39;               # country of citizenship: Switzerland
        wdt:P39 wd:Q18510612;         # position held: Member of the Swiss National Council
        wdt:P569 ?birthDate;          # date of birth
        wdt:P21 ?gender.              # gender

  BIND(year(?birthDate) AS ?year)
  BIND ( ?itemLabel as ?itemLabel)
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
}
LIMIT 10
```
## Préparation pour l'importation
Utilisation de la requête CONSTRUCT pour préparer les triplets à l'importation dans un graphe

```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX bd: <http://www.bigdata.com/rdf#>

CONSTRUCT 
        {?item  rdfs:label ?itemLabel.
           ?item wdt:P21 ?gender.
           ?item wdt:P569 ?year.
           ?item  rdf:type wd:Q5. }
        
        WHERE {

        SERVICE <https://query.wikidata.org/sparql>
            {
  ?item wdt:P106 wd:Q82955;           # profession: politician
        wdt:P31 wd:Q5;                # instance of: human
        wdt:P27 wd:Q39;               # country of citizenship: Switzerland
        wdt:P39 wd:Q18510612;         # position held: Member of the Swiss National Council
        wdt:P569 ?birthDate;          # date of birth
        wdt:P21 ?gender.              # gender

  BIND(year(?birthDate) AS ?year)
  BIND ( ?itemLabel as ?itemLabel)
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
        }
        LIMIT 5
```
## Importation des triplets dans un graphe dédié

```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX bd: <http://www.bigdata.com/rdf#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

INSERT {

        GRAPH <https://github.com/tbu02/swiss_national_council/blob/main/Graphiques/wikidata_imported_data.md>
        {?item  rdfs:label ?itemLabel.
           ?item wdt:P21 ?gender.
           ?item wdt:P569 ?year. 
           ?item  rdf:type wd:Q5.
           }
}
        
                WHERE {

        SERVICE <https://query.wikidata.org/sparql>
            {
  ?item wdt:P106 wd:Q82955;           # profession: politician
        wdt:P31 wd:Q5;                # instance of: human
        wdt:P27 wd:Q39;               # country of citizenship: Switzerland
        wdt:P39 wd:Q18510612;         # position held: Member of the Swiss National Council
        wdt:P569 ?birthDate;          # date of birth
        wdt:P21 ?gender.              # gender

  BIND(year(?birthDate) AS ?year)
  BIND ( ?itemLabel as ?itemLabel)
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
            }
                }
    
```
### Ajout du label "Person"

```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

INSERT DATA {
    GRAPH <https://github.com/tbu02/swiss_national_council/blob/main/Graphiques/wikidata_imported_data.md>
    {
        wd:Q5 rdfs:label "Person".
    }
}
```
### Ajout du genre

```sparql
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX bd: <http://www.bigdata.com/rdf#>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>

SELECT (COUNT(*) as ?n)
WHERE
   {
   SELECT DISTINCT ?gender
   WHERE {
      GRAPH <https://github.com/tbu02/swiss_national_council/blob/main/Graphiques/wikidata_imported_data.md>
         {
            ?s wdt:P21 ?gender.
         }
      }
   }
```

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>

WITH <https://github.com/tbu02/swiss_national_council/blob/main/Graphiques/wikidata_imported_data.md>
INSERT {
   ?gender rdf:type wd:Q48264.
}
WHERE
   {
   SELECT DISTINCT ?gender
   WHERE {
         {
            ?s wdt:P21 ?gender.
         }
      }
   }
```

```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

INSERT DATA {
    GRAPH <https://github.com/tbu02/swiss_national_council/blob/main/Graphiques/wikidata_imported_data.md>
    {
        wd:Q48264 rdfs:label "Gender Identity".
    }
}
```
### Vérification des triplets importés et ajout des labels de genre

```sparql
SELECT (COUNT(*) as ?n)
WHERE {
    GRAPH <https://github.com/tbu02/swiss_national_council/blob/main/Graphiques/wikidata_imported_data.md>
        {?s ?p ?o}
}
```

```sparql
SELECT (COUNT(*) as ?n)
WHERE {
    GRAPH <https://github.com/tbu02/swiss_national_council/blob/main/Graphiques/wikidata_imported_data.md>
        {?s rdf:label ?o}
}
GROUP BY ?s
HAVING (?n > 1)
```
### Exploration du genre

```sparql
REFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>

SELECT ?s (COUNT(*) as ?n)
WHERE {
    GRAPH <https://github.com/tbu02/swiss_national_council/blob/main/Graphiques/wikidata_imported_data.md>
        {?s wdt:P21 ?gen}
}
GROUP BY ?s
HAVING (?n > 1)
```

```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>

SELECT ?gen (COUNT(*) as ?n)
WHERE {
    GRAPH <https://github.com/tbu02/swiss_national_council/blob/main/Graphiques/wikidata_imported_data.md>
        {?s wdt:P21 ?gen}
}
GROUP BY ?gen
```

```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>

SELECT ?gen (COUNT(*) as ?n)
WHERE {
    GRAPH <https://github.com/tbu02/swiss_national_council/blob/main/Graphiques/wikidata_imported_data.md>
        {?s wdt:P21 ?gen;
            wdt:P569 ?birthDate.
        FILTER (?birthDate < '1900')     
          }
}
GROUP BY ?gen
```

```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX bd: <http://www.bigdata.com/rdf#>

SELECT ?gen ?genLabel
WHERE {

    

    {SELECT DISTINCT ?gen
    WHERE {
        GRAPH <https://github.com/tbu02/swiss_national_council/blob/main/Graphiques/wikidata_imported_data.md>    
            {?s wdt:P21 ?gen}
    }
    }   

    SERVICE  <https://query.wikidata.org/sparql> {
        ## Add this clause in order to fill the variable      
        BIND(?gen as ?gen)
        BIND ( ?genLabel as ?genLabel)
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }  
    }
}
```

```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX bd: <http://www.bigdata.com/rdf#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

CONSTRUCT {
     ?gen rdfs:label ?genLabel
    
} 
WHERE {

    

    {SELECT DISTINCT ?gen
    WHERE {
        GRAPH <https://github.com/tbu02/swiss_national_council/blob/main/Graphiques/wikidata_imported_data.md>    
            {?s wdt:P21 ?gen}
    }
    }   

    SERVICE  <https://query.wikidata.org/sparql> {
        ## Add this clause in order to fill the variable      
        BIND(?gen as ?gen)
        BIND ( ?genLabel as ?genLabel)
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }  
    }
}
```

```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX bd: <http://www.bigdata.com/rdf#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

WITH <https://github.com/tbu02/swiss_national_council/blob/main/Graphiques/wikidata_imported_data.md> 
INSERT {
     ?gen rdfs:label ?genLabel
    
} 
WHERE {    

    {SELECT DISTINCT ?gen
    WHERE {
        GRAPH <https://github.com/tbu02/swiss_national_council/blob/main/Graphiques/wikidata_imported_data.md>    
            {?s wdt:P21 ?gen}
    }
    }   

    SERVICE  <https://query.wikidata.org/sparql> {
        ## Add this clause in order to fill the variable      
        BIND(?gen as ?gen)
        BIND ( ?genLabel as ?genLabel)
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }  
    }
}
```

```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX bd: <http://www.bigdata.com/rdf#>

SELECT ?gen ?genLabel ?n
WHERE
{
    {
    SELECT ?gen (COUNT(*) as ?n)
        WHERE {
            GRAPH <https://github.com/tbu02/swiss_national_council/blob/main/Graphiques/wikidata_imported_data.md>  
                    {
            ?s wdt:P21 ?gen.
            }
        }    
        GROUP BY ?gen        
    }    
    ?gen rdfs:label ?genLabel
    }   
```
## Préparation des données pour l'analyse

```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>


SELECT ?s ?label ?birthDate ?genLabel
WHERE {
    GRAPH <https://github.com/tbu02/swiss_national_council/blob/main/Graphiques/wikidata_imported_data.md>
        {
            ## A property path passes through 
            # two or more properties
            ?s wdt:P21 / rdfs:label ?genLabel;
            rdfs:label ?label;
            wdt:P569 ?birthDate.
          }
}
ORDER BY ?birthDate
LIMIT 10
```

```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT (COUNT(*) as ?n)
WHERE {
    GRAPH <https://github.com/tbu02/swiss_national_council/blob/main/Graphiques/wikidata_imported_data.md>
        {
          # ?s wdt:P31 wd:Q5 
          ?s a wd:Q5
          }
}
```

```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>


SELECT  ?s (MAX(?label) as ?label) (xsd:integer(MAX(?birthDate)) as ?birthDate) 
    (MAX(?gen) as ?gen) (MAX(?genLabel) AS ?genLabel)
WHERE {
    GRAPH <https://github.com/tbu02/swiss_national_council/blob/main/Graphiques/wikidata_imported_data.md>
        {?s wdt:P21 ?gen;
            rdfs:label ?label;
            wdt:P569 ?birthDate.
        ?gen rdfs:label ?genLabel    
          }
}
GROUP BY ?s
LIMIT 10
```

```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT (COUNT(*) as ?n)
WHERE {
SELECT  ?s (MAX(?label) as ?label) (xsd:integer(MAX(?birthDate)) as ?birthDate) 
            (MAX(?gen) as ?gen) (MAX(?genLabel) AS ?genLabel)
WHERE {
    GRAPH <https://github.com/tbu02/swiss_national_council/blob/main/Graphiques/wikidata_imported_data.md>
        {?s wdt:P21 ?gen;
            rdfs:label ?label;
            wdt:P569 ?birthDate.
          }
}
GROUP BY ?s
}
```

```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

INSERT DATA {
GRAPH <https://github.com/tbu02/swiss_national_council/blob/main/Graphiques/wikidata_imported_data.md>
{    wdt:P569 rdfs:label "date of birth"
}    
}

```

```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

INSERT DATA {
GRAPH <https://github.com/tbu02/swiss_national_council/blob/main/Graphiques/wikidata_imported_data.md>
{    wdt:P21 rdfs:label "sex or gender"
}    
}

```
