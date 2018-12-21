process data as follows

``` 
python parseMAF.py > genenames.txt
```

- kegg enrichment

```
Rscript kegg_enrich.R
Rscript kegg_enrich_dotplot.R
```

- go enrichment

```
Rscript enrich_GO.R
```
