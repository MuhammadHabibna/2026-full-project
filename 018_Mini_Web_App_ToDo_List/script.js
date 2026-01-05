document.addEventListener('DOMContentLoaded', () => {
    const todoInput = document.getElementById('todo-input');
    const addBtn = document.getElementById('add-btn');
    const todoList = document.getElementById('todo-list');

    // Load tasks from LocalStorage
    let tasks = JSON.parse(localStorage.getItem('tasks')) || [];

    // Initial Render
    renderTasks();

    // Event Listeners
    addBtn.addEventListener('click', addTask);
    todoInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') addTask();
    });

    // Add Task Function
    function addTask() {
        const text = todoInput.value.trim();
        if (text === '') return;

        const newTask = {
            id: Date.now(),
            text: text,
            completed: false
        };

        tasks.unshift(newTask); // Add to top
        saveTasks();
        renderTasks();
        todoInput.value = '';
        
        // Add animation focus
        todoInput.focus();
    }

    // Toggle Complete Function
    window.toggleTask = function(id) {
        tasks = tasks.map(task => 
            task.id === id ? { ...task, completed: !task.completed } : task
        );
        saveTasks();
        renderTasks();
    }

    // Delete Task Function
    window.deleteTask = function(id, element) {
        // Find the li element to animate removal
        const li = document.querySelector(`li[data-id="${id}"]`);
        
        if (li) {
            li.style.transform = 'translateX(100px)';
            li.style.opacity = '0';
            
            setTimeout(() => {
                tasks = tasks.filter(task => task.id !== id);
                saveTasks();
                renderTasks();
            }, 300);
        } else {
             // Fallback if animation fails or element not found
             tasks = tasks.filter(task => task.id !== id);
             saveTasks();
             renderTasks();
        }
    }

    // Save to LocalStorage
    function saveTasks() {
        localStorage.setItem('tasks', JSON.stringify(tasks));
    }

    // Render Tasks
    function renderTasks() {
        todoList.innerHTML = '';
        tasks.forEach(task => {
            const li = document.createElement('li');
            li.className = task.completed ? 'completed' : '';
            li.setAttribute('data-id', task.id);
            
            // Allow clicking the whole row to toggle, but prevent delete btn from triggering toggle
            li.onclick = (e) => {
                if (!e.target.closest('.delete-btn')) {
                    toggleTask(task.id);
                }
            };

            li.innerHTML = `
                <div class="check-icon">
                    <i class="fa-solid fa-check"></i>
                </div>
                <span>${escapeHtml(task.text)}</span>
                <button class="delete-btn" onclick="deleteTask(${task.id}, this)">
                    <i class="fa-solid fa-trash"></i>
                </button>
            `;
            
            todoList.appendChild(li);
        });
    }

    // Security: Escape HTML to prevent XSS
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
});
