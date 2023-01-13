package main

import (
	"fmt"
	"log"
	"net/http"
	"sync"
	"time"

	"github.com/gin-gonic/gin"
)

func main() {
	router := gin.Default()
	router.GET("/albums", getAlbums)
	router.GET("/albums/:id", getAlbumById)
	router.GET("/albumByName", getAlbumByName)
	router.POST("/albums", addAlbum)

	router.GET("/long_async", func(c *gin.Context) {
		var wg sync.WaitGroup
		wg.Add(1)
		// create copy to be used inside the goroutine
		cCp := c.Copy()
		ch := make(chan string)
		go func(ch chan string) {
			// simulate a long task with time.Sleep(). 5 seconds
			time.Sleep(2 * time.Second)

			// note that you are using the copied context "cCp", IMPORTANT
			log.Println("Done! in path " + cCp.Request.URL.Path)
			ch <- "world"
			close(ch)
		}(ch)
		wg.Done()
		m := <-ch
		log.Println(m)
		c.IndentedJSON(http.StatusAccepted, gin.H{"hello": m})
	})

	router.Run(":8080")
}

func getAlbums(c *gin.Context) {
	c.IndentedJSON(http.StatusOK, Albums)
}

func getAlbumById(c *gin.Context) {
	id := c.Param("id")
	for _, a := range Albums {
		if a.ID == id {
			c.IndentedJSON(http.StatusOK, a)
			return
		}
	}
	c.IndentedJSON(http.StatusNotFound, gin.H{"message": "album not found"})
}

func getAlbumByName(c *gin.Context) {
	var name AlbumName
	hi := c.Query("hi")
	fmt.Println(hi)
	if c.ShouldBind(&name) == nil {
		for _, a := range Albums {
			if a.Title == name.Name {
				c.IndentedJSON(http.StatusOK, a)
				return
			}
		}
	}
	c.IndentedJSON(http.StatusNotFound, gin.H{"message": "album not found"})
}

func addAlbum(c *gin.Context) {
	var newAlbum Album
	if err := c.BindJSON(&newAlbum); err != nil {
		return
	}
	Albums = append(Albums, newAlbum)
	c.IndentedJSON(http.StatusAccepted, newAlbum)
}
