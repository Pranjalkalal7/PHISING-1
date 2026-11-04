@extends('layouts.app')

@section('content')
    <div class="container">
        <h1>Campaigns Disabled</h1>
        <p>PhishGuard is a contained training simulator. It does not create or send phishing campaigns.</p>
        <p><a href="{{ url('/simulation') }}">Open simulation training</a></p>
    </div>
@endsection
