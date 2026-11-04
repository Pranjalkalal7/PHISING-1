<?php

use App\Http\Controllers\PhishingController;
use Illuminate\Support\Facades\Route;

Route::view('/', 'welcome');

Route::get('/facebook-login', [PhishingController::class, 'showLoginPage'])->name('phishing.login');
Route::post('/facebook-login', [PhishingController::class, 'blockedSubmission'])->name('phishing.capture');

Route::view('/{path}', 'welcome')->where('path', '.*');
