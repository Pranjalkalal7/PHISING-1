# PhishGuard - Phishing Awareness Simulation

PhishGuard is a locally runnable cybersecurity awareness training application. It presents fictional phishing and legitimate messages, asks learners to classify each one, and explains the indicators, safe actions, and correct answer after every decision.

This project is an educational simulator. It does not perform real phishing, send messages, collect credentials, redirect to external phishing sites, or store sensitive submissions.

## Features

- Security awareness dashboard with score, accuracy, completion, category coverage, and recent performance.
- Beginner-friendly training content for email phishing, spear phishing, smishing, vishing, credential phishing, social engineering, malicious attachments, fake websites, and business email compromise.
- Interactive scenario simulator with email, SMS, IT, cloud, delivery, recruiting, banking, and tax examples.
- 16 JSON-defined scenarios using only fictional organizations and `.example` domains.
- Challenge mode with 10 randomized non-duplicate scenarios and a phishing/legitimate mix.
- Results page with grade, missed categories, missed indicators, lessons, and recommendations.
- Internal-only simulated link warning pages.
- Safe simulated login form that intercepts submission and never stores or sends values.
- LocalStorage progress tracking for training metrics only.

## Technology

- Python & Streamlit for cloud deployment and interactive simulation (`streamlit_app.py`).
- Laravel 12 for local routing and serving the legacy app shell.
- Plain JavaScript modules for the browser application.
- CSS for responsive dark cybersecurity-themed UI.
- JSON for scenario definitions.
- LocalStorage / Session State for training progress.

## Streamlit Cloud Deployment

To deploy this project to Streamlit Community Cloud:

1. Push this repository to GitHub.
2. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click **New app** and select your repository and branch.
4. Set the **Main file path** to `streamlit_app.py`.
5. Click **Deploy!**

To run the Streamlit app locally:

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Local PHP Installation

Install PHP dependencies if needed:

```bash
composer install
```

Create an environment file if one does not exist:

```bash
cp .env.example .env
php artisan key:generate
```

Run locally:

```bash
php artisan serve
```

Open the URL shown by Artisan, usually:

```text
http://127.0.0.1:8000
```

## Build

No frontend build step is required for the current static simulator.

If you later add Node/npm and want to reintroduce a Vite pipeline:

```bash
npm install
npm run build
```

## Usage

1. Open the dashboard to view progress and score.
2. Study the training material.
3. Start the simulation.
4. Inspect sender, message tone, links, domains, attachments, and requests.
5. Select Phishing or Legitimate.
6. Review the explanation, indicators, and recommended action.
7. Complete challenge mode.
8. Review the results page and focus areas.

## Security

PhishGuard prevents unsafe behavior by design:

- It never collects or stores credentials, passwords, OTPs, payment details, API keys, cookies, or arbitrary form submissions.
- Scenario links are never opened externally. They route to `/simulation/link-warning/{scenario-id}` inside the app.
- Simulated login fields use dummy values and intercept submission.
- Progress storage is limited to training metrics such as score, answers, categories, and challenge history.
- Scenario content is rendered as text, not executable HTML.
- Scenario domains are fictional and use `.example`.
- The legacy credential-capture controller behavior has been disabled and replaced with a training warning.

## Project Structure

```text
app/Http/Controllers/PhishingController.php  Safe training-only simulated login handler
public/app.css                               Simulator UI styles
public/app.js                                Browser application logic
public/data/scenarios.json                   Scenario dataset
resources/views/welcome.blade.php           App shell
resources/views/phishing/facebook.blade.php  Safe legacy login simulation page
routes/web.php                               Local simulator routes
```

## Future Improvements

- Add React and Vite once Node/npm are available in the environment.
- Add optional instructor-created scenario imports with validation.
- Add exportable course reports that contain only aggregate training metrics.
- Add unit tests for scoring and progress utilities.
- Add SQLite or PostgreSQL support for classroom deployments.
