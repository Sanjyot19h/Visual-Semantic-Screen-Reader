# Visionary: Visual-Semantic Screen Reader

**Category:** UI Automation · Voice AI · Accessibility

Visionary is an AI-powered screen reader that understands **what is visually happening on a webpage**, instead of reading raw HTML structures. It enables visually impaired users to browse the web through **natural voice interaction**.

---

##  Problem

Traditional screen readers rely on **DOM parsing**.
They read webpages like this:

> “link… button… div… image-1234.jpg…”

This approach exposes the **technical structure of the page**, not the **meaning of the content**, making modern websites extremely difficult for visually impaired users to navigate.

---

##  Solution

**Visionary replaces DOM-based reading with visual understanding.**

Instead of reading HTML tags, Visionary:

* Captures screenshots of the user’s browser
* Understands the visual layout using multimodal AI
* Interprets the page like a human would
* Responds conversationally through voice

This enables users to interact with the web naturally.

Example:

User asks:

```text
"What's the main headline on CNN right now?"
```

Visionary responds:

```text
"The main headline on your screen is: 'Global Markets React to AI Breakthrough.'"
```

---

##  How Visionary Works

Visionary combines **computer vision, voice AI, and agentic automation**.

1. **Screen Capture**
   A background process continuously captures screenshots of the user's browser.

2. **Visual Understanding (Nova Multimodal)**
   The screenshot is analyzed to understand layout and context such as:

   * Headlines
   * Products
   * Ads
   * Articles
   * Navigation elements

3. **Voice Interaction (Nova 2 Sonic)**
   Users interact through natural speech:

   ```text
   "Are there any good reviews for this product?"
   ```

4. **Agentic UI Actions (Nova Act)**
   Visionary can perform actions on behalf of the user.

   Example command:

   ```text
   "Add the black one to my cart."
   ```

   The AI visually identifies the correct button and performs the click.

---

##  System Architecture

![Visionary Architecture](architecture/Local Python Application-2026-03-14-060715.png)

### Local Client Environment (Python)

Runs directly on the user’s machine.

Components include:

* **Local Python Engine**
  Controls application state and AI requests.

* **Voice Capture & Playback**
  Captures microphone input and provides spoken responses.

* **Headless Browser Automation**
  Uses Playwright to interact with web pages.

* **Screen Capture Module**
  Generates viewport screenshots for visual analysis.

---

### AWS Cloud Backend

The AI reasoning and orchestration layer.

**AWS API Gateway**

* Secure endpoint for multimodal requests.

**AWS Lambda**

* Coordinates model execution.

**Amazon Bedrock Models**

* **Nova 2 Sonic**
  Handles speech-to-text and text-to-speech.

* **Nova Multimodal**
  Interprets screenshots and extracts context.

* **Nova Act**
  Performs UI actions such as clicking buttons or scrolling.

---

##   Workflow

```text
User Voice Input
      ↓
Speech Recognition (Nova Sonic)
      ↓
Screen Screenshot Captured
      ↓
Nova Multimodal Analysis
      ↓
Contextual AI Response
      ↓
(Optional) Nova Act Executes UI Action
```

---

##  Impact

Visionary enables visually impaired users to **experience the web as it is visually presented**, rather than as a collection of HTML elements.

This approach dramatically improves:

* Accessibility
* Web navigation
* Context understanding
* User independence

---
 