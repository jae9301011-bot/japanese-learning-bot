# Walkthrough - Japanese Learning App

**Status**: Completed
**Date**: 2026-02-14

## Overview
This application is a desktop-based Japanese vocabulary learning tool built with Python and Tkinter. It features a quiz mode, spaced repetition-style review, and native Text-to-Speech (TTS) pronunciation.

## Features Implemented
### 1. Vocabulary Quiz
- **JLPT N5 Level Data**: Automatically fetches word lists from a remote JSON source.
- **Interactive Quiz**: Displays Kanji and Reading, asks for Korean meaning.
- **Feedback System**: Immediate "Correct/Incorrect" feedback with score tracking.

### 2. Review System
- **Notepad Tab**: Lists all words with their learning status (Correct/Incorrect/Not Attempted).
- **Filtering**: View only "Incorrect" words to focus on weak points.
- **Retry Mode**: One-click "Retry Incorrect Words" button to create a custom quiz session for review.

### 3. Audio & Usability
- **Native TTS**: Uses macOS built-in `say` command for high-quality Japanese pronunciation (Kyoko voice) without external dependencies.
- **Robust UI**: Splash screen for smooth loading, macOS-compatible theme, and error handling.

## How to Run
### Option 1: Run from Source
1. Ensure Python 3.9+ is installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python gui.py
   ```

### Option 2: Standalone Executable
A standalone macOS application has been built.
1. Navigate to the `dist/` directory:
   ```bash
   cd dist
   ```
2. Open `JapaneseLearningApp.app` (or `JapaneseLearningApp` executable).
   - *Note*: You may need to standard macOS security check (Right-click -> Open) to run unsigned applications.

## Project Structure
- `gui.py`: Main application logic and UI.
- `fetch_data.py`: Utility to download vocabulary data.
- `data/`: Stores vocabulary JSON files and user progress.
- `dist/`: Contains the compiled executable.
