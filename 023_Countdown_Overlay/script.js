let countdown;
let totalSeconds = 0;
let isRunning = false;

const display = document.getElementById('timer-display');
const btnStart = document.getElementById('btn-start');
const btnPause = document.getElementById('btn-pause');
const btnReset = document.getElementById('btn-reset');
const controlsPanel = document.getElementById('controls-panel');

const inputH = document.getElementById('input-h');
const inputM = document.getElementById('input-m');
const inputS = document.getElementById('input-s');

// Helper: Format time
function formatTime(seconds) {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = seconds % 60;
    return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
}

// Helper: Update Display
function updateDisplay() {
    display.textContent = formatTime(totalSeconds);
}

// Get Input Time
function getSecondsFromInput() {
    const h = parseInt(inputH.value) || 0;
    const m = parseInt(inputM.value) || 0;
    const s = parseInt(inputS.value) || 0;
    return (h * 3600) + (m * 60) + s;
}

function startTimer() {
    if (isRunning) return;

    // If starting from 0 (or paused at 0), get new input
    if (totalSeconds === 0) {
        totalSeconds = getSecondsFromInput();
        if (totalSeconds === 0) {
            alert("Masukkan waktu dulu dong!");
            return;
        }
    }

    isRunning = true;
    updateDisplay();
    btnStart.textContent = "Running...";
    btnStart.disabled = true;
    btnPause.disabled = false;

    // Disable inputs
    inputH.disabled = inputM.disabled = inputS.disabled = true;

    countdown = setInterval(() => {
        if (totalSeconds > 0) {
            totalSeconds--;
            updateDisplay();
        } else {
            clearInterval(countdown);
            isRunning = false;
            btnStart.textContent = "Start";
            btnStart.disabled = false;
            btnPause.disabled = true;
            // Play a sound or flash?
            display.style.color = "#ff4757"; // Red when done
            setTimeout(() => display.style.color = "", 1000);

            // Re-enable inputs
            inputH.disabled = inputM.disabled = inputS.disabled = false;
        }
    }, 1000);
}

function pauseTimer() {
    clearInterval(countdown);
    isRunning = false;
    btnStart.textContent = "Resume";
    btnStart.disabled = false;
    btnPause.disabled = true;
}

function resetTimer() {
    pauseTimer();
    btnStart.textContent = "Start";

    // Reset inputs
    inputH.disabled = inputM.disabled = inputS.disabled = false;

    // Wait, do we clear inputs or keep them?
    // Let's keep them for quick restart.
    totalSeconds = getSecondsFromInput();
    updateDisplay();
    // Restore display color just in case
    display.style.color = "";
}

// Event Listeners
btnStart.addEventListener('click', startTimer);
btnPause.addEventListener('click', pauseTimer);
btnReset.addEventListener('click', resetTimer);

// Background Toggles
document.getElementById('btn-toggle-bg').addEventListener('click', () => {
    document.body.classList.toggle('green-screen');
});

const btnHideUI = document.getElementById('btn-hide-ui');
btnHideUI.addEventListener('click', (e) => {
    e.stopPropagation(); // Prevent body click from firing immediately
    controlsPanel.classList.add('hidden');
});

// Show UI on double click anywhere
document.body.addEventListener('dblclick', () => {
    controlsPanel.classList.remove('hidden');
});

// Init
inputM.value = 10; // Default 10 mins
totalSeconds = getSecondsFromInput();
updateDisplay();
