package main

const port = ":4545"
const baseURL = "http://localhost" + port

type Response struct {
	Message string      `json:"message,omitempty"`
	Data    interface{} `json:"data,omitempty"`
}

type URLInfo struct {
	URL    string `json:"url"`
	Method string `json:"method"`
	Params string `json:"params"`
	Body   string `json:"body"`
	Desc   string `json:"desc"`
}

type ShortUrl struct {
	ID          string `json:"id"`
	OriginalURL string `json:"originalURL"`
}

type ShortenURLRequest struct {
	URL string `json: "url"`
}
