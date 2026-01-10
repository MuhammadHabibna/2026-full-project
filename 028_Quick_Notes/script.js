document.addEventListener('DOMContentLoaded', () => {
    // State
    let notes = JSON.parse(localStorage.getItem('quick_notes_data')) || [];

    // DOM Elements
    const container = document.getElementById('notes-container');
    const addBtn = document.getElementById('add-note-btn');
    const searchInput = document.getElementById('search-input');
    const exportBtn = document.getElementById('export-btn');
    const importBtn = document.getElementById('import-btn');
    const importInput = document.getElementById('import-input');
    const toast = document.getElementById('toast');

    // --- Core Functions ---

    const saveNotes = () => {
        localStorage.setItem('quick_notes_data', JSON.stringify(notes));
    };

    const showToast = (msg) => {
        toast.textContent = msg;
        toast.classList.remove('hidden');
        setTimeout(() => toast.classList.add('hidden'), 2000);
    };

    const createNote = () => {
        const newNote = {
            id: Date.now(),
            title: '',
            content: '',
            pinned: false,
            updatedAt: Date.now()
        };
        notes.unshift(newNote); // Add to top
        saveNotes();
        renderNotes();
    };

    const deleteNote = (id) => {
        if (confirm('Delete this note?')) {
            notes = notes.filter(n => n.id !== id);
            saveNotes();
            renderNotes();
            showToast('Note deleted');
        }
    };

    const togglePin = (id) => {
        const note = notes.find(n => n.id === id);
        if (note) {
            note.pinned = !note.pinned;
            saveNotes();
            renderNotes();
            showToast(note.pinned ? 'Note pinned' : 'Note unpinned');
        }
    };

    const updateNote = (id, key, value) => {
        const note = notes.find(n => n.id === id);
        if (note) {
            note[key] = value;
            note.updatedAt = Date.now();
            saveNotes();
            // Don't re-render entire list to avoid losing focus
        }
    };

    const exportData = () => {
        const dataStr = JSON.stringify(notes, null, 2);
        const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr);

        const exportFileDefaultName = 'quick_notes_backup.json';

        const linkElement = document.createElement('a');
        linkElement.setAttribute('href', dataUri);
        linkElement.setAttribute('download', exportFileDefaultName);
        linkElement.click();
        showToast('Backup saved!');
    };

    const importData = (file) => {
        const reader = new FileReader();
        reader.onload = (event) => {
            try {
                const importedNotes = JSON.parse(event.target.result);
                if (Array.isArray(importedNotes)) {
                    // Merge strategy: Add imported notes to existing
                    // To replace instead: notes = importedNotes;
                    notes = [...importedNotes, ...notes];

                    // Remove duplicates based on ID (optional safeguard)
                    const uniqueNotes = Array.from(new Map(notes.map(item => [item.id, item])).values());
                    notes = uniqueNotes;

                    saveNotes();
                    renderNotes();
                    showToast('Notes imported successfully');
                } else {
                    alert('Invalid file format');
                }
            } catch (e) {
                alert('Error parsing JSON');
            }
        };
        reader.readAsText(file);
    };

    // --- Rendering ---

    const renderNotes = () => {
        container.innerHTML = '';
        const query = searchInput.value.toLowerCase();

        // Sort: Pinned first, then by UpdatedAt descending
        const sortedNotes = [...notes].sort((a, b) => {
            if (a.pinned === b.pinned) {
                return b.updatedAt - a.updatedAt;
            }
            return a.pinned ? -1 : 1;
        });

        const filteredNotes = sortedNotes.filter(note =>
            note.title.toLowerCase().includes(query) ||
            note.content.toLowerCase().includes(query)
        );

        if (filteredNotes.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <p>${query ? 'No matching notes found.' : 'No notes yet. Click "New Note" to start!'}</p>
                </div>
            `;
            return;
        }

        filteredNotes.forEach(note => {
            const card = document.createElement('div');
            card.className = `note-card ${note.pinned ? 'pinned' : ''}`;

            card.innerHTML = `
                <div class="note-header">
                    <input type="text" class="note-title" placeholder="Untitled" value="${note.title}">
                    <div class="note-actions">
                        <button class="icon-btn pin-btn ${note.pinned ? 'active' : ''}" title="Pin">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="${note.pinned ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2"><path d="M16 2v4l3 3h-6v8h3l-4 4-4-4h3V9H5l3-3V2z"/></svg>
                        </button>
                        <button class="icon-btn delete-btn" title="Delete">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
                        </button>
                    </div>
                </div>
                <textarea class="note-content" placeholder="Type something...">${note.content}</textarea>
            `;

            // Event Listeners for this card
            const titleInput = card.querySelector('.note-title');
            const contentInput = card.querySelector('.note-content');
            const pinBtn = card.querySelector('.pin-btn');
            const delBtn = card.querySelector('.delete-btn');

            // Debounce save for inputs
            // We use standard input event. Since we save to memory variable first, 
            // valid performance strategy is to just save on every input for local usage, 
            // or debounce localstorage write.
            // For simplicity and "instant" feel, we'll write directly.

            titleInput.addEventListener('input', (e) => updateNote(note.id, 'title', e.target.value));
            contentInput.addEventListener('input', (e) => updateNote(note.id, 'content', e.target.value));

            pinBtn.onclick = () => togglePin(note.id);
            delBtn.onclick = () => deleteNote(note.id);

            container.appendChild(card);
        });
    };

    // --- Global Listeners ---

    addBtn.onclick = createNote;

    searchInput.addEventListener('input', renderNotes);

    exportBtn.onclick = exportData;

    importBtn.onclick = () => importInput.click();
    importInput.onchange = (e) => {
        if (e.target.files.length > 0) {
            importData(e.target.files[0]);
            importInput.value = ''; // Reset
        }
    };

    // Initial render
    renderNotes();
});
