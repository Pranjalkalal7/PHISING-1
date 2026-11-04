<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('phishing_logs', function (Blueprint $table) {
            $table->id();
            $table->string('scenario_id')->nullable();
            $table->string('event_type')->default('training_event');
            $table->string('decision')->nullable();
            $table->boolean('correct')->nullable();
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('phishing_logs');
    }
};
