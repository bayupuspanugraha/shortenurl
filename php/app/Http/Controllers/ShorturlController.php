<?php

namespace App\Http\Controllers;

use App\Models\Shorturl;
use Illuminate\Http\Request;
use Mockery\Undefined;
use Hidehalo\Nanoid\Client;

class ShorturlController extends Controller
{
    private $baseURL = 'http://localhost:4545';

    function index()
    {
        return response()->json([
            [
                'url' => '/info',
                'method' => 'GET',
                'params' => '',
                'body' => '',
                'desc' => 'Shows all data from database'
            ],
            [
                'url' => '/shortenurl',
                'method' => 'POST',
                'params' => '',
                'body' => '{url: "YOUR_STRING_URL"}',
                'desc' => 'Generates new short url from original url'
            ],
            [
                'url' => '/go/:id',
                'method' => 'GET',
                'params' => ':id => the shorten url id',
                'body' => '',
                'desc' => 'Access your ORIGINAL Url and redirect to the page'
            ]
        ], 200, ['Content-Type' => 'application/json']);
    }

    function info()
    {
        $shortUrls = ShortUrl::all();
        $results = [];
        foreach ($shortUrls as $url) {
            array_push($results, [
                'originalURL' => $url->originalURL,
                'shortURL' => $this->baseURL . '/go/' . $url->id,
            ]);
        }
        return response()->json($results, 200, ['Content-Type' => 'application/json']);
    }

    function shortenurl()
    {
        if (!isset(request()->all()['url'])) {
            return response()->json([
                'message' => 'Bad Request'
            ], 400, ['Content-Type' => 'application/json']);
        }

        $client = new Client();
        $url = request()->all()['url'];
        $newData = new Shorturl();
        $newData->id = $client->generateId($size = 10, $mode = Client::MODE_DYNAMIC);
        $newData->originalURL = $url;

        $newData->save();

        return response()->json([
            'originalURL' => $url,
            'shortURL' => $this->baseURL . '/go/' . $newData->id
        ], 200, ['Content-Type' => 'application/json']);
    }

    function go(string $id)
    {
        $target = Shorturl::where('id', $id)->first();
        if ($target == null) {
            return response()->json([
                "message" => "Data was not found"
            ], 404, ['Content-Type' => 'application/json']);
        }

        return redirect($target->originalURL);
    }
}
