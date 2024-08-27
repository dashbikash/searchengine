package main

import (
	"github.com/dashbikash/embedded-search/pkg/server/handler"
	"github.com/gofiber/fiber/v2"
)

func main() {
	app := fiber.New()

	app.Get("/", handler.Index)
	app.Get("/search", handler.Search)
	app.Post("/index", handler.AddIndex)

	app.Listen(":3000")
}
