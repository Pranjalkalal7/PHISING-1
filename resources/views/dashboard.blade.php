@extends('layouts.app')

@section('content')
    <div class="container">
        <h1>PhishGuard</h1>
        <p>This project now runs as a safe browser-based training simulator. No credential, IP address, or user-agent phishing logs are collected.</p>
        <p><a href="{{ url('/') }}">Open the simulator</a></p>
    </div>
@endsection
