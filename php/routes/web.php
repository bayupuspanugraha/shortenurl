<?php

use App\Http\Controllers\ShorturlController;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/', [ShorturlController::class, 'index']);
Route::get('/info', [ShorturlController::class, 'info']);
Route::get('/go/{id}', [ShorturlController::class, 'go']);
Route::post('/shortenurl', [ShorturlController::class, 'shortenurl']);
