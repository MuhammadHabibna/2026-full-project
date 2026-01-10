document.addEventListener('DOMContentLoaded', () => {
    // State
    let habits = JSON.parse(localStorage.getItem('habits')) || [];
    let logs = JSON.parse(localStorage.getItem('logs')) || {}; // Format: { "YYYY-MM-DD": [habitId1, habitId2] }

    // DOM Elements
    const habitInput = document.getElementById('habit-input');
    const addBtn = document.getElementById('add-btn');
    const habitList = document.getElementById('habit-list');
    const currentDateEl = document.getElementById('current-date');
    const heatmapGrid = document.getElementById('heatmap-grid');
    const currentStreakEl = document.getElementById('current-streak');
    const totalDaysEl = document.getElementById('total-days');
    const completionRateEl = document.getElementById('completion-rate');

    // Init
    const today = new Date().toISOString().split('T')[0];
    currentDateEl.textContent = new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'short', day: 'numeric' });

    // Core Functions
    function saveInternal() {
        localStorage.setItem('habits', JSON.stringify(habits));
        localStorage.setItem('logs', JSON.stringify(logs));
        updateStats();
        renderHeatmap();
    }

    function addHabit() {
        const name = habitInput.value.trim();
        if (name) {
            const newHabit = {
                id: Date.now(),
                name: name,
                created: today
            };
            habits.push(newHabit);
            habitInput.value = '';
            saveInternal();
            renderHabits();
        }
    }

    function deleteHabit(id) {
        if (confirm('Delete this habit?')) {
            habits = habits.filter(h => h.id !== id);
            // Optional: Cleanup logs for this habit? keeping simple for now. 
            saveInternal();
            renderHabits();
        }
    }

    function toggleHabit(id) {
        if (!logs[today]) logs[today] = [];

        const index = logs[today].indexOf(id);
        if (index > -1) {
            logs[today].splice(index, 1); // Uncheck
        } else {
            logs[today].push(id); // Check
        }

        saveInternal();
        renderHabits();
    }

    function renderHabits() {
        habitList.innerHTML = '';

        if (habits.length === 0) {
            habitList.innerHTML = `
                <div class="empty-state">
                    <p>No habits yet. Start simple!</p>
                </div>`;
            return;
        }

        habits.forEach(habit => {
            const isCompleted = logs[today]?.includes(habit.id);
            const item = document.createElement('div');
            item.className = `habit-item ${isCompleted ? 'completed' : ''}`;
            item.onclick = (e) => {
                if (!e.target.closest('.delete-btn')) toggleHabit(habit.id);
            };

            item.innerHTML = `
                <div class="habit-info">
                    <div class="checkbox"></div>
                    <span class="habit-name">${habit.name}</span>
                </div>
                <button class="delete-btn" onclick="event.stopPropagation(); deleteHabit(${habit.id})">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M18 6L6 18M6 6l12 12"></path>
                    </svg>
                </button>
            `;

            // Passing the delete handler via inline for simplicity in this constrained env or use closure
            const delBtn = item.querySelector('.delete-btn');
            delBtn.onclick = (e) => {
                e.stopPropagation();
                deleteHabit(habit.id);
            }

            habitList.appendChild(item);
        });
    }

    function renderHeatmap() {
        heatmapGrid.innerHTML = '';

        // Generate last 365 days (approx 53 weeks)
        const endDate = new Date();
        const startDate = new Date();
        startDate.setDate(endDate.getDate() - 364);

        // Map data to easy lookup
        // We need to calculate "intensity" for each day
        // Intensity = completed_habits / total_habits_on_that_day
        // Since we don't track historical total habits easily, we'll use current habits count or simple count

        const dateMap = {};
        for (let d = new Date(startDate); d <= endDate; d.setDate(d.getDate() + 1)) {
            const dateStr = d.toISOString().split('T')[0];
            const completedCount = logs[dateStr]?.length || 0;
            // Simplified level logic: 
            // 0 = 0
            // 1 = 1-2
            // 2 = 3-4
            // 3 = 5-6
            // 4 = 7+ OR based on % if we knew total

            // Let's do a percentage-like approach if habits > 0
            let level = 0;
            if (completedCount > 0) {
                if (habits.length > 0) {
                    const pct = completedCount / habits.length;
                    if (pct <= 0.25) level = 1;
                    else if (pct <= 0.5) level = 2;
                    else if (pct <= 0.75) level = 3;
                    else level = 4;
                } else {
                    level = 1;
                }
            }

            const cell = document.createElement('div');
            cell.className = 'day-cell';
            cell.dataset.level = level;
            cell.title = `${dateStr}: ${completedCount} completed`;
            heatmapGrid.appendChild(cell);
        }
    }

    function updateStats() {
        // Total Active Days
        const activeDays = Object.keys(logs).filter(k => logs[k] && logs[k].length > 0).length;
        totalDaysEl.textContent = activeDays;

        // Current Streak
        // Count backwards from today (or yesterday if today is 0)
        let streak = 0;
        let d = new Date();
        // If today has activity?
        const tStr = d.toISOString().split('T')[0];
        if (!logs[tStr] || logs[tStr].length === 0) {
            // Check yesterday
            d.setDate(d.getDate() - 1);
        }

        while (true) {
            const dateStr = d.toISOString().split('T')[0];
            if (logs[dateStr] && logs[dateStr].length > 0) {
                streak++;
                d.setDate(d.getDate() - 1);
            } else {
                break;
            }
        }
        currentStreakEl.textContent = streak;

        // Completion Rate (All time stats)
        // Total possible completions = habits.length * days_since_start? Too complex.
        // Let's do: Today's completion rate
        if (habits.length > 0) {
            const todayCount = logs[today]?.length || 0;
            const rate = Math.round((todayCount / habits.length) * 100);
            completionRateEl.textContent = `${rate}%`;
        } else {
            completionRateEl.textContent = '0%';
        }
    }

    // Event Listeners
    addBtn.addEventListener('click', addHabit);
    habitInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') addHabit();
    });

    // Initial Render
    renderHabits();
    renderHeatmap();
    updateStats();
});
