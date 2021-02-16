package com.bayunugraha.shortenerurl.controller;

import com.aventrix.jnanoid.jnanoid.NanoIdUtils;
import com.bayunugraha.shortenerurl.model.ShortenUrl;
import com.bayunugraha.shortenerurl.viewmodel.GenerateUrlViewModel;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.net.URI;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import com.bayunugraha.shortenerurl.repository.ShortenUrlRepository;

@RestController
@RequestMapping("/")
public class ShortenerUrlController {

    @Autowired
    private ShortenUrlRepository _shortenUrlRepo;

    final String _baseURL = "http://localhost:4545";

    @GetMapping()
    public ResponseEntity<ArrayList<HashMap<String, String>>> Index()
    {
        ArrayList<HashMap<String, String>> response = new ArrayList<HashMap<String, String>>();
        response.add(new HashMap<String, String>() {{
            put("url", "/info");
            put("method", "GET");
            put("params", "");
            put("body", "");
            put("desc", "Shows all data from database");
        }});
        response.add(new HashMap<String, String>() {{
            put("url", "/shortenurl");
            put("method", "POST");
            put("params", "");
            put("body", "{url: \"YOUR_STRING_URL\"}");
            put("desc", "Generates new short url from original url");
        }});
        response.add(new HashMap<String, String>() {{
            put("url", "/go/:id");
            put("method", "GET");
            put("params", ":id => the shorten url id");
            put("body", "");
            put("desc", "Access your ORIGINAL Url and redirect to the page");
        }});

        return new ResponseEntity<ArrayList<HashMap<String, String>>>(response, HttpStatus.OK);
    }

    @GetMapping("/info")
    public ResponseEntity<ArrayList<HashMap<String, String>>> Info()
    {
        List<ShortenUrl> resultList = _shortenUrlRepo.findAll();
        ArrayList<HashMap<String, String>> response = new ArrayList<HashMap<String, String>>();

        for(ShortenUrl url: resultList) {
            response.add(new HashMap<String, String>() {{
                put("originalURL", url.getOriginalURL());
                put("shortURL", _baseURL + "/go/" + url.getId());
            }});
        }

        return new ResponseEntity<ArrayList<HashMap<String, String>>>(response, HttpStatus.OK);
    }

    @GetMapping("/go/{id}")
    public ResponseEntity<HashMap<String, String>> Go(@PathVariable String id)
    {
        return this._shortenUrlRepo.findById(id).map(data -> {
            HttpHeaders httpHeaders = new HttpHeaders();
            httpHeaders.setLocation(URI.create(data.getOriginalURL()));
            return new ResponseEntity<HashMap<String, String>>(httpHeaders, HttpStatus.SEE_OTHER);
        })
        .orElseGet(() -> new ResponseEntity<HashMap<String, String>>(new HashMap<String, String>() {{
            put("message", "NOT-FOUND");
        }}, HttpStatus.NOT_FOUND));
    }

    @PostMapping("/shortenurl")
    public ResponseEntity<HashMap<String, String>> ShortenUrl(@RequestBody GenerateUrlViewModel request)
    {
        if(request == null || request.getUrl() == null || request.getUrl() == "") {
            return new ResponseEntity<HashMap<String, String>>(new HashMap<String, String>() {{
                put("message", "BAD-REQUEST");
            }}, HttpStatus.BAD_REQUEST);
        }

        String id = NanoIdUtils.randomNanoId(NanoIdUtils.DEFAULT_NUMBER_GENERATOR, NanoIdUtils.DEFAULT_ALPHABET, 10);
        ShortenUrl model = new ShortenUrl(id, request.getUrl());
        this._shortenUrlRepo.save(model);

        return new ResponseEntity<HashMap<String, String>>( new HashMap<String, String>(){{
            put("originalURL", request.getUrl());
            put("shortURL", _baseURL + "/go/" + id);
        }}, HttpStatus.OK);
    }
}
