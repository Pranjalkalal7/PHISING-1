<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class PhishingLogs extends Model
{
    protected $fillable = ["scenario_id", "event_type", "decision", "correct"];
}
