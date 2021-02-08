package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"

	httprouter "github.com/julienschmidt/httprouter"
	gonanoid "github.com/matoous/go-nanoid/v2"
	_ "github.com/mattn/go-sqlite3"
)

func init() {
	if !fileExists("./app.db") {
		file, err := os.Create("app.db") // Create SQLite file
		if err != nil {
			log.Fatal(err.Error())
		}
		file.Close()
		log.Println("app.db created")
	}

	db, _ := sql.Open("sqlite3", "./app.db")
	defer db.Close()
	statement, _ := db.Prepare("CREATE TABLE IF NOT EXISTS shorturl(id text not null primary key, originalURL text not null)")
	statement.Exec()
}

func fileExists(filename string) bool {
	info, err := os.Stat(filename)
	if os.IsNotExist(err) {
		return false
	}
	return !info.IsDir()
}

func indexHandler(w http.ResponseWriter, r *http.Request, params httprouter.Params) {
	response := Response{
		Message: "Welcome to shorten url api",
		Data: []URLInfo{
			{
				URL:    "/info",
				Method: "GET",
				Params: "",
				Body:   "",
				Desc:   "Shows all data from database",
			},
			{
				URL:    "/shortenurl",
				Method: "POST",
				Params: "",
				Body:   "{url: 'YOUR_STRING_URL'}",
				Desc:   "Generates new short url from original url",
			},
			{
				URL:    "/go/:id",
				Method: "GET",
				Params: ":id => the shorten url id",
				Body:   "",
				Desc:   "Access your ORIGINAL Url and redirect to the page",
			},
		},
	}

	setResponse(w, response)
}

func ping(w http.ResponseWriter, r *http.Request, params httprouter.Params) {
	w.Write([]byte("[shorturl]: I am Listening..."))
}

func infoHandler(w http.ResponseWriter, r *http.Request, params httprouter.Params) {
	db, _ := sql.Open("sqlite3", "./app.db")
	defer db.Close()
	rows, err := db.Query("SELECT * FROM shorturl")
	if err != nil {
		panic(err)
	}
	defer rows.Close()

	var shortUrls []interface{}

	for rows.Next() {
		var shortUrl ShortUrl
		err := rows.Scan(&shortUrl.ID, &shortUrl.OriginalURL)
		if err != nil {
			panic(err)
		}

		shortUrls = append(shortUrls, map[string]string{
			"originalURL": shortUrl.OriginalURL,
			"shortURL":    fmt.Sprintf("%v/go/%v", baseURL, shortUrl.ID),
		})
	}

	response := Response{
		Message: "Found Data",
		Data:    shortUrls,
	}

	setResponse(w, response)
}

func goHandler(w http.ResponseWriter, r *http.Request, params httprouter.Params) {
	id := params.ByName("id")
	if id == "" {
		setResponse(w, "Invalid Params")
		return
	}

	db, _ := sql.Open("sqlite3", "./app.db")
	defer db.Close()
	rows, err := db.Query(fmt.Sprintf("SELECT * FROM shorturl WHERE id = '%v'", id))
	if err != nil {
		panic(err)
	}
	defer rows.Close()

	var shortUrl ShortUrl

	for rows.Next() {
		err := rows.Scan(&shortUrl.ID, &shortUrl.OriginalURL)
		if err != nil {
			panic(err)
		}
	}

	if shortUrl.ID == "" {
		setResponse(w, "Data was not found")
		return
	}

	http.Redirect(w, r, shortUrl.OriginalURL, http.StatusSeeOther)
}

func shortenURLHandler(w http.ResponseWriter, r *http.Request, params httprouter.Params) {
	var request ShortenURLRequest
	err := json.NewDecoder(r.Body).Decode(&request)
	if err != nil || request.URL == "" {
		setResponse(w, "Invalid Params")
		return
	}

	newID, _ := gonanoid.New(10)

	db, _ := sql.Open("sqlite3", "./app.db")
	defer db.Close()
	statement, err := db.Prepare("INSERT INTO shorturl(id, originalURL) VALUES (?, ?)")
	if err != nil {
		setResponse(w, "Failed to process your request")
		return
	}

	_, err = statement.Exec(newID, request.URL)
	if err != nil {
		setResponse(w, "Failed to process your request")
		return
	}

	response := Response{
		Data: map[string]string{
			"originalURL": request.URL,
			"shortURL":    fmt.Sprintf("%v/go/%v", baseURL, newID),
		},
	}

	setResponse(w, response)
}

func setResponse(w http.ResponseWriter, response interface{}) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func main() {
	router := httprouter.New()

	router.GET("/", indexHandler)
	router.GET("/ping", ping)
	router.GET("/go/:id", goHandler)
	router.POST("/shortenurl", shortenURLHandler)
	router.GET("/info", infoHandler)

	log.Fatal(http.ListenAndServe(":4545", router))
}
