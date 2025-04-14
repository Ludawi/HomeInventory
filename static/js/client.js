document.addEventListener('DOMContentLoaded', function () {
    console.log("JavaScript is working!");
});
fetch('/api/record', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'  // sending JSON
    },
    body: JSON.stringify({
        code: '123',
    })
})
.then(response => response.json())
.then(data => {
    console.log('Server response:', data);
})
.catch(error => {
    console.error('Error:', error);
});
