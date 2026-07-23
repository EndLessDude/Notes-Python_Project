function deleteNote(noteId){
    fetch('/delete-note', {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
        window.location.href = "/";
    });
}

// Auto-resize the note textarea as the user types
document.addEventListener('DOMContentLoaded', function() {
    const textarea = document.getElementById('note');
    if (textarea) {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    }
});
