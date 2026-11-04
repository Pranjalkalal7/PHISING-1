<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class PhishingController extends Controller
{
    public function showLoginPage(){
        return view('phishing.facebook');
    }

    public function blockedSubmission(Request $request){
        return back()->with('simulation_warning', 'Stop! This is a training simulation. Credentials are never collected, stored, logged, or forwarded.');
    }
}
