document.getElementById('itemForm').addEventListener('submit', function (event){
    event.preventDefault();

    const code = document.getElementById('code').value;
    fetch('/api/record', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            code: code,
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Server response:', data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
