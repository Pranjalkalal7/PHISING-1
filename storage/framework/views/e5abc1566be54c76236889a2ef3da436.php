<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="csrf-token" content="<?php echo e(csrf_token()); ?>">
    <title>PhishGuard - Cybersecurity Awareness Training</title>
    <link rel="stylesheet" href="<?php echo e(asset('app.css')); ?>">
</head>
<body>
    <noscript>
        <main class="noscript">
            <h1>PhishGuard requires JavaScript</h1>
            <p>This local educational simulator runs entirely in your browser and stores only training progress in LocalStorage.</p>
        </main>
    </noscript>
    <div id="app" data-scenario-source="<?php echo e(asset('data/scenarios.json')); ?>"></div>
    <script type="module" src="<?php echo e(asset('app.js')); ?>"></script>
</body>
</html>
<?php /**PATH /home/p7/PhisingSim/resources/views/welcome.blade.php ENDPATH**/ ?>