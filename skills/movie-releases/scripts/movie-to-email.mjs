#!/usr/bin/env node

/**
 * Movie Search + Email Script
 * Get movie info and send it via email
 * Usage: node movie-to-email.mjs "<email>" "<command>" [args...]
 *
 * Commands:
 *   latest [region] [days]  - Latest releases
 *   search <query> [year]   - Search for movies
 *   top-rated [region]      - Top-rated movies
 *   now-playing [region]    - Currently in theaters
 *
 * Examples:
 *   node movie-to-email.mjs user@example.com latest US 30
 *   node movie-to-email.mjs user@example.com search "Dune" 2024
 */

import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

async function runMovieSearch(args) {
  return new Promise((resolve, reject) => {
    const pythonScript = join(__dirname, 'movie_search.py');
    const python = spawn('python3', [pythonScript, ...args]);

    let stdout = '';
    let stderr = '';

    python.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    python.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    python.on('close', (code) => {
      if (code === 0) {
        resolve(stdout);
      } else {
        reject(new Error(`Movie search failed: ${stderr || 'Unknown error'}`));
      }
    });

    python.on('error', (err) => {
      reject(err);
    });
  });
}

async function sendEmail(to, subject, message) {
  const emailScript = join(__dirname, '../../../../helpers/send-email-cli.mjs');

  return new Promise((resolve, reject) => {
    const node = spawn('node', [emailScript, to, subject, message]);

    let stdout = '';
    let stderr = '';

    node.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    node.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    node.on('close', (code) => {
      if (code === 0) {
        resolve(stdout);
      } else {
        reject(new Error(`Email failed: ${stderr || 'Unknown error'}`));
      }
    });

    node.on('error', (err) => {
      reject(err);
    });
  });
}

async function main() {
  const args = process.argv.slice(2);

  if (args.length < 2) {
    console.error('Usage: node movie-to-email.mjs "<email>" "<command>" [args...]');
    console.error('');
    console.error('Commands:');
    console.error('  latest [region] [days]  - Latest releases');
    console.error('  search <query> [year]   - Search for movies');
    console.error('  top-rated [region]      - Top-rated movies');
    console.error('  now-playing [region]    - Currently in theaters');
    console.error('');
    console.error('Examples:');
    console.error('  node movie-to-email.mjs user@example.com latest US 30');
    console.error('  node movie-to-email.mjs user@example.com search "Dune" 2024');
    process.exit(1);
  }

  const [email, command, ...searchArgs] = args;

  try {
    console.log(`🎬 Searching for movies...`);

    // Get movie data
    const movieData = await runMovieSearch([command, ...searchArgs]);

    console.log(`✅ Got movie data, sending email...`);

    // Create subject line
    const subjects = {
      latest: 'Latest Movie Releases',
      search: 'Movie Search Results',
      'top-rated': 'Top-Rated Movies',
      'now-playing': 'Movies Now Playing'
    };
    const subjectLine = subjects[command] || 'Movie Information';

    // Send email
    await sendEmail(email, subjectLine, movieData);

    console.log(`🎉 Email sent successfully to ${email}!`);

  } catch (error) {
    console.error(`❌ Error: ${error.message}`);
    process.exit(1);
  }
}

main();
