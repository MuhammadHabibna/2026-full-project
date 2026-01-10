const wordsList = [
    "the", "be", "of", "and", "a", "to", "in", "he", "have", "it", "that", "for", "they", "i", "with", "as", "not", "on", "she", "at", "by", "this", "we", "you", "do", "but", "from", "or", "which", "one", "would", "all", "will", "there", "say", "who", "make", "when", "can", "more", "if", "no", "man", "out", "other", "so", "what", "time", "up", "go", "about", "than", "into", "could", "state", "only", "new", "year", "some", "take", "come", "these", "know", "see", "use", "get", "like", "then", "first", "any", "work", "now", "may", "such", "give", "over", "think", "most", "even", "find", "day", "also", "after", "way", "many", "must", "look", "before", "great", "back", "through", "long", "where", "much", "should", "well", "people", "down", "own", "just", "because", "good", "each", "those", "feel", "seem", "how", "high", "too", "place", "little", "world", "very", "still", "nation", "hand", "old", "life", "tell", "write", "become", "here", "show", "house", "both", "between", "need", "mean", "call", "develop", "under", "last", "right", "move", "thing", "general", "school", "never", "same", "another", "begin", "while", "number", "part", "turn", "real", "leave", "might", "want", "point", "form", "off", "child", "few", "small", "since", "against", "ask", "late", "home", "interest", "large", "person", "end", "open", "public", "follow", "during", "present", "without", "again", "hold", "govern", "around", "possible", "head", "consider", "word", "program", "problem", "however", "lead", "system", "set", "order", "eye", "plan", "run", "keep", "face", "fact", "group", "play", "stand", "increase", "early", "course", "change", "help", "line"
];

const timeDisplay = document.getElementById('time');
const wordsContainer = document.getElementById('words');
const inputField = document.getElementById('hidden-input');
const typingArea = document.getElementById('typing-area');
const focusOverlay = document.getElementById('focus-overlay');
const liveWpm = document.getElementById('live-wpm');
const liveAcc = document.getElementById('live-acc');
const configBtns = document.querySelectorAll('.config-btn');
const modal = document.getElementById('results-modal');
const finalWpm = document.getElementById('final-wpm');
const finalAcc = document.getElementById('final-acc');
const finalRaw = document.getElementById('final-raw');
const finalError = document.getElementById('final-error');

let timer = null;
let maxTime = 60;
let timeLeft = maxTime;
let charIndex = 0; // Current character index in current word
let wordIndex = 0; // Current word index
let isPlaying = false;
let isTyping = false; // Started typing?

let totalChars = 0;
let correctChars = 0;
let errors = 0;
let currentWords = [];

// Init
function initGame() {
    isPlaying = false;
    isTyping = false;
    if (timer) clearInterval(timer);

    timeLeft = maxTime;
    timeDisplay.innerText = timeLeft;

    charIndex = 0;
    wordIndex = 0;
    totalChars = 0;
    correctChars = 0;
    errors = 0;

    liveWpm.innerText = 0;
    liveAcc.innerText = '100%';

    inputField.value = '';
    wordsContainer.innerHTML = '';

    // Close modal
    modal.classList.remove('show');

    // Shuffle and load words
    // We create enough words to fill screens. 200 is plenty.
    currentWords = [...wordsList].sort(() => Math.random() - 0.5).slice(0, 100);

    currentWords.forEach(word => {
        let wordSpan = document.createElement('span');
        wordSpan.classList.add('word');

        word.split('').forEach(char => {
            let charSpan = document.createElement('span');
            charSpan.classList.add('letter');
            charSpan.innerText = char;
            wordSpan.appendChild(charSpan);
        });

        // Add a space represented implicitly, but we might want strict space handling?
        // Usually space is just moving to next word. We won't render a space character node unless we want to style it.
        // But the input logic relies on space.

        wordsContainer.appendChild(wordSpan);
    });

    // Set active class on first word
    wordsContainer.children[0].children[0].classList.add('active'); // active char

    // Reset scroll
    wordsContainer.style.marginTop = '0px';

    // Focus
    inputField.focus();
}

function startGame() {
    isTyping = true;
    timer = setInterval(updateTimer, 1000);
}

function updateTimer() {
    if (timeLeft > 0) {
        timeLeft--;
        timeDisplay.innerText = timeLeft;
        calculateStats();
    } else {
        finishGame();
    }
}

function finishGame() {
    clearInterval(timer);
    isPlaying = false;
    isTyping = false;
    inputField.blur();

    // Show results
    calculateStats(); // Final update
    finalWpm.innerText = liveWpm.innerText;
    finalAcc.innerText = liveAcc.innerText;
    finalRaw.innerText = totalChars;
    finalError.innerText = errors;

    modal.classList.add('show');
}

function calculateStats() {
    let timeElapsed = maxTime - timeLeft;
    if (timeElapsed === 0) return;

    let grossWpm = (totalChars / 5) / (timeElapsed / 60);
    let netWpm = ((totalChars / 5) - errors) / (timeElapsed / 60);
    netWpm = netWpm < 0 ? 0 : netWpm; // No negative WPM

    let accuracy = ((correctChars / totalChars) * 100);
    if (totalChars === 0) accuracy = 100;

    liveWpm.innerText = Math.round(netWpm);
    liveAcc.innerText = Math.round(accuracy) + '%';
}

function handleInput(e) {
    if (!isTyping && timeLeft > 0) {
        startGame();
    }

    let currentInput = inputField.value;

    // We only care about the last character usually, but input fields can be tricky.
    // Better strategy: Capture keydown/keypress.
    // But input field is good for mobile.

    // Let's rely on the input field value.
    // We need to know if space was pressed (handled in keydown listener usually)
    // Or we verify the whole string against current word

    // Actually, simple "check char by char" logic:
    // User types in inputField. 
    // If user presses SPACE, we move to next word.
    // If user types chars, we validate against current word.

    const wordSpans = wordsContainer.querySelectorAll('.word');
    const currentWordSpan = wordSpans[wordIndex];
    if (!currentWordSpan) return; // End of list
    const currentWord = currentWords[wordIndex];

    // If input ends with space, check if we should move to next word
    if (currentInput.endsWith(' ')) {
        // Space pressed
        // Mark remaining letters as incorrect if word isn't finished
        // But usually we just verify what was typed.

        // Simple logic:
        // Compare trimmed input with current word.
        const typedWord = currentInput.trim();

        // If word length matches or we want to allow skipping?
        // Standard typing test: Space moves to next word regardless of completion? 
        // Or space is only accepted if word is complete?
        // Let's do: Space moves to next word.

        // Count errors for untyped or wrong characters
        // ... (simplified for this demo: just move to next)

        // Reset input
        inputField.value = '';

        // Remove active from any char in this word
        Array.from(currentWordSpan.children).forEach(char => char.classList.remove('active'));

        // Move to next word
        wordIndex++;
        charIndex = 0;

        // Scroll logic (simple)
        if (currentWordSpan.offsetTop > typingArea.offsetHeight / 2) {
            // Logic to shift margin top?
            // Since we use flex wrap, detailed scroll calculation:
            // Get top diff
            // wordsContainer.style.marginTop = `-${currentWordSpan.offsetTop}px`;
            // Actually, safer:
            const firstWord = wordSpans[0];
            const currentTop = currentWordSpan.offsetTop;
            const firstTop = firstWord.offsetTop; // likely 0
            if (currentTop > 50) { // If we are on new line
                wordsContainer.style.marginTop = `-${currentTop - 10}px`;
            }
        }

        // Set active on new word first char
        if (wordSpans[wordIndex]) {
            wordSpans[wordIndex].children[0].classList.add('active');
        } else {
            // End of words list - generate more? or finish?
            finishGame();
        }

        // Update stats (count space as char for raw wpm?)
        totalChars++;
        if (typedWord === currentWord) {
            correctChars++; // Space is correct
        }

        return;
    }

    // If not space, we are typing the word
    // We need to compare specific character index
    // But input field has the whole string typed so far for this word.
    const typedVal = currentInput.split('');
    const wordCharsNodes = currentWordSpan.children;

    // Reset all chars color in this word first, then re-apply
    Array.from(wordCharsNodes).forEach(span => {
        span.classList.remove('correct', 'incorrect', 'active');
    });

    // Re-evaluate current input against word
    typedVal.forEach((char, index) => {
        if (index < wordCharsNodes.length) {
            const charSpan = wordCharsNodes[index];
            if (char === currentWord[index]) {
                charSpan.classList.add('correct');
            } else {
                charSpan.classList.add('incorrect');
            }
        }
    });

    // Set active cursor on next char
    if (typedVal.length < wordCharsNodes.length) {
        wordCharsNodes[typedVal.length].classList.add('active');
    }

    // Update active cursor index or logic?
    // We already moved the 'active' class.

    // Calculate stats live (rough)
    // A better way is tracking keypresses. But `input` event is good for mobile sync.
    // We just need to know if the last char typed was new totalChar.

    // Fix: totalChars should only increment on new keypress.
    // This `handleInput` re-runs on every change. 
    // We might double count if we just iterate.
    // Let's depend on the event listener for stats incrementing more precisely 
    // OR we track `prevInputLength`.
}

// Better handling with Keydown for space and stats
inputField.addEventListener('keydown', (e) => {
    // Prevent default if needed?
});

// Use input event for visual update
// Use a variable to track processed length to update totalChars
let lastInputLen = 0;

inputField.addEventListener('input', (e) => {
    if (!isTyping && timeLeft > 0) startGame();

    const val = inputField.value;
    const currentWordSpan = wordsContainer.querySelectorAll('.word')[wordIndex];
    const currentWordChars = currentWordSpan.querySelectorAll('.letter');
    const currentWordStr = currentWords[wordIndex];

    // Handle Space
    if (e.data === ' ' || (val.length > 0 && val[val.length - 1] === ' ')) {
        // Check validity of the word typed so far (minus the space)
        const typedWord = val.trim();

        // Calculate errors for this word now?
        // Let's assume user finished the word.

        // Compare typedWord with currentWordStr
        // Any missing chars count as errors? Usually typing tests allow skipping.
        // Any wrong chars are errors.

        // Update stats
        totalChars++; // space
        correctChars++; // space usually counts if word was correct? 
        // Standard WPM: 5 chars = 1 word.

        // Move next
        inputField.value = '';
        lastInputLen = 0;

        // Visually cleanup current word
        wordIndex++;
        currentWordChars.forEach(c => c.classList.remove('active'));

        // Scroll
        // Simple line check logic
        const nextWordSpan = wordsContainer.querySelectorAll('.word')[wordIndex];
        if (nextWordSpan) {
            nextWordSpan.children[0].classList.add('active');

            // Scroll Logic
            if (nextWordSpan.offsetTop !== currentWordSpan.offsetTop) {
                // New line detected?
                // If it's the second line or more
                // We want to keep current line visible
                // Or better: keep active line in middle or top.
                // Let's just create a generic offset based on font size (approx 36px line height?)
                const lineHeight = 55; // Approx from CSS
                if (nextWordSpan.offsetTop > lineHeight) {
                    wordsContainer.style.marginTop = `-${nextWordSpan.offsetTop}px`;
                }
            }
        } else {
            finishGame();
        }
        return;
    }

    // Backspace handling
    if (e.inputType === 'deleteContentBackward') {
        // Just removed a char.
        // Update totalChars? No, we don't decrement usually, or we do?
        // Usually backspacing allows correcting.
        // We shouldn't decrement totalChars (keypresses typed), but we decrement totalChars in terms of "current string length" logic?
        // WPM usually counts all keystrokes. But net WPM penalizes uncorrected errors.

        // Let's just re-render.
        lastInputLen = val.length;
    }
    else {
        // Did we add a char?
        if (val.length > lastInputLen) {
            totalChars++;

            // Check if correct
            const charIdx = val.length - 1;
            if (charIdx < currentWordStr.length) {
                if (val[charIdx] === currentWordStr[charIdx]) {
                    correctChars++;
                } else {
                    errors++;
                }
            } else {
                errors++; // Extra chars
            }
        }
        lastInputLen = val.length;
    }

    // Visual Update
    currentWordChars.forEach(c => c.classList.remove('correct', 'incorrect', 'active'));

    for (let i = 0; i < val.length; i++) {
        if (i < currentWordChars.length) {
            if (val[i] === currentWordStr[i]) {
                currentWordChars[i].classList.add('correct');
            } else {
                currentWordChars[i].classList.add('incorrect');
            }
        }
    }

    // Cursor
    if (val.length < currentWordChars.length) {
        currentWordChars[val.length].classList.add('active');
    }
});

// Controls
configBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        configBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        maxTime = parseInt(btn.dataset.time);
        timeLeft = maxTime;
        timeDisplay.innerText = maxTime;
        initGame();
        inputField.focus();
    });
});

// Focus handling
typingArea.addEventListener('click', () => {
    inputField.focus();
});

inputField.addEventListener('focus', () => {
    typingArea.classList.remove('blurred');
    focusOverlay.style.opacity = '0';
});

inputField.addEventListener('blur', () => {
    typingArea.classList.add('blurred');
    focusOverlay.style.opacity = '1';
});

// Keyboard
document.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
        e.preventDefault();
        initGame();
    }
});

// Init
window.onload = initGame;
