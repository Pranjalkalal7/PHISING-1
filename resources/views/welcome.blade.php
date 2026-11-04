<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="csrf-token" content="{{ csrf_token() }}">
    <title>PhishGuard - Cybersecurity Awareness Training</title>
    <link rel="stylesheet" href="{{ asset('app.css') }}">
</head>
<body>
    <noscript>
        <main class="noscript">
            <h1>PhishGuard requires JavaScript</h1>
            <p>This local educational simulator runs entirely in your browser and stores only training progress in LocalStorage.</p>
        </main>
    </noscript>
    <div id="app" data-scenario-source="{{ asset('data/scenarios.json') }}"></div>
    <script type="module" src="{{ asset('app.js') }}"></script>
</body>
</html>
