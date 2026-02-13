document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('commentForm');
    const commentInput = document.getElementById('comment');

    if (form) {
        form.addEventListener('submit', function(e) {
            const value = commentInput.value;
            
            // Basic Client-Side Validation (Optional layer)
            // In a real scenario, this helps UI but doesn't replace server security
            if (value.length < 1) {
                e.preventDefault();
                alert('Comment cannot be empty');
            }
        });
    }
});
