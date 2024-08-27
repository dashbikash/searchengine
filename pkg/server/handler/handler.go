package handler

import (
	"encoding/json"

	"github.com/dashbikash/embedded-search/pkg/engine"
	"github.com/gofiber/fiber/v2"
)

func Index(c *fiber.Ctx) error {
	return c.SendString("Welcome to Embedded Search Engine!")
}

func Search(c *fiber.Ctx) error {
	// Get the search query from the request parameters
	query := c.Query("q")

	jsonResult, _ := json.Marshal(engine.Search(query))
	return c.Send(jsonResult)
}
func AddIndex(c *fiber.Ctx) error {
	// Get the index data from the request body
	indexData := c.Body()

	// Add the index data to the search engine index

	// Return a success response
	return c.SendString(string(indexData))
}
