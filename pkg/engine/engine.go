package engine

import (
	"fmt"

	"github.com/blevesearch/bleve/v2"
	"github.com/google/uuid"
)

func AddToIndex(d interface{}) {
	index, err := bleve.Open("index")
	if err != nil {
		mapping := bleve.NewIndexMapping()
		index, err = bleve.New("index", mapping)
		if err != nil {
			fmt.Println("Failed to create index:", err)
			return
		}
	}

	id := uuid.New().String()
	err = index.Index(id, d)
	if err != nil {
		fmt.Println("Failed to index document:", err)
		return
	}

	fmt.Println("Document indexed successfully")
}

func Search(query string) *bleve.SearchResult {
	index, err := bleve.Open("index")
	if err != nil {
		fmt.Println("Failed to open index:", err)
		return nil
	}

	searchRequest := bleve.NewSearchRequest(bleve.NewQueryStringQuery(query))
	searchResult, err := index.Search(searchRequest)
	if err != nil {
		fmt.Println("Failed to execute search:", err)
		return nil
	}

	fmt.Println("Search results:")
	for _, hit := range searchResult.Hits {
		fmt.Println("ID:", hit.ID)
		fmt.Println("Score:", hit.Score)
		fmt.Println("Document:", hit.Fields)
		fmt.Println()
	}
	return searchResult
}
