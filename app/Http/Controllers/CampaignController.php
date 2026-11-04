<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class CampaignController extends Controller
{
    public function index(){
        return view('welcome');
    }

    public function create(){
        return view('welcome');
    }

    public function store(Request $request){
        return redirect('/')->with('simulation_warning', 'Real phishing campaigns are disabled. Use the local PhishGuard simulator instead.');
    }

}
