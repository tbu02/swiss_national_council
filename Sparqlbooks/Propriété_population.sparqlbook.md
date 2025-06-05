## Nombre de propriété pour la population

Ici, on va voir combien de propriété il existe pour ma population, à savoir les conseillers nationaux. Retrouvez une liste des informations disponibles dans Wikidata [ici](https://github.com/tbu02/swiss_national_council/blob/main/Wikidata/wdt_person_prorpieties_20250605.csv).

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
      {?item wdt:P106 wd:Q82955}  # Politician
      UNION
      {?item wdt:P101 wd:Q7163}     # Politics

      ?item wdt:P31 wd:Q5 .        # Any instance of a human
      ?item wdt:P27 wd:Q39 .       # Any country of citizenship: Switzerland
      ?item p:P39 ?mandatStatement .  # Position held: Member of the Swiss National Council
      ?mandatStatement ps:P39 wd:Q18510612 .  # Member of Swiss National Council

      ?item ?p ?o .  # Query properties of the item
      
    }
    GROUP BY ?p
  }
  
  # Get the original property (in the statement construct)
  ?prop wikibase:directClaim ?p .

  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
ORDER BY DESC(?eff)
LIMIT 20
```
