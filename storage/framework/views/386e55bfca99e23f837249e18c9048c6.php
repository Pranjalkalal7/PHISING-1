<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Simulation Login - PhishGuard</title>
    <style>
        body { margin: 0; font-family: Arial, sans-serif; background: #101923; color: #edf7f6; }
        main { min-height: 100vh; display: grid; place-items: center; padding: 24px; }
        .panel { width: min(380px, 100%); background: #172332; border: 1px solid #365164; border-radius: 8px; padding: 24px; box-shadow: 0 24px 80px rgba(0, 0, 0, .35); }
        h1 { margin: 0 0 8px; font-size: 1.6rem; }
        p { color: #b7c8d6; line-height: 1.5; }
        label { display: block; margin-top: 16px; color: #d8e6ee; font-weight: 700; }
        input { box-sizing: border-box; width: 100%; margin-top: 6px; padding: 12px; border-radius: 6px; border: 1px solid #516a7c; background: #0f1720; color: #edf7f6; }
        button, a { display: inline-block; margin-top: 18px; border: 0; border-radius: 6px; padding: 12px 14px; background: #21b6a8; color: #061112; font-weight: 800; text-decoration: none; cursor: pointer; }
        .warning { background: #3d2c12; border: 1px solid #d59f39; padding: 12px; border-radius: 6px; color: #ffe7b0; }
    </style>
</head>
<body>
<main>
    <section class="panel" aria-labelledby="sim-title">
        <h1 id="sim-title">Example Login Simulation</h1>
        <p class="warning">Simulation only. This page never collects, stores, logs, or sends credentials.</p>
        <?php if(session('simulation_warning')): ?>
            <p class="warning"><?php echo e(session('simulation_warning')); ?></p>
        <?php endif; ?>
        <form action="<?php echo e(route('phishing.capture')); ?>" method="POST">
            <?php echo csrf_field(); ?>
            <label for="email">Username</label>
            <input id="email" name="email" value="training-user" autocomplete="off" inputmode="text">
            <label for="password">Password</label>
            <input id="password" name="password" value="example-password" type="text" autocomplete="off">
            <button type="submit">Show Safety Warning</button>
        </form>
        <a href="/simulation">Back to PhishGuard</a>
    </section>
</main>
</body>
</html>
<?php /**PATH /home/p7/PhisingSim/resources/views/phishing/facebook.blade.php ENDPATH**/ ?>